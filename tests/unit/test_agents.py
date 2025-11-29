import pytest
from unittest.mock import MagicMock, patch
from app.agents.tutor_agent import TutorAgent
from app.agents.quiz_agent import QuizAgent
from app.agents.orchestrator_agent import OrchestratorAgent

class TestAgents:
    def test_tutor_agent_initialization(self, mock_agent_dependencies):
        """Test if TutorAgent initializes correctly and loads tools."""
        agent = TutorAgent(subject="matematica")
        
        assert agent.get_agent_type() == "tutor"
        assert agent.get_agent_name() == "Tutor ENEM"
        
        tools = agent.get_agent_tools()
        assert len(tools) > 0
        assert any(t.__name__ == "search_educational_content" for t in tools)

    def test_quiz_agent_initialization(self, mock_agent_dependencies):
        """Test if QuizAgent initializes correctly and loads tools."""
        agent = QuizAgent()
        
        # Default difficulty is 'medio'
        assert agent.get_agent_type() == "quiz_medio"
        
        tools = agent.get_agent_tools()
        assert len(tools) > 0
        assert any(t.__name__ == "save_quiz_result" for t in tools)

    def test_orchestrator_routing_tutor(self, mock_agent_dependencies):
        """Test Orchestrator routing logic for Tutor intent."""
        orchestrator = OrchestratorAgent()
        
        # Mock the classifier agent
        with patch("app.agents.orchestrator_agent.Agent") as mock_agent_cls:
            mock_classifier = MagicMock()
            mock_classifier.run.return_value.content = '{"target_agent": "tutor", "reason": "Math question"}'
            mock_agent_cls.return_value = mock_classifier
            
            # Mock the factory function for tutor agent
            with patch("app.agents.orchestrator_agent.get_tutor_agent") as mock_get_tutor:
                mock_tutor_instance = MagicMock()
                mock_tutor_instance.run.return_value.content = "Tutor response"
                mock_get_tutor.return_value = mock_tutor_instance
                
                response = orchestrator.process_message("Help with math", user_id="u1")
                
                assert response["agent_id"] == "tutor"
                assert response["content"] == "Tutor response"
                assert response["metadata"]["routed_to"] == "tutor"

    def test_orchestrator_initialization(self, mock_agent_dependencies):
        """Test OrchestratorAgent initialization."""
        agent = OrchestratorAgent()
        assert agent.get_agent_type() == "orchestrator"
        # Orchestrator doesn't have tools in get_agent_tools currently
        assert len(agent.get_agent_tools()) == 0
