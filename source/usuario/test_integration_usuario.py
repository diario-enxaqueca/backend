"""
Testes de integração focados no CRUD de `usuario`.

Contém apenas casos que exercitam os endpoints de usuário: registro
(`POST /api/usuarios/`) e operações autenticadas em `/api/usuarios/me`.
"""

import pytest
from jose import jwt
from config.settings import settings


@pytest.mark.integration
def test_create_read_update_delete_usuario(client):
    # 1) Criar usuário via endpoint de usuário
    payload = {
        "nome": "Usuario Integração",
        "email": "user_integ@example.com",
        "senha": "SenhaInteg!23",
    }
    res = client.post("/api/usuarios/", json=payload)
    assert res.status_code == 201
    created = res.json()
    assert created["email"] == payload["email"]

    # 2) Gerar token JWT localmente (simula login do serviço de auth)
    token = jwt.encode(
        {"sub": payload["email"]},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    headers = {"Authorization": f"Bearer {token}"}

    # 3) Ler recurso protegido (/me)
    res = client.get("/api/usuarios/me", headers=headers)
    assert res.status_code == 200
    assert res.json()["email"] == payload["email"]

    # 4) Atualizar usuário
    update_payload = {
        "nome": "Usuario Atualizado",
        "email": "user_updated@example.com",
        "senha": "SenhaInteg!23",
    }
    res = client.put("/api/usuarios/me", json=update_payload, headers=headers)
    assert res.status_code == 200
    assert res.json()["nome"] == "Usuario Atualizado"
    assert res.json()["email"] == "user_updated@example.com"

    # Gerar novo token com o email atualizado
    token = jwt.encode(
        {"sub": "user_updated@example.com"},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    headers = {"Authorization": f"Bearer {token}"}

    # 5) Deletar usuário
    res = client.delete("/api/usuarios/me", headers=headers)
    assert res.status_code == 204

    # 6) Após deleção, token não deve mais permitir acesso
    res = client.get("/api/usuarios/me", headers=headers)
    assert res.status_code == 401


@pytest.mark.integration
def test_register_duplicate_email_returns_400(client):
    payload = {
        "nome": "Dup User",
        "email": "dup@example.com",
        "senha": "SenhaDup!23",
    }
    res = client.post("/api/usuarios/", json=payload)
    assert res.status_code == 201

    # Tentativa de registrar novamente com mesmo email
    res2 = client.post("/api/usuarios/", json=payload)
    assert res2.status_code == 400
