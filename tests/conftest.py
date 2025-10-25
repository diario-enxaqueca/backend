"""
Fixtures globais e configuração de testes.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

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
    """
    Fixture que cria um banco de dados limpo para cada teste.
    """
    # Criar todas as tabelas
    Base.metadata.create_all(bind=engine)
    
    # Criar sessão
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        # Dropar todas as tabelas após o teste
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """
    Fixture que fornece um TestClient do FastAPI.
    Override da dependência get_db para usar o banco de testes.
    """
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Limpar overrides após o teste
    app.dependency_overrides.clear()


@pytest.fixture
def usuario_teste(client):
    """
    Fixture que cria um usuário de teste e retorna seus dados.
    """
    dados = {
        "nome": "Usuario Teste",
        "email": "teste@email.com",
        "senha": "senha12345"
    }
    
    response = client.post("/api/usuarios/register", json=dados)
    assert response.status_code == 200
    
    return {
        "id": response.json()["id"],
        "nome": dados["nome"],
        "email": dados["email"],
        "senha": dados["senha"]
    }


@pytest.fixture
def auth_token(client, usuario_teste):
    """
    Fixture que retorna um token JWT válido.
    """
    response = client.post("/api/usuarios/login", json={
        "email": usuario_teste["email"],
        "senha": usuario_teste["senha"]
    })
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_header(auth_token):
    """
    Fixture que retorna headers de autenticação prontos para uso.
    """
    return {"Authorization": f"Bearer {auth_token}"}
