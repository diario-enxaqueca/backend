# import pytest

# @pytest.mark.skip(reason="Teste skipado apenas para primeira entrega")
# def test_criar_episodio():
#     assert True


import pytest
from fastapi.testclient import TestClient
from main import app  # certifique-se que o app FastAPI está em main.py

client = TestClient(app)

@pytest.mark.skip(reason="Desabilitado até o banco estar configurado para testes")
def test_criar_episodio():
    response = client.post(
        "/episodios/",
        params={"usuario_id": 1, "data": "2025-09-28", "intensidade": 7, "observacoes": "Dor moderada"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["usuario_id"] == 1
    assert body["intensidade"] == 7
