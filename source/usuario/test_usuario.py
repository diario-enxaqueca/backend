"""
Testes unitários e parametrizados para o CRUD de `usuario`.

Cobertura focada nas funções do controller: criação, busca,
atualização e exclusão, além de comportamento de hashing.
"""

# pylint: disable=redefined-outer-name, import-outside-toplevel
# pylint: disable=unused-argument, invalid-name, import-error

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from source.usuario.controller_usuario import (
    create_usuario,
    get_usuario_by_email,
    update_usuario,
    delete_usuario,
    hash_password,
    pwd_context,
    MAX_PASSWORD_LENGTH,
)
# Usuario model not needed directly in these unit tests

# Usar SQLite em memória para testes (isolado do MySQL)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="function")
def db():
    """Provide a transactional DB session for tests."""
    # Garantir que as tabelas existam
    from config.database import Base
    import source.usuario.model_usuario  # noqa: F401  # pylint: disable=unused-import

    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def test_hash_password_truncates_and_verifies():
    long_password = "a" * 100 + "çñ"
    hashed = hash_password(long_password)
    # Recompute truncated form as controller does
    trunc = long_password.encode("utf-8")[:MAX_PASSWORD_LENGTH].decode(
        "utf-8", "ignore")
    assert pwd_context.verify(trunc, hashed)


def test_create_get_delete_usuario(db):
    user = create_usuario(db, "Unit Tester", "unit@test.local", "Pwd!1234")
    assert user.email == "unit@test.local"

    fetched = get_usuario_by_email(db, "unit@test.local")
    assert fetched is not None
    assert fetched.email == user.email

    delete_usuario(db, fetched)
    after = get_usuario_by_email(db, "unit@test.local")
    assert after is None


@pytest.mark.parametrize(
    "nome,email,expected_nome,expected_email",
    [
        ("Novo Nome", None, "Novo Nome", "u1@example.com"),
        (None, "novo@example.com", "User One", "novo@example.com"),
        ("Nome Ambos", "ambos@example.com", "Nome Ambos", "ambos@example.com"),
    ],
)
def test_update_usuario_parametrized(
    db,
    nome,
    email,
    expected_nome,
    expected_email,
):
    # criar usuário base
    base = create_usuario(db, "User One", "u1@example.com", "Senha123")

    updated = update_usuario(db, base, nome=nome, email=email)
    assert updated.nome == expected_nome
    assert updated.email == expected_email
