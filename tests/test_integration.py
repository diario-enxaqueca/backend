"""
Testes de integração - fluxo completo da aplicação.
"""
import pytest

@pytest.mark.integration
def test_fluxo_completo_usuario_episodio(client):
    """
    Testa fluxo completo: registro → login → criar episódio → listar → editar → deletar
    """
    # 1. Registrar usuário
    response = client.post("/api/usuarios/register", json={
        "nome": "Fluxo Teste",
        "email": "fluxo@test.com",
        "senha": "senha12345"
    })
    assert response.status_code == 200
    
    # 2. Login
    response = client.post("/api/usuarios/login", json={
        "email": "fluxo@test.com",
        "senha": "senha12345"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Criar episódio
    response = client.post("/api/episodios/", json={
        "data": "2025-10-24",
        "intensidade": 8,
        "duracao": 120,
        "observacoes": "Teste de integração"
    }, headers=headers)
    assert response.status_code == 201
    episodio_id = response.json()["id"]
    
    # 4. Listar episódios
    response = client.get("/api/episodios/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    # 5. Editar episódio
    response = client.put(f"/api/episodios/{episodio_id}", json={
        "data": "2025-10-25",
        "intensidade": 6,
        "duracao": 90,
        "observacoes": "Melhorando"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["intensidade"] == 6
    
    # 6. Deletar episódio
    response = client.delete(f"/api/episodios/{episodio_id}", headers=headers)
    assert response.status_code == 204
    
    # 7. Verificar que foi deletado
    response = client.get("/api/episodios/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.integration
@pytest.mark.slow
def test_fluxo_com_gatilhos_e_medicacoes(client, auth_header):
    """
    Testa fluxo completo com gatilhos e medicações.
    """
    # 1. Criar gatilhos
    gatilhos = []
    for nome in ["Estresse", "Café", "Chocolate"]:
        response = client.post("/api/gatilhos/", json={"nome": nome}, headers=auth_header)
        assert response.status_code == 201
        gatilhos.append(response.json()["id"])
    
    # 2. Criar medicações
    medicacoes = []
    for nome, dosagem in [("Paracetamol", "500mg"), ("Ibuprofeno", "400mg")]:
        response = client.post("/api/medicacoes/", json={
            "nome": nome,
            "dosagem": dosagem
        }, headers=auth_header)
        assert response.status_code == 201
        medicacoes.append(response.json()["id"])
    
    # 3. Listar todos
    response = client.get("/api/gatilhos/", headers=auth_header)
    assert len(response.json()) == 3
    
    response = client.get("/api/medicacoes/", headers=auth_header)
    assert len(response.json()) == 2
