"""
Teste básico de health check.
"""

def test_health_check(client):
    """Testa endpoint de health check."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root(client):
    """Testa endpoint root."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Diário de Enxaqueca API"
