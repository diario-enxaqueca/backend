"""
Testes para o módulo Usuário.
"""
import pytest
from source.usuario.controller_usuario import hash_password, verify_password
from fastapi.testclient import TestClient
from main import app
from config.database import get_db, DATABASE_URL
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
def usuario_teste(client):
    """Cria o usuário para testes e retorna seus dados."""
    email = "teste_usuario_email_unico@email.com"
    data = {
        "nome": "Usuario Teste",
        "email": email,
        "senha": "senha12345"
    }
    response = client.post("/api/usuarios/register", json=data)
    assert response.status_code == 201
    return data


@pytest.fixture
def auth_header(client, usuario_teste):
    response = client.post("/api/usuarios/login", json={
        "nome": "Usuario Teste",
        "email": usuario_teste["email"],
        "senha": usuario_teste["senha"]
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_bcrypt_fix():
    """Testa hash e verificação de senha com mais de 72 caracteres."""
    senha = "a" * 200
    hash_ = hash_password(senha)
    print("Hash gerado:", hash_[:50], "...")
    assert verify_password(senha, hash_) is True


def test_register_usuario(client, db):
    """Testa registro de novo usuário."""
    response = client.post("/api/usuarios/register", json={
        "nome": "João Silva",
        "email": "joao@email.com",
        "senha": "senha12345"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "joao@email.com"
    assert data["nome"] == "João Silva"
    assert "id" in data


def test_register_email_duplicado(client, usuario_teste):
    """Testa que não permite email duplicado."""
    response = client.post("/api/usuarios/register", json={
        "nome": "Outro Usuario",
        "email": usuario_teste["email"],
        "senha": "outrasenha123"
    })
    assert response.status_code == 400
    assert "já cadastrado" in response.json()["detail"].lower()


def test_login_sucesso(client, usuario_teste):
    """Testa login com credenciais corretas."""
    response = client.post("/api/usuarios/login", json={
        "nome": usuario_teste["nome"],
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
        "nome": usuario_teste["nome"],
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


@pytest.mark.parametrize("senha_invalida,motivo", [
    ("123", "muito_curta"),
    ("1234567", "ainda_curta"),
    ("A" * 73, "muito_longa"),  # ✅ Testa senha muito longa
])
def test_validacao_senha(client, senha_invalida, motivo):
    """Testa validação de senha."""
    response = client.post("/api/usuarios/register", json={
        "nome": "Teste",
        "email": f"teste_{motivo}@email.com",
        "senha": senha_invalida
    })
    assert response.status_code == 422  # Validation error
