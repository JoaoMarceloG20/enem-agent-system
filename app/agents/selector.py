from enum import Enum
from typing import Optional

from agno.agent import Agent

# Import implemented agent functions
from .test_agent import get_test_enem_agent
from .tutor_agent import get_tutor_agent
from .quiz_agent import get_quiz_agent
from .essay_grader_agent import get_essay_grader_agent
from .study_plan_agent import get_study_plan_agent
from .orchestrator_agent import get_orchestrator_agent

class AgentType(str, Enum):
    """Available ENEM agent types"""
    TEST = 'test_enem'
    TUTOR = 'tutor'
    QUIZ = 'quiz'
    ESSAY = 'essay_grader'
    STUDY_PLAN = 'study_plan'
    ORCHESTRATOR = 'orchestrator'


def get_agent(
    agent_id: AgentType,
    model_id: str = 'gemini-2.5-flash',
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = True,
    subject: Optional[str] = None,
    difficulty: Optional[str] = None,
    intensity: Optional[str] = None,
    **kwargs
) -> Agent:
    """
    Factory function to get agent instances.
    
    Args:
        agent_id: The type of agent to create
        model_id: The model ID to use (default: gemini-2.5-flash)
        user_id: Optional user ID for personalization
        session_id: Optional session ID for conversation continuity
        debug_mode: Enable debug logging
        subject: Optional subject for specialized agents (e.g., 'matematica')
        difficulty: Optional difficulty level for quiz agent ('facil', 'medio', 'dificil')
        intensity: Optional intensity level for study plan agent ('light', 'moderate', 'intensive', 'extreme')
        **kwargs: Additional parameters passed to agent factory
        
    Returns:
        Agent instance
        
    Raises:
        ValueError: If agent_id is not supported
    """
    
    # Implemented agents
    if agent_id == AgentType.TEST:
        return get_test_enem_agent(
            model_id=model_id,
            user_id=user_id,
            session_id=session_id,
            debug_mode=debug_mode,
            **kwargs
        )
    elif agent_id == AgentType.TUTOR:
        return get_tutor_agent(
            subject=subject,
            model_id=model_id,
            user_id=user_id,
            session_id=session_id,
            debug_mode=debug_mode,
            **kwargs
        )
    elif agent_id == AgentType.QUIZ:
        return get_quiz_agent(
            subject=subject,
            difficulty=difficulty or 'medio',
            model_id=model_id,
            user_id=user_id,
            session_id=session_id,
            debug_mode=debug_mode,
            **kwargs
        )
    elif agent_id == AgentType.ESSAY:
        return get_essay_grader_agent(
            model_id=model_id,
            user_id=user_id,
            session_id=session_id,
            debug_mode=debug_mode,
            **kwargs
        )
    elif agent_id == AgentType.STUDY_PLAN:
        return get_study_plan_agent(
            intensity=intensity or 'moderate',
            model_id=model_id,
            user_id=user_id,
            session_id=session_id,
            debug_mode=debug_mode,
            **kwargs
        )
    elif agent_id == AgentType.ORCHESTRATOR:
        return get_orchestrator_agent(
            model_id=model_id,
            user_id=user_id,
            session_id=session_id,
            debug_mode=debug_mode,
            **kwargs
        )
    
    raise ValueError(f"Agent type '{agent_id}' is not yet implemented")


def get_available_agents() -> list[str]:
    """
    Get list of available agent IDs.
    
    Returns:
        List of agent identifiers
    """
    return [agent.value for agent in AgentType]


def get_agent_info(agent_id: AgentType) -> dict:
    """
    Get information about a specific agent type.
    
    Args:
        agent_id: The agent type to get info for
        
    Returns:
        Dictionary with agent information
    """
    agent_info = {
        AgentType.TEST: {
            "name": "Test ENEM Agent",
            "description": "Agent de teste para validação do sistema ENEM",
            "supports_subject": False,
            "supports_difficulty": False,
            "temperature": 0.5,
            "max_tokens": 1024
        },
        AgentType.TUTOR: {
            "name": "Tutor ENEM",
            "description": "Tutor educacional especializado em preparação para ENEM",
            "supports_subject": True,
            "supports_difficulty": False,
            "temperature": 0.7,
            "max_tokens": 2048,
            "subjects": [
                "matematica", "portugues", "literatura", "ingles", "espanhol",
                "fisica", "quimica", "biologia", "historia", "geografia", 
                "filosofia", "sociologia", "redacao"
            ]
        },
        AgentType.QUIZ: {
            "name": "Quiz ENEM",
            "description": "Gerador e avaliador de quizzes estilo ENEM",
            "supports_subject": True,
            "supports_difficulty": True,
            "temperature": 0.4,
            "max_tokens": 3000,
            "subjects": [
                "matematica", "portugues", "literatura", "ingles", "espanhol",
                "fisica", "quimica", "biologia", "historia", "geografia", 
                "filosofia", "sociologia", "redacao"
            ],
            "difficulties": ["facil", "medio", "dificil"]
        },
        AgentType.ESSAY: {
            "name": "Corretor de Redação ENEM",
            "description": "Corretor automático de redações baseado nos critérios oficiais do ENEM",
            "supports_subject": False,
            "supports_difficulty": False,
            "temperature": 0.2,
            "max_tokens": 4000,
            "competencies": [
                "Domínio da norma padrão da língua escrita",
                "Compreender a proposta e aplicar conceitos",
                "Seleção e organização das informações", 
                "Coesão e coerência",
                "Proposta de intervenção"
            ]
        },
        AgentType.STUDY_PLAN: {
            "name": "Plano de Estudos ENEM",
            "description": "Criação de planos de estudo personalizados e adaptativos para o ENEM",
            "supports_subject": False,
            "supports_difficulty": False,
            "supports_intensity": True,
            "temperature": 0.3,
            "max_tokens": 3000,
            "intensities": ["light", "moderate", "intensive", "extreme"],
            "features": [
                "Distribuição inteligente de horas por matéria",
                "Cronogramas semanais detalhados",
                "Sistema de marcos e milestones",
                "Adaptação baseada em performance",
                "Múltiplos níveis de intensidade"
            ]
        },
        AgentType.ORCHESTRATOR: {
            "name": "Orchestrator ENEM",
            "description": "Coordenador central que gerencia todos os agentes e roteia mensagens",
            "supports_subject": False,
            "supports_difficulty": False,
            "supports_intensity": False,
            "temperature": 0.1,
            "max_tokens": 1500,
            "features": [
                "Roteamento inteligente de mensagens",
                "Gerenciamento de sessões ativas",
                "Health checks de todos os agentes",
                "Sistema de comandos integrado",
                "Broadcasting de mensagens",
                "Cleanup automático de sessões"
            ],
            "commands": [
                "/help", "/status", "/agents", "/sessions", "/health",
                "/switch <agent>", "/session new", "/session end"
            ],
            "managed_agents": ["tutor", "quiz", "essay", "study_plan"]
        }
    }
    
    return agent_info.get(agent_id, {})


def get_all_agents_info() -> dict:
    """
    Get information about all available agents.
    
    Returns:
        Dictionary with all agent information
    """
    return {agent.value: get_agent_info(agent) for agent in AgentType}