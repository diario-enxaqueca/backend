"""Testes para o módulo Medicação."""

# pylint: disable=redefined-outer-name,import-outside-toplevel

import pytest
from fastapi.testclient import TestClient
from main import app
from config.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError
from source.medicacao.controller_medicacao import update_medicacao
from source.medicacao.model_medicacao import Medicacao


# Usar SQLite em memória para testes (isolado do MySQL)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
testing_session_local = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="function")
def db():
    """Cria um banco de dados limpo para cada teste."""
    # Garantir que as tabelas existam
    from config.database import Base
    # pylint: disable=unused-import
    # import source.usuario.model_usuario
    # pylint: disable=unused-import
    # import source.medicacao.model_medicacao
    # pylint: disable=unused-import
    # import source.episodio.model_episodio
    # Imports necessários para criar tabelas; ignorar se não usados diretamente
    # noqa: F401  # pylint: disable=unused-import
    # import source.gatilho.model_gatilho

    Base.metadata.create_all(bind=engine)
    db_session = testing_session_local()
    try:
        yield db_session
    finally:
        db_session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c


@pytest.fixture
def auth_header(db):
    """Cria usuário e retorna header de autenticação."""
    # Criar usuário diretamente no banco
    from source.usuario.model_usuario import Usuario
    from source.usuario.controller_usuario import hash_password

    usuario = Usuario(
        nome="Med Tester",
        email="medicacao@test.com",
        senha_hash=hash_password("senha12345"),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    # Gerar token JWT
    from config.settings import settings
    from jose import jwt

    token = jwt.encode(
        {"sub": usuario.email},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
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
    url = f"/api/medicacoes/{medicacao_id}"
    response = client.get(url, headers=auth_header)
    assert response.status_code == 200
    assert response.json()["nome"] == "Paracetamol"

    # 5. Editar medicação (nome e dosagem)
    url = f"/api/medicacoes/{medicacao_id}"
    response = client.put(
        url,
        json={"nome": "Paracetamol Extra", "dosagem": "750mg"},
        headers=auth_header,
    )
    assert response.status_code == 200
    assert response.json()["nome"] == "Paracetamol Extra"
    assert response.json()["dosagem"] == "750mg"

    # 6. Editar apenas dosagem
    url = f"/api/medicacoes/{medicacao_id}"
    response = client.put(
        url,
        json={"dosagem": "1000mg"},
        headers=auth_header,
    )
    assert response.status_code == 200
    assert response.json()["dosagem"] == "1000mg"

    # 7. Excluir medicação
    url = f"/api/medicacoes/{medicacao_id}"
    response = client.delete(url, headers=auth_header)
    assert response.status_code == 204

    # 8. Verificar exclusão
    url = f"/api/medicacoes/{medicacao_id}"
    response = client.get(url, headers=auth_header)
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


@pytest.mark.parametrize(
    "dados_invalidos,campo_erro",
    [
        ({"nome": "A", "dosagem": "500mg"}, "nome"),
        # Nome curto
        ({"nome": "X" * 101, "dosagem": "500mg"}, "nome"),
        # Nome longo
        ({"nome": "Paracetamol", "dosagem": "X" * 101}, "dosagem"),
        # Dosagem longa
    ],
)
def test_validacao_campos(auth_header, client, dados_invalidos, campo_erro):
    """Testa validação de campos."""
    response = client.post(
        "/api/medicacoes/",
        json=dados_invalidos,
        headers=auth_header
    )
    assert response.status_code == 422  # Validation error
    assert campo_erro in str(response.json())


def test_update_medicacao_remove_dosagem(db):
    medic = Medicacao(nome="Naramig", dosagem="800mg", usuario_id=1)
    db.add(medic)
    db.commit()
    db.refresh(medic)

    updated = update_medicacao(db, medic, dosagem=None)
    db.refresh(updated)

    # Forçar uma nova consulta para certificar que valor está salvo
    db.expire_all()
    medic_salvo = db.query(Medicacao).filter_by(id=medic.id).first()

    assert medic_salvo.dosagem is None


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


@pytest.mark.parametrize(
    "novo_nome,nova_dosagem,esperado_nome,esperado_dosagem",
    [
        ("Novo Nome", "100mg", "Novo Nome", "100mg"),
        # atualização normal
        (None, None, "Original", None),
        # sem alteração
        ("Nome Atualizado", None, "Nome Atualizado", None),
        # altera nome, remove dosagem
    ],
)
def test_update_medicacao_parametrizado(db, novo_nome, nova_dosagem,
                                        esperado_nome, esperado_dosagem):
    # Cria medicação inicial
    medic = Medicacao(nome="Original", dosagem="50mg", usuario_id=1)
    db.add(medic)
    db.commit()
    db.refresh(medic)

    updated = update_medicacao(db, medic, nome=novo_nome, dosagem=nova_dosagem)
    db.refresh(updated)

    assert updated is not None
    assert updated.nome == esperado_nome
    assert updated.dosagem == esperado_dosagem


def test_update_medicacao_integrity_error(db):
    medic = Medicacao(nome="Original", dosagem="50mg", usuario_id=1)
    db.add(medic)
    db.commit()
    db.refresh(medic)

    def raise_integrity_error():
        raise IntegrityError("Simulado", None, None)

    original_commit = db.commit
    db.commit = raise_integrity_error

    result = update_medicacao(db, medic, nome="Duplicado", dosagem="25mg")
    assert result is None

    db.commit = original_commit
