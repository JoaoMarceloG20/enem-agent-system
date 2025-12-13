from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.api.models import StatusEnum

client = TestClient(app)

def test_list_agents():
    # This route uses a simple list of strings, so we can test it directly
    # assuming get_available_agents() is deterministic or we patch it
    with patch("app.api.routes.agents.get_available_agents") as mock_get_agents:
        mock_get_agents.return_value = ["tutor", "quiz"]
        response = client.get("/api/v1/agents")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert len(data["agents"]) == 2

def test_get_agents_info():
    with patch("app.api.routes.agents.get_all_agents_info") as mock_get_info:
        mock_get_info.return_value = {
            "tutor": {"name": "Tutor", "description": "Tutor Agent"},
            "quiz": {"name": "Quiz", "description": "Quiz Agent"}
        }
        response = client.get("/api/v1/agents/info")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "tutor" in data["agents"]

def test_get_supported_subjects_agents():
    response = client.get("/api/v1/agents/subjects")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["subjects"]) > 0

@patch("app.api.routes.agents.get_agent")
def test_create_agent(mock_get_agent):
    mock_agent = MagicMock()
    mock_agent.name = "Test Agent"
    mock_get_agent.return_value = mock_agent

    payload = {
        "agent_id": "tutor",
        "subject": "matematica",
        "user_id": "user123"
    }
    response = client.post("/api/v1/agents/create", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["agent_id"] == "tutor"

@patch("app.api.routes.agents.get_agent")
def test_run_agent(mock_get_agent):
    mock_agent = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Agent response"
    mock_agent.run.return_value = mock_response
    mock_agent.name = "Tutor Agent"
    mock_agent.session_id = "session-123"
    mock_get_agent.return_value = mock_agent

    payload = {
        "message": "Hello",
        "user_id": "user123"
    }
    response = client.post("/api/v1/agents/tutor/runs", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["content"] == "Agent response"
