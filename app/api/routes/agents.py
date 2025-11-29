"""
Agent API Routes

Rotas FastAPI para interação com os agents ENEM.
Agora com response models estruturados usando Pydantic.
"""

import time
import uuid
from datetime import datetime
from logging import getLogger
from typing import List, Optional, Union

from agno.agent import Agent
from fastapi import APIRouter, HTTPException, status
from app.core.config import settings

from app.agents.selector import get_agent, get_available_agents, get_all_agents_info
from app.api.models import (
    # Request models
    AgentCreationRequest,
    AgentRunRequest,
    
    # Response models
    AgentListResponse,
    AgentInfoResponse,
    AgentCreationResponse,
    AgentRunResponse,
    AgentRunMetadata,
    QuizResponse,
    EssayGradeResponse,
    StudyPlanResponse,
    TutorResponse,
    SubjectListResponse,
    TopicListResponse,
    DifficultyListResponse,
    IntensityListResponse,
    
    # Enums
    AgentTypeEnum,
    StatusEnum
)

logger = getLogger(__name__)

router = APIRouter()


@router.get('', response_model=AgentListResponse)
async def list_agents():
    """
    Lista todos os IDs de agentes disponíveis no sistema.

    Returns:
        AgentListResponse: Lista de identificadores de agentes.
    
    Example:
        ```json
        {
            "status": "success",
            "message": "Agents retrieved successfully",
            "agents": ["tutor", "quiz", "essay_grader", "study_plan"],
            "total_count": 4
        }
        ```
    """
    try:
        agents = get_available_agents()
        return AgentListResponse(
            status=StatusEnum.SUCCESS,
            message="Agents retrieved successfully",
            agents=agents,
            total_count=len(agents)
        )
    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get('/info', response_model=AgentInfoResponse)
async def get_agents_info():
    """
    Retorna informações detalhadas sobre todos os agentes disponíveis.
    
    Inclui capacidades, parâmetros suportados e descrições.
    
    Returns:
        AgentInfoResponse: Detalhes completos de cada agente.
    """
    try:
        from app.api.models import AgentInfo
        
        agents_info = get_all_agents_info()
        structured_agents = {}
        
        for agent_id, info in agents_info.items():
            structured_agents[agent_id] = AgentInfo(
                agent_id=agent_id,
                name=info.get('name', ''),
                description=info.get('description', ''),
                supports_subject=info.get('supports_subject', False),
                supports_difficulty=info.get('supports_difficulty', False),
                supports_intensity=info.get('supports_intensity', False),
                temperature=info.get('temperature', 0.7),
                max_tokens=info.get('max_tokens', 2048),
                subjects=info.get('subjects'),
                difficulties=info.get('difficulties'),
                intensities=info.get('intensities'),
                features=info.get('features')
            )
        
        return AgentInfoResponse(
            status=StatusEnum.SUCCESS,
            message="Agent information retrieved successfully",
            agents=structured_agents
        )
    except Exception as e:
        logger.error(f"Error getting agents info: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get('/subjects', response_model=SubjectListResponse)
async def get_supported_subjects():
    """
    Retorna a lista de matérias suportadas pelos agentes ENEM.
    
    Útil para popular dropdowns no frontend.
    
    Returns:
        SubjectListResponse: Lista de matérias com chaves e nomes de exibição.
    """
    try:
        from app.agents.tutor_agent import TutorAgent
        
        subjects_data = []
        for key, name in TutorAgent.ENEM_SUBJECTS.items():
            subjects_data.append({
                "key": key,
                "name": name
            })
        
        return SubjectListResponse(
            status=StatusEnum.SUCCESS,
            message="Subjects retrieved successfully",
            subjects=subjects_data
        )
    except Exception as e:
        logger.error(f"Error getting subjects: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get('/quiz/topics', response_model=TopicListResponse)
async def get_quiz_topics(subject: Optional[str] = None):
    """
    Retorna tópicos disponíveis para geração de quiz, filtrados por matéria.
    
    Args:
        subject: Filtro opcional de matéria (ex: 'matematica')
    
    Returns:
        TopicListResponse: Lista de tópicos.
    """
    try:
        from app.agents.quiz_agent import QuizAgent
        
        if subject:
            if subject not in QuizAgent.ENEM_TOPICS:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Subject '{subject}' not found"
                )
            
            return TopicListResponse(
                status=StatusEnum.SUCCESS,
                message=f"Topics for {subject} retrieved successfully",
                subject=subject,
                topics=QuizAgent.ENEM_TOPICS[subject]
            )
        else:
            # Return all topics
            all_topics = []
            for subj_topics in QuizAgent.ENEM_TOPICS.values():
                all_topics.extend(subj_topics)
            
            return TopicListResponse(
                status=StatusEnum.SUCCESS,
                message="All topics retrieved successfully",
                subject="all",
                topics=list(set(all_topics))  # Remove duplicates
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting quiz topics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get('/quiz/difficulties', response_model=DifficultyListResponse)
async def get_quiz_difficulties():
    """
    Retorna os níveis de dificuldade disponíveis para quizzes.
    
    Returns:
        DifficultyListResponse: Lista de dificuldades (facil, medio, dificil).
    """
    try:
        from app.agents.quiz_agent import QuizAgent
        
        difficulties_data = []
        for key, info in QuizAgent.DIFFICULTY_LEVELS.items():
            difficulties_data.append({
                "key": key,
                "description": info.get('description', key)
            })
        
        return DifficultyListResponse(
            status=StatusEnum.SUCCESS,
            message="Difficulties retrieved successfully",
            difficulties=difficulties_data
        )
    except Exception as e:
        logger.error(f"Error getting difficulties: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get('/study/intensities', response_model=IntensityListResponse)
async def get_study_intensities():
    """
    Retorna os níveis de intensidade disponíveis para planos de estudo.
    
    Returns:
        IntensityListResponse: Lista de intensidades (light, moderate, intensive, extreme).
    """
    try:
        from app.agents.study_plan_agent import StudyPlanAgent
        
        intensities_data = []
        for key, info in StudyPlanAgent.INTENSITY_LEVELS.items():
            intensities_data.append({
                "key": key,
                "description": info.get('description', key)
            })
        
        return IntensityListResponse(
            status=StatusEnum.SUCCESS,
            message="Study intensities retrieved successfully",
            intensities=intensities_data
        )
    except Exception as e:
        logger.error(f"Error getting intensities: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post('/create', response_model=AgentCreationResponse)
async def create_agent_instance(body: AgentCreationRequest):
    """
    Cria uma instância de agente e retorna sua configuração.
    
    Args:
        body: Parâmetros de criação do agente.
        
    Returns:
        AgentCreationResponse: Detalhes do agente criado.
    """
    try:
        # Generate session ID if not provided
        session_id = body.session_id or str(uuid.uuid4())
        
        # Create the agent
        agent = get_agent(
            agent_id=body.agent_id,
            model_id=settings.gemini_model,
            user_id=body.user_id,
            session_id=session_id,
            debug_mode=body.debug_mode,
            subject=body.subject,
            difficulty=body.difficulty,
            intensity=body.intensity
        )
        
        # Build configuration dict
        configuration = {
            "agent_id": body.agent_id,
            "model": settings.gemini_model,
            "user_id": body.user_id,
            "debug_mode": body.debug_mode
        }
        
        if body.subject:
            configuration["subject"] = body.subject
        if body.difficulty:
            configuration["difficulty"] = body.difficulty
        if body.intensity:
            configuration["intensity"] = body.intensity
        
        return AgentCreationResponse(
            status=StatusEnum.SUCCESS,
            message=f"Agent '{body.agent_id}' created successfully",
            agent_id=body.agent_id,
            agent_name=agent.name,
            session_id=session_id,
            configuration=configuration
        )
        
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create agent: {str(e)}"
        )


def _create_agent_run_response(
    agent: Agent, 
    content: str, 
    session_id: str,
    processing_time_ms: int,
    agent_type: str,
    subject: Optional[str] = None,
    difficulty: Optional[str] = None,
    intensity: Optional[str] = None
) -> Union[AgentRunResponse, QuizResponse, EssayGradeResponse, StudyPlanResponse, TutorResponse]:
    """
    Creates appropriate response model based on agent type.
    """
    # Base metadata
    metadata = AgentRunMetadata(
        agent_id=agent_type,
        agent_name=agent.name,
        model_used=settings.gemini_model,
        temperature=0.7,  # Default, could be extracted from agent
        max_tokens=2048,  # Default, could be extracted from agent
        processing_time_ms=processing_time_ms,
        subject=subject,
        difficulty=difficulty,
        intensity=intensity
    )
    
    # Base response data
    base_data = {
        "status": StatusEnum.SUCCESS,
        "message": f"Agent '{agent_type}' executed successfully",
        "content": content,
        "metadata": metadata,
        "session_id": session_id,
        "run_id": str(uuid.uuid4())
    }
    
    # Return specialized response based on agent type
    if agent_type == AgentTypeEnum.QUIZ:
        return QuizResponse(**base_data)
    elif agent_type == AgentTypeEnum.ESSAY:
        return EssayGradeResponse(**base_data)
    elif agent_type == AgentTypeEnum.STUDY_PLAN:
        return StudyPlanResponse(**base_data)
    elif agent_type == AgentTypeEnum.TUTOR:
        return TutorResponse(**base_data)
    else:
        return AgentRunResponse(**base_data)


@router.post('/{agent_id}/runs', response_model=Union[AgentRunResponse, QuizResponse, EssayGradeResponse, StudyPlanResponse, TutorResponse])
async def run_agent(
    agent_id: AgentTypeEnum, 
    body: AgentRunRequest,
    subject: Optional[str] = None,
    difficulty: Optional[str] = None,
    intensity: Optional[str] = None
):
    """
    Executa um agente específico com uma mensagem.
    
    Este endpoint permite interagir diretamente com um agente (Tutor, Quiz, etc) sem passar pelo orquestrador.
    
    Args:
        agent_id: Tipo de agente (tutor, quiz, essay_grader, study_plan)
        body: Corpo da requisição contendo a mensagem
        subject: (Opcional) Matéria específica
        difficulty: (Opcional) Nível de dificuldade
        intensity: (Opcional) Intensidade do plano de estudos
        
    Returns:
        Resposta estruturada dependendo do tipo de agente.
        
    Example:
        POST /api/v1/agents/tutor/runs
        {
            "message": "Explique a fórmula de Bhaskara",
            "session_id": "optional-session-id"
        }
    """
    try:
        start_time = time.time()
        
        # Create the agent
        agent = get_agent(
            agent_id=agent_id,
            model_id=settings.gemini_model,
            user_id=body.user_id,
            session_id=body.session_id,
            debug_mode=True,
            subject=subject,
            difficulty=difficulty,
            intensity=intensity
        )
        
        # Handle streaming vs non-streaming
        if body.stream:
            # For now, return error for streaming - we'll implement this later
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="Streaming not yet implemented with new response models"
            )
        else:
            # Non-streaming execution
            response = agent.run(body.message)
            
            end_time = time.time()
            processing_time_ms = int((end_time - start_time) * 1000)
            
            # Get the response content
            if hasattr(response, 'content'):
                content = response.content
            elif hasattr(response, 'messages') and response.messages:
                content = response.messages[-1].content
            else:
                content = str(response)
            
            session_id = body.session_id or agent.session_id or str(uuid.uuid4())
            
            return _create_agent_run_response(
                agent=agent,
                content=content,
                session_id=session_id,
                processing_time_ms=processing_time_ms,
                agent_type=agent_id,
                subject=subject,
                difficulty=difficulty,
                intensity=intensity
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error running agent {agent_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute agent: {str(e)}"
        )


# Removed duplicate endpoint - using the main one above