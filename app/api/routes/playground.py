from agno.playground import Playground
from fastapi import APIRouter

from app.agents.test_agent import get_test_enem_agent
from app.agents.tutor_agent import get_tutor_agent
from app.agents.quiz_agent import get_quiz_agent

# Get Agents to serve in the playground  
test_agent = get_test_enem_agent(debug_mode=True)
tutor_agent = get_tutor_agent(debug_mode=True)
quiz_agent = get_quiz_agent(difficulty='medio', debug_mode=True)

# Create a playground instance with available agents
playground = Playground(agents=[test_agent, tutor_agent, quiz_agent])

# Get the router for the playground
router = playground.get_async_router()
