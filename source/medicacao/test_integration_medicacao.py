"""
Testes de integração focados no CRUD de medicação.

Contém apenas casos que exercitam os endpoints de medicação:
`POST /api/medicacoes/`, `GET /api/medicacoes/`,
`PUT /api/medicacoes/{id}` e `DELETE /api/medicacoes/{id}`.
"""

import pytest


@pytest.mark.integration
def test_crud_medicacao(client, auth_header):
    headers = auth_header

    # Criar medicação
    payload = {"nome": "Paracetamol", "dosagem": "500mg"}
    res = client.post("/api/medicacoes/", json=payload, headers=headers)
    assert res.status_code == 201
    created = res.json()
    medicacao_id = created.get("id")
    assert medicacao_id is not None

    # Listar e verificar presença
    res = client.get("/api/medicacoes/", headers=headers)
    assert res.status_code == 200
    lista = res.json()
    assert any(m.get("id") == medicacao_id for m in lista)

    # Atualizar
    update_payload = {"nome": "Paracetamol", "dosagem": "650mg"}
    res = client.put(f"/api/medicacoes/{medicacao_id}", json=update_payload,
                     headers=headers)
    assert res.status_code == 200
    assert res.json().get("dosagem") == "650mg"

    # Deletar
    res = client.delete(f"/api/medicacoes/{medicacao_id}", headers=headers)
    assert res.status_code == 204

    # Confirmar exclusão
    res = client.get("/api/medicacoes/", headers=headers)
    assert res.status_code == 200
    final = res.json()
    assert not any(m.get("id") == medicacao_id for m in final)


@pytest.mark.integration
def test_create_medicacao_invalid_returns_400(client, auth_header):
    headers = auth_header
    # Falta de campos obrigatórios
    res = client.post("/api/medicacoes/", json={"nome": ""}, headers=headers)
    assert res.status_code in (422, 400)
