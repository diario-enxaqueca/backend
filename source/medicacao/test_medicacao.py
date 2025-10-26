"""
Testes para o módulo Medicação.
"""
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
    # Registrar usuário
    register_resp = client.post("/api/usuarios/register", json={
        "nome": "Med Tester",
        "email": "medicacao@test.com",
        "senha": "senha12345"
    })
    assert register_resp.status_code == 201

    # Login para obter token
    login_resp = client.post(
        "/api/usuarios/login",
        json={"nome": "Med Tester",
              "email": "medicacao@test.com",
              "senha": "senha12345"})
    assert login_resp.status_code == 200
    token = login_resp.json().get("access_token")
    assert token is not None
    return {"Authorization": f"Bearer {token}"}


def test_crud_medicacao_completo(auth_header, client):
    """Testa CRUD completo de medicações."""

    # 1. Criar medicação com dosagem
    response = client.post(
        "/api/medicacoes/",
        json={"nome": "Paracetamol", "dosagem": "500mg"},
        headers=auth_header
    )
    assert response.status_code == 201
    medicacao_id = response.json()["id"]
    assert response.json()["nome"] == "Paracetamol"
    assert response.json()["dosagem"] == "500mg"

    # 2. Criar medicação sem dosagem
    response = client.post(
        "/api/medicacoes/",
        json={"nome": "Ibuprofeno"},
        headers=auth_header
    )
    assert response.status_code == 201
    assert response.json()["dosagem"] is None

    # 3. Listar medicações
    response = client.get("/api/medicacoes/", headers=auth_header)
    assert response.status_code == 200
    assert len(response.json()) >= 2

    # 4. Ver medicação específica
    response = client.get(f"/api/medicacoes/{medicacao_id}", headers=auth_header)
    assert response.status_code == 200
    assert response.json()["nome"] == "Paracetamol"

    # 5. Editar medicação (nome e dosagem)
    response = client.put(
        f"/api/medicacoes/{medicacao_id}",
        json={"nome": "Paracetamol Extra", "dosagem": "750mg"},
        headers=auth_header
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Paracetamol Extra"
    assert response.json()["dosagem"] == "750mg"

    # 6. Editar apenas dosagem
    response = client.put(
        f"/api/medicacoes/{medicacao_id}",
        json={"dosagem": "1000mg"},
        headers=auth_header
    )
    assert response.status_code == 200
    assert response.json()["dosagem"] == "1000mg"

    # 7. Excluir medicação
    response = client.delete(f"/api/medicacoes/{medicacao_id}", headers=auth_header)
    assert response.status_code == 204

    # 8. Verificar exclusão
    response = client.get(f"/api/medicacoes/{medicacao_id}", headers=auth_header)
    assert response.status_code == 404


def test_medicacao_duplicada(auth_header, client):
    """Testa que não permite criar medicação duplicada."""

    # Criar primeira medicação
    client.post(
        "/api/medicacoes/",
        json={"nome": "Dipirona", "dosagem": "500mg"},
        headers=auth_header
    )

    # Tentar criar duplicada
    response = client.post(
        "/api/medicacoes/",
        json={"nome": "Dipirona", "dosagem": "1000mg"},
        # Dosagem diferente, mas nome igual
        headers=auth_header
    )
    assert response.status_code == 400
    assert "já cadastrada" in response.json()["detail"].lower()


@pytest.mark.parametrize("dados_invalidos,campo_erro", [
    ({"nome": "A", "dosagem": "500mg"}, "nome"),  # Nome muito curto
    ({"nome": "X" * 101, "dosagem": "500mg"}, "nome"),  # Nome muito longo
    ({"nome": "Paracetamol", "dosagem": "X" * 101}, "dosagem"),  # Dosagem muito longa
])
def test_validacao_campos(auth_header, client, dados_invalidos, campo_erro):
    """Testa validação de campos."""
    response = client.post(
        "/api/medicacoes/",
        json=dados_invalidos,
        headers=auth_header
    )
    assert response.status_code == 422  # Validation error
    assert campo_erro in str(response.json())


def test_medicacao_sem_dosagem(auth_header, client):
    """Testa criação e edição de medicação sem dosagem."""

    # Criar sem dosagem
    response = client.post(
        "/api/medicacoes/",
        json={"nome": "Aspirina"},
        headers=auth_header
    )
    assert response.status_code == 201
    medicacao_id = response.json()["id"]
    assert response.json()["dosagem"] is None

    # Adicionar dosagem depois
    response = client.put(
        f"/api/medicacoes/{medicacao_id}",
        json={"dosagem": "100mg"},
        headers=auth_header
    )
    assert response.status_code == 200
    assert response.json()["dosagem"] == "100mg"

    # Remover dosagem (enviando null)
    response = client.put(
        f"/api/medicacoes/{medicacao_id}",
        json={"dosagem": None},
        headers=auth_header
    )
    print("Response após remoção de dosagem:", response.json())
    assert response.status_code == 200
    assert response.json()["dosagem"] is None
