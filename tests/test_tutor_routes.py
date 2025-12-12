from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.api.models import SubjectEnum

client = TestClient(app)

@patch("app.api.routes.tutor.get_agent")
def test_get_tutor_info(mock_get_agent):
    response = client.get("/api/v1/tutor/info")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "supported_subjects" in data
    assert "capabilities" in data

@patch("app.api.routes.tutor.get_agent")
def test_chat_with_tutor(mock_get_agent):
    mock_agent_instance = MagicMock()
    # Simulate agent response
    mock_response = MagicMock()
    mock_response.content = "This is the tutor explaining something about Math."
    mock_agent_instance.run.return_value = mock_response
    mock_agent_instance.name = "TutorAgent"
    mock_get_agent.return_value = mock_agent_instance

    payload = {
        "message": "Explain Pythagorean theorem",
        "subject": "matematica",
        "user_id": "test_user"
    }

    response = client.post("/api/v1/tutor/chat", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["content"] == "This is the tutor explaining something about Math."
    # Check if helper functions populated fields
    assert "explanation_type" in data

@patch("app.api.routes.tutor.get_agent")
def test_get_subject_tree(mock_get_agent):
    response = client.get("/api/v1/tutor/subjects/matematica/tree")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["subject"] == "matematica"
    assert "topics" in data

@patch("app.api.routes.tutor.get_agent")
def test_get_learning_path(mock_get_agent):
    response = client.get("/api/v1/tutor/learning-path/matematica?current_level=basic")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["subject"] == "matematica"
    assert "recommended_path" in data

@patch("app.api.routes.tutor.get_agent")
def test_get_supported_subjects(mock_get_agent):
    response = client.get("/api/v1/tutor/subjects")
    assert response.status_code == 200
    data = response.json()
    assert len(data["subjects"]) > 0
