from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.api.models import StatusEnum

client = TestClient(app)

@patch("app.api.routes.orchestrator.get_orchestrator_agent")
def test_chat_with_orchestrator(mock_get_orchestrator):
    mock_orchestrator = MagicMock()
    mock_orchestrator.process_message.return_value = {
        "content": "Routed response",
        "agent_id": "study_plan",
        "metadata": {"routed": True}
    }
    mock_get_orchestrator.return_value = mock_orchestrator

    payload = {
        "message": "I need a study plan",
        "user_id": "user123"
    }

    response = client.post("/api/v1/orchestrator/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["agent_id"] == "study_plan"
    assert data["response"] == "Routed response"

def test_get_orchestrator_info():
    response = client.get("/api/v1/orchestrator/info")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "capabilities" in data
