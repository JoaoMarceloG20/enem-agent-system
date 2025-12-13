from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.api.models import StatusEnum

client = TestClient(app)

@patch("app.api.routes.study_plan.get_agent")
def test_get_study_plan_info(mock_get_agent):
    response = client.get("/api/v1/study-plan/info")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "study_intensities" in data
    assert "available_templates" in data

@patch("app.api.routes.study_plan.get_agent")
def test_generate_study_plan(mock_get_agent):
    mock_agent_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Study plan content"
    mock_agent_instance.run.return_value = mock_response
    mock_get_agent.return_value = mock_agent_instance

    payload = {
        "available_hours_per_day": 4,
        "study_days_per_week": 5,
        "target_exam_date": "2024-11-01",
        "study_intensity": "medium",
        "priority_subjects": ["matematica"],
        "student_id": "test_student"
    }

    response = client.post("/api/v1/study-plan/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "weekly_schedules" in data
    assert "subject_distribution" in data

def test_update_progress():
    payload = {
        "plan_id": "plan-123",
        "completed_hours": {"matematica": 5, "portugues": 3},
        "difficulty_feedback": {"matematica": "medium"}
    }
    response = client.put("/api/v1/study-plan/update-progress", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "new_recommendations" in data

def test_get_study_templates():
    response = client.get("/api/v1/study-plan/templates")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["templates"]) > 0
