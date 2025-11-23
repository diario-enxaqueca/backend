"""
Testes de integração focados no CRUD de gatilho.

Mantém apenas casos que exercitam os endpoints de gatilho:
`POST /api/gatilhos/`, `GET /api/gatilhos/`,
`PUT /api/gatilhos/{id}` e `DELETE /api/gatilhos/{id}`.
"""

import pytest


@pytest.mark.integration
def test_crud_gatilho(client, auth_header):
    headers = auth_header

    # Criar gatilho
    payload = {"nome": "Estresse"}
    res = client.post("/api/gatilhos/", json=payload, headers=headers)
    assert res.status_code == 201
    created = res.json()
    gatilho_id = created.get("id")
    assert gatilho_id is not None

    # Listar - deve conter o gatilho criado
    res = client.get("/api/gatilhos/", headers=headers)
    assert res.status_code == 200
    lista = res.json()
    assert any(g.get("id") == gatilho_id for g in lista)

    # Atualizar
    update_payload = {"nome": "Estresse Atualizado"}
    res = client.put(f"/api/gatilhos/{gatilho_id}", json=update_payload,
                     headers=headers)
    assert res.status_code == 200
    assert res.json().get("nome") == "Estresse Atualizado"

    # Deletar
    res = client.delete(f"/api/gatilhos/{gatilho_id}", headers=headers)
    assert res.status_code == 204

    # Confirmar exclusão
    res = client.get("/api/gatilhos/", headers=headers)
    assert res.status_code == 200
    final = res.json()
    assert not any(g.get("id") == gatilho_id for g in final)


@pytest.mark.integration
def test_create_gatilho_invalid_returns_400(client, auth_header):
    headers = auth_header
    # Nome obrigatório -> enviar payload vazio
    res = client.post("/api/gatilhos/", json={}, headers=headers)
    assert res.status_code in (422, 400)
