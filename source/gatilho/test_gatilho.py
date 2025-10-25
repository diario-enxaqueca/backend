"""
Testes para o módulo Gatilho.
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def auth_header():
    """Fixture para autenticação de teste."""
    # Registrar usuário
    client.post("/api/usuarios/register", json={
        "nome": "Gatilho Tester",
        "email": "gatilho@test.com",
        "senha": "senha12345"
    })
    
    # Fazer login
    response = client.post("/api/usuarios/login", json={
        "email": "gatilho@test.com",
        "senha": "senha12345"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_crud_gatilho(auth_header):
    """Testa CRUD completo de gatilhos."""
    
    # 1. Criar gatilho
    response = client.post(
        "/api/gatilhos/",
        json={"nome": "Estresse"},
        headers=auth_header
    )
    assert response.status_code == 201
    gatilho_id = response.json()["id"]
    assert response.json()["nome"] == "Estresse"
    
    # 2. Listar gatilhos
    response = client.get("/api/gatilhos/", headers=auth_header)
    assert response.status_code == 200
    assert len(response.json()) > 0
    
    # 3. Ver gatilho específico
    response = client.get(f"/api/gatilhos/{gatilho_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["nome"] == "Estresse"
    
    # 4. Editar gatilho
    response = client.put(
        f"/api/gatilhos/{gatilho_id}",
        json={"nome": "Estresse no Trabalho"},
        headers=auth_header
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Estresse no Trabalho"
    
    # 5. Excluir gatilho
    response = client.delete(f"/api/gatilhos/{gatilho_id}", headers=auth_header)
    assert response.status_code == 204
    
    # 6. Verificar que foi deletado
    response = client.get(f"/api/gatilhos/{gatilho_id}", headers=auth_header)
    assert response.status_code == 404

def test_gatilho_duplicado(auth_header):
    """Testa que não permite criar gatilho duplicado."""
    
    # Criar primeiro gatilho
    client.post(
        "/api/gatilhos/",
        json={"nome": "Chocolate"},
        headers=auth_header
    )
    
    # Tentar criar duplicado
    response = client.post(
        "/api/gatilhos/",
        json={"nome": "Chocolate"},
        headers=auth_header
    )
    assert response.status_code == 400
    assert "já cadastrado" in response.json()["detail"].lower()

@pytest.mark.parametrize("nome_invalido", [
    "A",  # Muito curto (mínimo 2)
    "X" * 101,  # Muito longo (máximo 100)
    "",  # Vazio
])
def test_validacao_nome(auth_header, nome_invalido):
    """Testa validação de nome de gatilho."""
    response = client.post(
        "/api/gatilhos/",
        json={"nome": nome_invalido},
        headers=auth_header
    )
    assert response.status_code == 422  # Validation error
