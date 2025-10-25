"""
Testes para o módulo Usuário.
"""
import pytest

def test_register_usuario(client):
    """Testa registro de novo usuário."""
    response = client.post("/api/usuarios/register", json={
        "nome": "João Silva",
        "email": "joao@email.com",
        "senha": "senha12345"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "joao@email.com"
    assert data["nome"] == "João Silva"
    assert "id" in data


def test_register_email_duplicado(client, usuario_teste):
    """Testa que não permite email duplicado."""
    response = client.post("/api/usuarios/register", json={
        "nome": "Outro Usuario",
        "email": usuario_teste["email"],  # Email já existe
        "senha": "outrasenha123"
    })
    assert response.status_code == 400
    assert "já cadastrado" in response.json()["detail"].lower()


def test_login_sucesso(client, usuario_teste):
    """Testa login com credenciais corretas."""
    response = client.post("/api/usuarios/login", json={
        "email": usuario_teste["email"],
        "senha": usuario_teste["senha"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_senha_incorreta(client, usuario_teste):
    """Testa login com senha incorreta."""
    response = client.post("/api/usuarios/login", json={
        "email": usuario_teste["email"],
        "senha": "senhaerrada"
    })
    assert response.status_code == 401


def test_get_perfil(client, auth_header, usuario_teste):
    """Testa obtenção de perfil do usuário logado."""
    response = client.get("/api/usuarios/me", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == usuario_teste["email"]
    assert data["nome"] == usuario_teste["nome"]


@pytest.mark.parametrize("senha_invalida", [
    "123",      # Muito curta
    "1234567",  # Ainda curta (mínimo 8)
])
def test_validacao_senha(client, senha_invalida):
    """Testa validação de senha mínima."""
    response = client.post("/api/usuarios/register", json={
        "nome": "Teste",
        "email": "teste@email.com",
        "senha": senha_invalida
    })
    assert response.status_code == 422  # Validation error
