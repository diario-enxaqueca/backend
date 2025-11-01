import pytest
from fastapi.testclient import TestClient
from source.auth.controller_auth import (
    hash_password, verify_password, create_access_token)
from main import app
from config.database import get_db, DATABASE_URL
from config.settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
from datetime import timedelta
from jose import jwt as jose_jwt


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


def test_hash_and_verify_password():
    senha = "umaSenhaComplexa123"
    hashed = hash_password(senha)
    assert verify_password(senha, hashed) is True
    assert verify_password("senhaErrada", hashed) is False


@pytest.mark.parametrize("senha_invalida", [
    "123",      # muito curta
    "a"*73,     # muito longa
    "",         # vazia
])
def test_user_create_invalid_password(client, senha_invalida):
    data = {
        "nome": "Teste",
        "email": f"teste_{senha_invalida}@test.com",
        "senha": senha_invalida,
    }
    response = client.post("/api/auth/register", json=data)
    assert response.status_code == 422


def test_register_and_login(client):
    user_data = {
        "nome": "User Test",
        "email": "user@test.com",
        "senha": "senhaSegura123",
    }
    # Registro
    res_reg = client.post("/api/auth/register", json=user_data)
    assert res_reg.status_code == 201
    # Login
    res_login = client.post("/api/auth/login", json=user_data)
    assert res_login.status_code == 200
    token_data = res_login.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"


def test_access_protected_route(client):
    user_data = {
        "nome": "User Test",
        "email": "user2@test.com",
        "senha": "senhaSegura123",
    }
    client.post("/api/auth/register", json=user_data)
    res_login = client.post("/api/auth/login", json=user_data)
    token = res_login.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    res_me = client.get("/api/auth/me", headers=headers)
    assert res_me.status_code == 200
    assert res_me.json()["email"] == user_data["email"]


def test_create_access_token():
    data = {"sub": "user@example.com"}
    expires = timedelta(minutes=10)
    token = create_access_token(data, expires)
    assert isinstance(token, str)
    # O token JWT deve conter três partes separadas por pontos
    assert token.count('.') == 2

    # Opcional: decodificar para conferir 'sub' (requer a chave secreta e algoritmo)
    decoded = jose_jwt.decode(token,
                              settings.SECRET_KEY,
                              algorithms=[settings.ALGORITHM])
    assert decoded.get("sub") == "user@example.com"
