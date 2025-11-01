import pytest
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
def auth_header(client):
    email = "episodio_test@example.com"
    senha = "senha12345"
    # Registra usuário para testar episódios
    r = client.post("/api/auth/register", json={
        "nome": "Episodio Tester",
        "email": email,
        "senha": senha
    })
    print("auth_header - registering user")
    print("Registro status:", r.status_code)
    print("Registro response:", r.json())
    assert r.status_code == 201

    # Login para obter token
    r = client.post("/api/auth/login",
                    json={"nome": "Episodio Tester", "email": email, "senha": senha})
    print("Login status:", r.status_code)
    if r.status_code != 200:
        print("Login response:", r.json())
    assert r.status_code == 200
    token = r.json().get("access_token")
    assert token is not None
    return {"Authorization": f"Bearer {token}"}


def test_crud_episodio(auth_header, client):
    # Criar episódio
    dados = {
        "data": "2025-10-24",
        "intensidade": 8,
        "duracao": 120,
        "observacoes": "Dor forte após café"
    }
    r = client.post("/api/episodios/", json=dados, headers=auth_header)
    print("test_crud_episodio - post /api/episodios/")
    print("Criar episódio status:", r.status_code)
    print("Criar episódio response:", r.json())
    assert r.status_code == 201
    eid = r.json()["id"]

    # Listar episódios
    r = client.get("/api/episodios/", headers=auth_header)
    print("test_crud_episodio - get /api/episodios/")
    print("Criar episódio status:", r.status_code)
    print("Criar episódio response:", r.json())
    assert r.status_code == 200
    assert len(r.json()) > 0

    # Ver episódio
    r = client.get(f"/api/episodios/{eid}", headers=auth_header)
    print(f"test_crud_episodio - get /api/episodios/{eid}")
    print("Criar episódio status:", r.status_code)
    print("Criar episódio response:", r.json())
    assert r.status_code == 200
    assert r.json()["intensidade"] == 8

    # Editar episódio
    novos_dados = {
        "data": "2025-10-25",
        "intensidade": 6,
        "duracao": 100,
        "observacoes": "Melhorando após medicação"
    }
    r = client.put(f"/api/episodios/{eid}", json=novos_dados, headers=auth_header)
    print(f"test_crud_episodio - put /api/episodios/{eid}")
    print("Criar episódio status:", r.status_code)
    print("Criar episódio response:", r.json())
    assert r.status_code == 200
    assert r.json()["intensidade"] == 6
    assert r.json()["observacoes"] == "Melhorando após medicação"

    # Excluir episódio
    print(f"test_crud_episodio - delete /api/episodios/{eid}")
    r = client.delete(f"/api/episodios/{eid}", headers=auth_header)
    print("Criar episódio status:", r.status_code)
    assert r.status_code == 204

    # Verificar exclusão
    r = client.get(f"/api/episodios/{eid}", headers=auth_header)
    print("test_crud_episodio - get /api/episodios/eid after deletion")
    print("Criar episódio status:", r.status_code)
    assert r.status_code == 404
