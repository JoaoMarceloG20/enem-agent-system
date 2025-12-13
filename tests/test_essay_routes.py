from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.api.models import StatusEnum

client = TestClient(app)

@patch("app.api.routes.essay.get_agent")
def test_get_essay_info(mock_get_agent):
    response = client.get("/api/v1/essay/info")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "competencies" in data
    assert "scoring_system" in data

@patch("app.api.routes.essay.get_agent")
def test_grade_essay(mock_get_agent):
    mock_agent_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Essay content feedback"
    mock_agent_instance.run.return_value = mock_response
    mock_get_agent.return_value = mock_agent_instance

    payload = {
        "essay_text": "This is a very long essay text to meet the minimum length requirements. " * 10,
        "theme": "Education",
        "student_id": "test_student"
    }

    response = client.post("/api/v1/essay/grade", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "total_score" in data
    assert "competency_scores" in data

@patch("app.api.routes.essay.get_agent")
def test_grade_essay_detailed(mock_get_agent):
    mock_agent_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Detailed feedback"
    mock_agent_instance.run.return_value = mock_response
    mock_get_agent.return_value = mock_agent_instance

    payload = {
        "essay_text": "This is a very long essay text to meet the minimum length requirements. " * 10,
        "theme": "Education",
        "include_line_by_line": True
    }

    response = client.post("/api/v1/essay/grade-detailed", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "detailed_analysis" in data
    assert "line_by_line_feedback" in data

def test_get_rubric_details():
    response = client.get("/api/v1/essay/rubric-details")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "competencies" in data

def test_get_sample_essays():
    response = client.get("/api/v1/essay/sample-essays?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["essays"]) == 2
