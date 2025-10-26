"""
Testes para o módulo Gatilho.
"""
import pytest
from fastapi.testclient import TestClient
from main import app
from config.database import SessionLocal, Base, get_db, DATABASE_URL

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    # Cria conexão e transação principal
    connection = engine.connect()
    transaction = connection.begin()

    # Cria sessão ligada à conexão
    session = TestingSessionLocal(bind=connection)

    # Cria transação aninhada (savepoint)
    nested = connection.begin_nested()

    @sa.event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c



@pytest.fixture
def auth_header(client):
    # Registrar usuário
    register_resp = client.post("/api/usuarios/register", json={
        "nome": "Gatilho Tester",
        "email": "gatilho@test.com",
        "senha": "senha12345"
    })
    assert register_resp.status_code == 201

    # Login para obter token
    login_resp = client.post("/api/usuarios/login", json={
        "nome": "Gatilho Tester",
        "email": "gatilho@test.com",
        "senha": "senha12345"
    })
    assert login_resp.status_code == 200
    token = login_resp.json().get("access_token")
    assert token is not None
    return {"Authorization": f"Bearer {token}"}


def test_crud_gatilho(auth_header, client):
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


def test_gatilho_duplicado(auth_header, client):
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
def test_validacao_nome(auth_header, client, nome_invalido):
    """Testa validação de nome de gatilho."""
    response = client.post(
        "/api/gatilhos/",
        json={"nome": nome_invalido},
        headers=auth_header
    )
    assert response.status_code == 422  # Validation error