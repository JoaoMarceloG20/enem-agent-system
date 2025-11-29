import pytest
from unittest.mock import patch, MagicMock
from app.api.models import StatusEnum

class TestAPI:
    def test_list_agents(self, client):
        response = client.get("/api/v1/agents")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "tutor" in data["agents"]

    def test_get_agents_info(self, client):
        response = client.get("/api/v1/agents/info")
        assert response.status_code == 200
        data = response.json()
        assert "tutor" in data["agents"]
        assert data["agents"]["tutor"]["name"] == "Tutor ENEM"

    def test_orchestrator_chat(self, client, mock_orchestrator_response):
        # Mock the orchestrator response
        mock_orchestrator_response.return_value = {
            "content": "Resposta do Tutor",
            "agent_id": "tutor",
            "metadata": {"routed_to": "tutor"}
        }
        
        payload = {"message": "Ajuda em math", "user_id": "user1"}
        response = client.post("/api/v1/orchestrator/chat", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["response"] == "Resposta do Tutor"
        assert data["agent_id"] == "tutor"

    def test_run_agent_direct(self, client, mock_agent_dependencies):
        # Mock the get_agent call to return a mock agent
        with patch("app.api.routes.agents.get_agent") as mock_get_agent:
            mock_agent_instance = MagicMock()
            mock_agent_instance.run.return_value = MagicMock(content="Resposta direta")
            mock_agent_instance.name = "Tutor Test"
            mock_agent_instance.session_id = "sess1"
            mock_get_agent.return_value = mock_agent_instance
            
            payload = {"message": "Ola", "user_id": "user1"}
            response = client.post("/api/v1/agents/tutor/runs", json=payload)
            
            assert response.status_code == 200
            data = response.json()
            assert data["content"] == "Resposta direta"
            assert data["metadata"]["agent_id"] == "tutor"
