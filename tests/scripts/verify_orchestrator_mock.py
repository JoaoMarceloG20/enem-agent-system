
import sys
import os
from unittest.mock import MagicMock, patch

# Add app to path
sys.path.append(os.getcwd())

# Mock agno and google to avoid real API calls during basic logic test
# We want to verify routing logic, not the LLM itself for this quick check
# However, the routing logic USES the LLM. 
# So we will mock the Agent.run method to return specific JSONs for classification.

# Ensure modules are loaded
import app.agents.orchestrator_agent

import app.agents.orchestrator_agent

# Mock DB components to avoid connection errors
with patch('app.agents.base_enem_agent.PostgresAgentStorage') as MockStorage, \
     patch('app.agents.base_enem_agent.PostgresMemoryDb') as MockMemoryDb, \
     patch('app.agents.base_enem_agent.Memory') as MockMemory, \
     patch('app.agents.orchestrator_agent.Agent') as MockAgent:
    from app.agents.orchestrator_agent import OrchestratorAgent
    
    # Setup mock for classifier
    mock_classifier_instance = MagicMock()
    MockAgent.return_value = mock_classifier_instance
    
    # Test 1: Tutor Routing
    print("Testing Tutor Routing...")
    mock_classifier_instance.run.return_value.content = '{"target_agent": "tutor", "reason": "Math question"}'
    
    # Mock the specialized agent factory and instance
    with patch('app.agents.orchestrator_agent.get_tutor_agent') as mock_get_tutor:
        mock_tutor_instance = MagicMock()
        mock_get_tutor.return_value = mock_tutor_instance
        mock_tutor_instance.run.return_value.content = "Bhaskara explanation..."
        
        orchestrator = OrchestratorAgent()
        result = orchestrator.process_message("Explique Bhaskara")
        
        print(f"Result: {result}")
        assert result['agent_id'] == 'tutor'
        assert result['content'] == "Bhaskara explanation..."
        print("Tutor Routing: PASS")

    # Test 2: Quiz Routing
    print("\nTesting Quiz Routing...")
    mock_classifier_instance.run.return_value.content = '{"target_agent": "quiz", "reason": "Quiz request"}'
    
    with patch('app.agents.orchestrator_agent.get_quiz_agent') as mock_get_quiz:
        mock_quiz_instance = MagicMock()
        mock_get_quiz.return_value = mock_quiz_instance
        mock_quiz_instance.run.return_value.content = "Question 1..."
        
        result = orchestrator.process_message("Crie um quiz")
        
        print(f"Result: {result}")
        assert result['agent_id'] == 'quiz'
        assert result['content'] == "Question 1..."
        print("Quiz Routing: PASS")

print("\nAll verification tests passed!")
