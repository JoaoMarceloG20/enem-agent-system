"""
Base ENEM Agent Module

This module provides the abstract base class for all ENEM agents,
following the exact same patterns as dr_ubyfol for consistency.
"""

from abc import ABC, abstractmethod
from textwrap import dedent
from typing import Optional, Dict, Any, List
from pathlib import Path

from agno.agent import Agent, AgentKnowledge
from agno.models.google import Gemini
from agno.storage.agent.postgres import PostgresAgentStorage
from agno.memory.v2.memory import Memory
from agno.memory.v2.db.postgres import PostgresMemoryDb
from agno.tools.reasoning import ReasoningTools

from app.core.config import settings
from app.agents.knowledge import get_enem_knowledge_base, get_subject_knowledge


class BaseENEMAgent(ABC):
    """
    Abstract base class for all ENEM agents.
    
    Follows the exact same patterns as dr_ubyfol to ensure consistency
    and compatibility with the Agno framework.
    """
    
    @abstractmethod
    def get_agent_type(self) -> str:
        """
        Return the unique identifier for this agent type.
        
        Returns:
            str: Agent type identifier (e.g., 'tutor', 'quiz', 'essay_grader')
        """
        pass
    
    @abstractmethod
    def get_agent_name(self) -> str:
        """
        Return the display name for this agent.
        
        Returns:
            str: Human-readable agent name
        """
        pass
    
    @abstractmethod
    def get_agent_description(self) -> str:
        """
        Return the agent description for the Agno Agent.
        
        Returns:
            str: Agent description (should use dedent for formatting)
        """
        pass
    
    @abstractmethod
    def get_agent_instructions(self) -> str:
        """
        Return the detailed instructions for this agent.
        
        Returns:
            str: Agent instructions (should use dedent for formatting)
        """
        pass
    
    @abstractmethod
    def get_agent_tools(self) -> List[Any]:
        """
        Return agent-specific tools beyond ReasoningTools.
        
        Returns:
            List[Any]: List of agent-specific tools
        """
        pass
    
    def get_agent_knowledge(self, subject: Optional[str] = None) -> Optional[AgentKnowledge]:
        """
        Get knowledge base for this agent.
        
        Args:
            subject: Specific ENEM subject if applicable
            
        Returns:
            AgentKnowledge or None if no knowledge base needed
        """
        try:
            if subject:
                return get_subject_knowledge(subject)
            else:
                return get_enem_knowledge_base()
        except Exception as e:
            # Return None if knowledge base is not available yet
            # This allows agents to work without PDFs during development
            print(f"Warning: Knowledge base not available - {e}")
            return None
    
    def get_agent_temperature(self) -> float:
        """
        Get the temperature setting for this agent's model.
        
        Returns:
            float: Temperature value (can be overridden by subclasses)
        """
        return 0.7  # Default balanced temperature
    
    def get_max_output_tokens(self) -> int:
        """
        Get the maximum output tokens for this agent.
        
        Returns:
            int: Maximum output tokens (can be overridden by subclasses)
        """
        return 2048  # Default reasonable limit
    
    def get_agent_storage_table_name(self) -> str:
        """
        Get the PostgreSQL table name for this agent's storage.
        
        Returns:
            str: Table name for PostgresAgentStorage
        """
        return f'enem_{self.get_agent_type()}_sessions'
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check for this agent.
        
        Returns:
            Dict with health status information
        """
        try:
            # Check Google API Key
            api_key_status = bool(settings.GOOGLE_API_KEY)
            
            # Check database connection
            from app.core.db import engine
            with engine.connect() as conn:
                db_status = True
        except Exception:
            db_status = False
        
        # Check Qdrant connection
        try:
            from app.core.qdrant import get_qdrant_client
            client = get_qdrant_client()
            client.get_collections()
            qdrant_status = True
        except Exception:
            qdrant_status = False
        
        return {
            'agent_type': self.get_agent_type(),
            'agent_name': self.get_agent_name(),
            'google_api_key': api_key_status,
            'database': db_status,
            'qdrant': qdrant_status,
            'healthy': all([api_key_status, db_status, qdrant_status])
        }
    
    def get_agent(
        self,
        model_id: str = settings.gemini_model,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        debug_mode: bool = False,
        subject: Optional[str] = None,
    ) -> Agent:
        """
        Create an Agent instance following the exact dr_ubyfol pattern.
        
        Args:
            model_id: Gemini model ID to use
            user_id: Optional user ID for personalization
            session_id: Optional session ID for conversation continuity
            debug_mode: Enable debug logging
            subject: Optional ENEM subject for specialized knowledge
            
        Returns:
            Configured Agent instance
        """
        # Get agent-specific tools and combine with ReasoningTools
        agent_tools = []
        agent_tools.extend(self.get_agent_tools())
        
        # Get knowledge base (optional during development)
        knowledge = self.get_agent_knowledge(subject)
        
        return Agent(
            # Basic agent configuration
            name=self.get_agent_name(),
            agent_id=self.get_agent_type(),
            user_id=user_id,
            session_id=session_id,
            
            # Model configuration
            model=Gemini(
                id=model_id, 
                api_key=settings.GOOGLE_API_KEY,
                temperature=self.get_agent_temperature(),
                max_output_tokens=self.get_max_output_tokens(),
            ),
            
            # Tools and capabilities
            tools=agent_tools,
            
            # Agent behavior
            description=self.get_agent_description(),
            instructions=self.get_agent_instructions(),
            
            # State management (following dr_ubyfol pattern)
            add_state_in_messages=True,
            
            # Knowledge base (optional)
            knowledge=knowledge,
            search_knowledge=knowledge is not None,
            
            # Storage for chat history (following dr_ubyfol pattern)
            storage=PostgresAgentStorage(
                table_name=self.get_agent_storage_table_name(),
                db_url=settings.SQLALCHEMY_DATABASE_URI,
            ),
            
            # Chat history management (following dr_ubyfol pattern)
            add_history_to_messages=True,
            num_history_runs=3,
            read_chat_history=True,
            
            # Agentic memory for personalization (following dr_ubyfol pattern)
            memory=Memory(
                model=Gemini(id=model_id, api_key=settings.GOOGLE_API_KEY),
                db=PostgresMemoryDb(
                    table_name='user_memories',
                    db_url=settings.SQLALCHEMY_DATABASE_URI,
                ),
                delete_memories=True,
                clear_memories=True,
            ),
            enable_agentic_memory=True,
            
            # Response formatting (following dr_ubyfol pattern)
            markdown=True,
            add_datetime_to_instructions=False,
            
            # Debug configuration
            debug_mode=debug_mode,
        )


def get_agent_health_status() -> Dict[str, Any]:
    """
    Get health status for all available ENEM agents.
    
    Returns:
        Dict with health status for each agent type
    """
    # This will be populated as agents are implemented
    agent_classes = {}
    
    # Import and register agents
    try:
        from .tutor_agent import TutorAgent
        from .quiz_agent import QuizAgent
        from .essay_grader_agent import EssayGraderAgent
        from .study_plan_agent import StudyPlanAgent
        from .orchestrator_agent import OrchestratorAgent
        
        agent_classes = {
            'tutor': TutorAgent(),
            'quiz': QuizAgent(),
            'essay_grader': EssayGraderAgent(),
            'study_plan': StudyPlanAgent(),
            'orchestrator': OrchestratorAgent(),
        }
    except ImportError as e:
        print(f"Error importing agents for health check: {e}")
        agent_classes = {}
    
    health_status = {
        'system': {
            'database': True,  # Will be checked in each agent
            'qdrant': True,    # Will be checked in each agent
            'google_api': bool(settings.GOOGLE_API_KEY),
        },
        'agents': {}
    }
    
    for agent_id, agent_instance in agent_classes.items():
        health_status['agents'][agent_id] = agent_instance.health_check()
    
    # Overall system health
    health_status['system']['healthy'] = all([
        health_status['system']['database'],
        health_status['system']['qdrant'], 
        health_status['system']['google_api'],
    ])
    
    return health_status