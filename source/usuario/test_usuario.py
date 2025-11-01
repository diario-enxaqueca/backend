import pytest
from fastapi.testclient import TestClient
from source.usuario.controller_usuario import get_usuario_by_email
from source.usuario.view_usuario import get_current_user
from source.auth.controller_auth import hash_password
from source.usuario.model_usuario import Usuario
from main import app
from config.database import get_db, DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
from datetime import datetime

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
    # Já que registro é no serviço auth, use dados mockados ou consulta ao banco direto
    return {"id": 1, "nome": "Usuario Teste", "email": "usuario@teste.com"}


@pytest.fixture
def usuario_real(db):
    usuario = Usuario(
        nome="Usuario Teste",
        email="usuario@teste.com",
        senha_hash=hash_password("12345678"),
        data_cadastro=datetime.utcnow()
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def test_get_usuario_by_email(db):
    email = "usuario_novo@teste.com"
    senha = "senha12345"
    usuario = Usuario(nome="Usuario Novo",
                      email=email, senha_hash=senha)
    db.add(usuario)
    db.commit()
    user = get_usuario_by_email(db, email)
    assert user.email == email


def test_read_me_route(client, usuario_teste):
    # simula token válido, ou utilize mock de dependência get_current_user
    def override_get_current_user():
        class User:
            def __init__(self, nome, email):
                self.nome = nome
                self.email = email
                self.id = 1
                self.data_cadastro = datetime.utcnow()
        return User(usuario_teste["nome"], usuario_teste["email"])
    app.dependency_overrides[get_current_user] = override_get_current_user

    res = client.get("/api/usuarios/me")
    app.dependency_overrides.clear()
    assert res.status_code == 200
    assert res.json()["email"] == usuario_teste["email"]


@pytest.mark.parametrize("novo_nome, novo_email", [
    ("Nome Alterado", "novo@email.com"),
    (None, "emailonly@mail.com"),
    ("NomeSomente", None),
])
def test_update_usuario(client, usuario_real, novo_nome, novo_email):
    def override_get_current_user():
        return usuario_real
    app.dependency_overrides[get_current_user] = override_get_current_user

    data = {}
    if novo_nome is not None:
        data["nome"] = novo_nome
    if novo_email is not None:
        data["email"] = novo_email
    data["senha"] = "12345678"

    res = client.put("/api/usuarios/me", json=data)

    print(f"Payload enviado: {data}")
    print(f"Status code: {res.status_code}")
    print(f"Response JSON: {res.json()}")

    app.dependency_overrides.clear()
    assert res.status_code == 200
    if novo_nome:
        assert res.json()["nome"] == novo_nome
    if novo_email:
        assert res.json()["email"] == novo_email


def test_delete_usuario(client, usuario_real):
    def override_get_current_user():
        return usuario_real
    app.dependency_overrides[get_current_user] = override_get_current_user

    res = client.delete("/api/usuarios/me")
    assert res.status_code == 204

    app.dependency_overrides.clear()

    # Verifica se o usuário foi realmente deletado
    res_get = client.get("/api/usuarios/me")
    assert res_get.status_code == 401  # Unauthorized após deleção
