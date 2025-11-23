"""
Fixtures globais e configuração de testes.
"""
# Nota: testes usam padrões diferentes (fixtures, imports locais).
# pylint: disable=redefined-outer-name, import-outside-toplevel
# pylint: disable=unused-argument, invalid-name, import-error

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
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


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
def usuario_teste(db):
    # Usuário mockado para endpoints que precisam de um usuário
    dados = {
        "nome": "Usuario Teste",
        "email": "teste_usuario@email.com",
        "senha": "senha12345",
    }

    # Cria usuário direto no DB para evitar dependência do serviço de auth
    from source.usuario.model_usuario import Usuario
    from source.usuario.controller_usuario import hash_password

    usuario = Usuario(
        nome=dados["nome"],
        email=dados["email"],
        senha_hash=hash_password(dados["senha"]),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    return {
        "id": usuario.id,
        "nome": dados["nome"],
        "email": dados["email"],
        "senha": dados["senha"],
    }


@pytest.fixture
def auth_token(client, usuario_teste):
    """Fixture que retorna token JWT válido para usuário de teste."""

    # Gera token JWT localmente sem passar pelo endpoint de login
    from config.settings import settings
    from jose import jwt

    token = jwt.encode(
        {"sub": usuario_teste["email"]},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return token


@pytest.fixture
def auth_header(auth_token):
    """Fixture que retorna header Authorization para usar
    em requisições autenticadas."""

    return {"Authorization": f"Bearer {auth_token}"}
