from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app
from app.api.models import SubjectEnum, DifficultyEnum

client = TestClient(app)

@patch("app.api.routes.quiz.get_agent")
def test_get_quiz_info(mock_get_agent):
    response = client.get("/api/v1/quiz/info")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "supported_subjects" in data
    assert "difficulty_levels" in data

@patch("app.api.routes.quiz.get_agent")
def test_generate_quiz_success(mock_get_agent):
    # Mock the agent and its run method
    mock_agent_instance = MagicMock()
    # Mock return value that mimics the structure expected by parse_quiz_content
    # It needs to return a string that the parser can handle
    mock_content = """
    Here is the quiz:

    ## Questão 1
    **Contexto:** This is a context.
    **Comando:** Calculate 1+1.
    A) 1
    B) 2
    C) 3
    D) 4
    E) 5
    **Gabarito:** B
    **Explicação:** 1+1=2
    **Tópico:** Basic Math
    **Dificuldade:** facil

    ## Questão 2
    **Contexto:** Another context.
    **Comando:** Calculate 2+2.
    A) 2
    B) 3
    C) 4
    D) 5
    E) 6
    **Gabarito:** C
    **Explicação:** 2+2=4
    **Tópico:** Basic Math
    **Dificuldade:** facil
    """

    # The agent.run return value acts like an object with .content
    mock_response = MagicMock()
    mock_response.content = mock_content
    mock_agent_instance.run.return_value = mock_response
    mock_agent_instance.name = "QuizAgent"

    mock_get_agent.return_value = mock_agent_instance

    payload = {
        "subject": "matematica",
        "difficulty": "facil",
        "num_questions": 2,
        "topics": ["Basic Math"]
    }

    response = client.post("/api/v1/quiz/generate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["questions"]) == 2
    assert data["total_questions"] == 2

@patch("app.api.routes.quiz.get_agent")
def test_quick_generate_success(mock_get_agent):
    mock_agent_instance = MagicMock()
    mock_content = """
    ## Questão 1
    **Contexto:** Quick context.
    **Comando:** Quick question?
    A) Yes
    B) No
    C) Maybe
    D) Dunno
    E) All
    **Gabarito:** A
    **Explicação:** Because yes.
    **Tópico:** Quick Topic
    **Dificuldade:** medio
    """
    mock_response = MagicMock()
    mock_response.content = mock_content
    mock_agent_instance.run.return_value = mock_response
    mock_get_agent.return_value = mock_agent_instance

    response = client.get("/api/v1/quiz/quick-generate?subject=matematica&difficulty=medio")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["question"]["command"] == "Quick question?"

def test_submit_quiz():
    payload = {
        "quiz_id": "some-id",
        "answers": {
            "q_1": "A",
            "q_2": "B"
        },
        "time_taken": 120
    }
    response = client.post("/api/v1/quiz/submit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["grade"] in ["Excelente", "Bom", "Regular", "Precisa melhorar"]

def test_get_subject_topics():
    response = client.get("/api/v1/quiz/topics/matematica")
    assert response.status_code == 200
    data = response.json()
    assert "topics" in data
    assert len(data["topics"]) > 0

def test_get_difficulty_levels():
    response = client.get("/api/v1/quiz/difficulties")
    assert response.status_code == 200
    data = response.json()
    assert len(data["difficulties"]) > 0
