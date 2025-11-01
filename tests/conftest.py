"""
Fixtures globais e configuração de testes.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import sys
import os
from config.database import Base, get_db
from main import app

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# URL do banco de testes (SQLite em memória)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

# Engine de teste
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Session de teste
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Fixture que cria um banco de dados limpo para cada teste."""
    # Cria as tabelas do metadata antes do teste
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        # Dropa as tabelas após o teste para isolar testes
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Fixture que fornece um TestClient do FastAPI com override do get_db."""

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Limpa override após uso
    app.dependency_overrides.clear()


@pytest.fixture
def usuario_teste(client):
    """
    Fixture que cria um usuário de teste via API no serviço de autenticação.
    Nota: Senha com tamanho entre 8 e 72 caracteres (limite bcrypt).
    """
    dados = {
        "nome": "Usuario Teste",
        "email": "teste_usuario@email.com",
        "senha": "senha12345"
    }

    response = client.post("/api/auth/register", json=dados)

    if response.status_code != 201:
        print("❌ Erro ao criar usuário teste:")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        pytest.fail(f"Falha ao criar usuário teste: {response.json()}")

    return {
        "id": response.json().get("id"),
        "nome": dados["nome"],
        "email": dados["email"],
        "senha": dados["senha"],
    }


@pytest.fixture
def auth_token(client, usuario_teste):
    """Fixture que retorna token JWT válido para usuário de teste."""

    response = client.post("/api/auth/login", json={
        "nome": usuario_teste["nome"],
        "email": usuario_teste["email"],
        "senha": usuario_teste["senha"]
    })

    if response.status_code != 200:
        print("❌ Erro no login:")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        pytest.fail(f"Falha no login: {response.json()}")

    return response.json().get("access_token")


@pytest.fixture
def auth_header(auth_token):
    """Fixture que retorna header Authorization para usar
    em requisições autenticadas."""

    return {"Authorization": f"Bearer {auth_token}"}
