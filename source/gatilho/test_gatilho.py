"""
Testes unitários e parametrizados para o CRUD de gatilho.

Chamam diretamente as funções do controller para verificar
criação, leitura, atualização, remoção e paginação. A fixture
`db` usa uma transação com savepoint para isolar cada teste.
"""

# pylint: disable=invalid-name,redefined-outer-name,import-outside-toplevel

import pytest
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.database import DATABASE_URL
from source.gatilho.controller_gatilho import (
    create_gatilho,
    get_gatilho,
    get_gatilhos_usuario,
    update_gatilho,
    delete_gatilho,
)
from source.usuario.controller_usuario import create_usuario


engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()

    # Garantir que as tabelas existam para os testes
    from config.database import Base
    import source.usuario.model_usuario  # pylint: disable=unused-import
    import source.gatilho.model_gatilho  # pylint: disable=unused-import
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
        Base.metadata.drop_all(bind=connection)
        transaction.rollback()
        connection.close()


def test_create_get_delete_gatilho(db):
    user = create_usuario(db, "Gat User", "gat@test.local", "Senha1")

    gat = create_gatilho(
        db,
        user.id,
        nome="Luz",
    )
    assert gat.id is not None
    assert gat.nome == "Luz"

    fetched = get_gatilho(db, gat.id, user.id)
    assert fetched is not None
    assert fetched.id == gat.id

    delete_gatilho(db, fetched)
    after = get_gatilho(db, gat.id, user.id)
    assert after is None


@pytest.mark.parametrize(
    "value, expected",
    [
        ("Janela", "Janela"),
        ("Café", "Café"),
        ("Estresse", "Estresse"),
    ],
)
def test_update_gatilho_parametrized(db, value, expected):
    user = create_usuario(db, "Gat User2", "gat2@test.local", "Senha1")
    gat = create_gatilho(
        db,
        user.id,
        nome="Botao",
    )

    updated = update_gatilho(db, gat, nome=value)
    assert updated.nome == expected


def test_get_gatilhos_usuario_pagination(db):
    user = create_usuario(db, "Gat User3", "gat3@test.local", "Senha1")
    for i in range(4):
        create_gatilho(db, user.id, nome=f"G{i}")

    all_list = get_gatilhos_usuario(db, user.id)
    assert len(all_list) == 4
