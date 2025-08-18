# ENEM Agents Module
# This module contains all the AI agents for ENEM preparation

from typing import Dict, Any, Type
from agno.agent import Agent

# Agent registry will be populated as agents are implemented
AGENT_REGISTRY: Dict[str, Type[Agent]] = {}

def register_agent(agent_id: str, agent_class: Type[Agent]) -> None:
    """Register an agent in the global registry."""
    AGENT_REGISTRY[agent_id] = agent_class

def get_agent(agent_id: str, **kwargs) -> Agent:
    """Get an agent instance by ID."""
    if agent_id not in AGENT_REGISTRY:
        raise ValueError(f"Agent '{agent_id}' not found in registry")
    
    agent_class = AGENT_REGISTRY[agent_id]
    return agent_class(**kwargs)

def list_agents() -> Dict[str, str]:
    """List all registered agents."""
    return {agent_id: agent_class.__name__ for agent_id, agent_class in AGENT_REGISTRY.items()}