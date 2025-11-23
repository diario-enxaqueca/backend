"""
Testes de integração focados no CRUD de episódios.

Contém apenas casos que exercitam os endpoints de episódio:
`POST /api/episodios/`, `GET /api/episodios/`,
`PUT /api/episodios/{id}` e `DELETE /api/episodios/{id}`.
"""

import pytest


@pytest.mark.integration
def test_crud_episodio(client, auth_header):
    """Cobre criação, leitura, atualização e exclusão de episódio."""
    headers = auth_header

    # Criar episódio
    payload = {
        "data": "2025-10-24",
        "intensidade": 8,
        "duracao": 120,
        "observacoes": "Teste CRUD episodio",
    }
    res = client.post("/api/episodios/", json=payload, headers=headers)
    assert res.status_code == 201
    created = res.json()
    episodio_id = created.get("id")
    assert episodio_id is not None

    # Listar - deve conter 1 episódio
    res = client.get("/api/episodios/", headers=headers)
    assert res.status_code == 200
    lista = res.json()
    assert any(e.get("id") == episodio_id for e in lista)

    # Atualizar episódio
    update_payload = {
        "data": "2025-10-25",
        "intensidade": 6,
        "duracao": 90,
        "observacoes": "Atualizado",
    }
    res = client.put(f"/api/episodios/{episodio_id}", json=update_payload,
                     headers=headers)
    assert res.status_code == 200
    assert res.json().get("intensidade") == 6

    # Deletar episódio
    res = client.delete(f"/api/episodios/{episodio_id}", headers=headers)
    assert res.status_code == 204

    # Confirmar exclusão
    res = client.get("/api/episodios/", headers=headers)
    assert res.status_code == 200
    lista_final = res.json()
    assert not any(e.get("id") == episodio_id for e in lista_final)


@pytest.mark.integration
def test_create_invalid_data_returns_400(client, auth_header):
    headers = auth_header
    # Intensidade fora do range, por exemplo
    payload = {"data": "2025-10-24", "intensidade": 99}
    res = client.post("/api/episodios/", json=payload, headers=headers)
    assert res.status_code in (422, 400)
