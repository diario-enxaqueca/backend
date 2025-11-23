"""
Testes unitários e parametrizados para o CRUD de Episódio.

Usam diretamente as funções do controller (`create_episodio`,
`get_episodio`, `get_episodios_usuario`, `update_episodio`, `delete_episodio`)
com uma sessão transacional (savepoint) para isolamento.
"""

# pylint: disable=invalid-name,redefined-outer-name,import-outside-toplevel

from datetime import date
import pytest
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from source.episodio.controller_episodio import (
    create_episodio,
    get_episodio,
    get_episodios_usuario,
    update_episodio,
    delete_episodio,
)
from source.usuario.controller_usuario import create_usuario

# Usar SQLite em memória para testes (não usar banco real)
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
    connection = engine.connect()
    transaction = connection.begin()

    # Garantir que as tabelas existam no banco de teste
    from config.database import Base
    # importar models para registrar metadata
    import source.usuario.model_usuario  # pylint: disable=unused-import
    import source.episodio.model_episodio  # pylint: disable=unused-import
    import source.gatilho.model_gatilho  # pylint: disable=unused-import
    import source.medicacao.model_medicacao  # pylint: disable=unused-import
    Base.metadata.create_all(bind=connection)

    session = TestingSessionLocal(bind=connection)

    nested = connection.begin_nested()

    @sa.event.listens_for(session, "after_transaction_end")
    def restart_savepoint(_session, _transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()

    try:
        yield session
    finally:
        session.close()
        # limpar tabelas criadas para o teste
        Base.metadata.drop_all(bind=connection)
        transaction.rollback()
        connection.close()


def test_create_get_delete_episodio(db):
    user = create_usuario(db, "Epi User", "epi@test.local", "Senha1")

    epi = create_episodio(
        db,
        user.id,
        date(2025, 10, 24),
        8,
        duracao=120,
        observacoes="obs",
    )
    assert epi.id is not None
    assert epi.intensidade == 8

    fetched = get_episodio(db, epi.id, user.id)
    assert fetched is not None
    assert fetched.id == epi.id

    delete_episodio(db, fetched)
    after = get_episodio(db, epi.id, user.id)
    assert after is None


@pytest.mark.parametrize(
    "field, value, expected",
    [
        ("intensidade", 5, 5),
        ("observacoes", "novo texto", "novo texto"),
        ("duracao", 45, 45),
    ],
)
def test_update_episodio_parametrized(db, field, value, expected):
    user = create_usuario(db, "Epi User2", "epi2@test.local", "Senha1")
    epi = create_episodio(
        db,
        user.id,
        date(2025, 10, 24),
        7,
        duracao=60,
        observacoes="orig",
    )

    updated = update_episodio(db, epi, **{field: value})
    assert getattr(updated, field) == expected


def test_get_episodios_usuario_pagination(db):
    user = create_usuario(db, "Epi User3", "epi3@test.local", "Senha1")
    # criar 3 episódios
    for i in range(3):
        create_episodio(db, user.id, date(2025, 10, 20 + i), intensidade=3 + i)

    all_list = get_episodios_usuario(db, user.id)
    assert len(all_list) == 3

    limited = get_episodios_usuario(db, user.id, skip=1, limit=1)
    assert len(limited) == 1
