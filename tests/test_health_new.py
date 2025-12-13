from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data

def test_detailed_health_check():
    response = client.get("/api/v1/health/detailed")
    # It might return partial if services are down, but should be 200 OK
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["success", "partial", "error"]
    assert "services" in data

def test_system_health_check():
    response = client.get("/api/v1/health/system")
    assert response.status_code == 200
    data = response.json()
    assert "services" in data

def test_agents_health_check():
    response = client.get("/api/v1/health/agents")
    assert response.status_code == 200
    data = response.json()
    assert "services" in data
