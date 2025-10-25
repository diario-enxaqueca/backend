import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def auth_header():
    # Registrar e fazer login para obter token
    r = client.post("/api/usuarios/register", json={
        "nome": "Tester",
        "email": "episodio@email.com",
        "senha": "senha12345"
    })
    assert r.status_code == 200
    r = client.post("/api/usuarios/login", json={
        "email": "episodio@email.com",
        "senha": "senha12345"
    })
    token = r.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_crud_episodio(auth_header):
    # Criar episódio
    dados = {
        "data": "2025-10-24",
        "intensidade": 8,
        "duracao": 120,
        "observacoes": "Dor forte após café"
    }
    r = client.post("/api/episodios/", json=dados, headers=auth_header)
    assert r.status_code == 201
    eid = r.json()["id"]

    # Listar episódios
    r = client.get("/api/episodios/", headers=auth_header)
    assert r.status_code == 200
    assert len(r.json()) > 0

    # Ver episódio
    r = client.get(f"/api/episodios/{eid}", headers=auth_header)
    assert r.status_code == 200
    assert r.json()["intensidade"] == 8

    # Editar episódio
    novos_dados = {
        "data": "2025-10-25",
        "intensidade": 6,
        "duracao": 100,
        "observacoes": "Melhorando após medicação"
    }
    r = client.put(f"/api/episodios/{eid}", json=novos_dados, headers=auth_header)
    assert r.status_code == 200
    assert r.json()["intensidade"] == 6
    assert r.json()["observacoes"] == "Melhorando após medicação"

    # Excluir episódio
    r = client.delete(f"/api/episodios/{eid}", headers=auth_header)
    assert r.status_code == 204

    # Episódio excluído não deve existir mais
    r = client.get(f"/api/episodios/{eid}", headers=auth_header)
    assert r.status_code == 404
