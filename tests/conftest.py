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

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.database import Base, get_db
from main import app

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
    Base.metadata.create_all(bind=engine)
    db_session = TestingSessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Fixture que fornece um TestClient do FastAPI."""
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture
def usuario_teste(client):
    """
    Fixture que cria um usuário de teste.
    IMPORTANTE: Senha deve ter 8-72 caracteres (limite bcrypt).
    """
    dados = {
        "nome": "Usuario Teste",
        "email": "teste_usuario@email.com",
        "senha": "senha12345"  # ✅ Senha válida: 10 caracteres
    }
    
    response = client.post("/api/usuarios/register", json=dados)
    
    # Debug se falhar
    if response.status_code != 201:
        print(f"❌ Erro ao criar usuário teste:")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        pytest.fail(f"Falha ao criar usuário teste: {response.json()}")
    
    return {
        "id": response.json()["id"],
        "nome": dados["nome"],
        "email": dados["email"],
        "senha": dados["senha"]
    }


@pytest.fixture
def auth_token(client, usuario_teste):
    """Fixture que retorna um token JWT válido."""
    response = client.post("/api/usuarios/login", json={
        "nome": usuario_teste["nome"],  # ✅ Adicionado nome
        "email": usuario_teste["email"],
        "senha": usuario_teste["senha"]
    })
    
    if response.status_code != 200:
        print(f"❌ Erro no login:")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        pytest.fail(f"Falha no login: {response.json()}")
    
    return response.json()["access_token"]


@pytest.fixture
def auth_header(auth_token):
    """Fixture que retorna headers de autenticação."""
    return {"Authorization": f"Bearer {auth_token}"}
