"""
Tutor Agent API Routes

Rotas específicas para o TutorAgent com endpoints otimizados para frontend.
Inclui funcionalidades de tutoria educacional especializada em ENEM.
"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel

from app.agents.selector import get_agent, AgentType
from app.api.models import (
    AgentRunRequest,
    TutorResponse,
    AgentRunMetadata,
    StatusEnum,
    BaseResponse,
    SubjectEnum,
    ErrorResponse,
    SubjectListResponse,
)

router = APIRouter()

# Tutor-specific models
class TutorInfoResponse(BaseResponse):
    """Response for tutor information"""
    status: StatusEnum = StatusEnum.SUCCESS
    agent_name: str
    description: str
    supported_subjects: List[Dict[str, str]]
    capabilities: List[str]
    temperature: float
    max_tokens: int

class TutorChatRequest(BaseModel):
    """Request for tutor chat interaction"""
    message: str
    subject: Optional[SubjectEnum] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class TutorChatResponse(TutorResponse):
    """Enhanced response for tutor interactions"""
    explanation_type: Optional[str] = None  # "concept", "problem", "example"
    difficulty_level: Optional[str] = None  # "basic", "intermediate", "advanced"
    subject_focus: Optional[str] = None
    learning_objectives: Optional[List[str]] = None

class SubjectTreeResponse(BaseResponse):
    """Response for subject tree structure"""
    status: StatusEnum = StatusEnum.SUCCESS
    subject: str
    subject_name: str
    topics: List[Dict[str, Any]]
    total_topics: int

class LearningPathResponse(BaseResponse):
    """Response for learning path recommendations"""
    status: StatusEnum = StatusEnum.SUCCESS
    subject: str
    current_level: str
    recommended_path: List[Dict[str, Any]]
    estimated_duration: str


@router.get("/info", response_model=TutorInfoResponse)
async def get_tutor_info():
    """
    Get detailed information about the TutorAgent.
    
    Returns comprehensive information about capabilities, subjects, and configuration.
    """
    try:
        from app.agents.tutor_agent import TutorAgent
        
        # Get subjects with proper formatting
        subjects_data = []
        for key, name in TutorAgent.ENEM_SUBJECTS.items():
            subjects_data.append({
                "key": key,
                "name": name,
                "icon": _get_subject_icon(key)
            })
        
        capabilities = [
            "Explicações didáticas personalizadas",
            "Resolução de problemas passo a passo",
            "Adaptação ao nível do estudante",
            "Sugestões de estudo direcionadas",
            "Conexão com tópicos relacionados",
            "Exemplos práticos contextualizados",
            "Preparação específica para ENEM"
        ]
        
        return TutorInfoResponse(
            message="Informações do TutorAgent recuperadas com sucesso",
            agent_name="Tutor ENEM - Especialista Educacional",
            description="Tutor IA especializado em preparação para ENEM com suporte a todas as 13 matérias",
            supported_subjects=subjects_data,
            capabilities=capabilities,
            temperature=0.7,
            max_tokens=2048
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter informações do tutor: {str(e)}"
        )


@router.post("/chat", response_model=TutorChatResponse)
async def chat_with_tutor(request: TutorChatRequest):
    """
    Interact with the TutorAgent for educational guidance.
    
    Provides personalized tutoring with subject-specific expertise.
    """
    try:
        # Create tutor agent
        agent = get_agent(
            agent_id=AgentType.TUTOR,
            subject=request.subject,
            user_id=request.user_id,
            session_id=request.session_id
        )
        
        # Execute conversation
        response = agent.run(request.message)
        
        # Extract content from response
        if hasattr(response, 'content'):
            content = response.content
        elif hasattr(response, 'messages') and response.messages:
            content = response.messages[-1].content
        else:
            content = str(response)
        
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Create metadata
        metadata = AgentRunMetadata(
            agent_id="tutor",
            agent_name=agent.name,
            model_used="gemini-2.5-flash",
            temperature=0.7,
            max_tokens=2048,
            subject=request.subject,
            processing_time_ms=None
        )
        
        # Analyze message to determine response characteristics
        explanation_type = _analyze_message_type(request.message)
        difficulty_level = _determine_difficulty_level(request.message, content)
        learning_objectives = _extract_learning_objectives(content)
        
        return TutorChatResponse(
            message="Resposta do tutor gerada com sucesso",
            content=content,
            metadata=metadata,
            session_id=session_id,
            run_id=str(uuid.uuid4()),
            concept_explained=_extract_concept(request.message),
            related_topics=_extract_related_topics(content),
            examples=_extract_examples(content),
            practice_suggestions=_extract_practice_suggestions(content),
            explanation_type=explanation_type,
            difficulty_level=difficulty_level,
            subject_focus=request.subject,
            learning_objectives=learning_objectives
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na interação com tutor: {str(e)}"
        )


@router.get("/subjects/{subject}/tree", response_model=SubjectTreeResponse)
async def get_subject_tree(subject: SubjectEnum):
    """
    Get the hierarchical structure of topics for a specific subject.
    
    Returns organized tree of topics, subtopics, and learning materials.
    """
    try:
        from app.agents.tutor_agent import TutorAgent
        
        if subject not in TutorAgent.ENEM_SUBJECTS:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Matéria '{subject}' não encontrada"
            )
        
        subject_name = TutorAgent.ENEM_SUBJECTS[subject]
        topics = _build_subject_tree(subject)
        
        return SubjectTreeResponse(
            message=f"Estrutura de tópicos para {subject_name} recuperada com sucesso",
            subject=subject,
            subject_name=subject_name,
            topics=topics,
            total_topics=len(topics)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter estrutura de tópicos: {str(e)}"
        )


@router.get("/learning-path/{subject}", response_model=LearningPathResponse)
async def get_learning_path(
    subject: SubjectEnum,
    current_level: str = Query("basic", description="Nível atual: basic, intermediate, advanced"),
    focus_areas: Optional[List[str]] = Query(None, description="Áreas de foco específicas")
):
    """
    Get personalized learning path for a subject.
    
    Returns recommended sequence of topics based on current level and goals.
    """
    try:
        from app.agents.tutor_agent import TutorAgent
        
        if subject not in TutorAgent.ENEM_SUBJECTS:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Matéria '{subject}' não encontrada"
            )
        
        # Build personalized learning path
        learning_path = _build_learning_path(subject, current_level, focus_areas or [])
        estimated_duration = _calculate_duration(learning_path)
        
        return LearningPathResponse(
            message=f"Trilha de aprendizagem para {subject} criada com sucesso",
            subject=subject,
            current_level=current_level,
            recommended_path=learning_path,
            estimated_duration=estimated_duration
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar trilha de aprendizagem: {str(e)}"
        )


@router.get("/subjects", response_model=SubjectListResponse)
async def get_supported_subjects():
    """
    Get list of all subjects supported by the TutorAgent.
    
    Returns comprehensive list with metadata for each subject.
    """
    try:
        from app.agents.tutor_agent import TutorAgent
        
        subjects_data = []
        for key, name in TutorAgent.ENEM_SUBJECTS.items():
            subjects_data.append({
                "key": key,
                "name": name,
                "icon": _get_subject_icon(key),
                "description": _get_subject_description(key),
                "difficulty": _get_subject_difficulty(key),
                "estimated_hours": _get_estimated_hours(key)
            })
        
        return SubjectListResponse(
            status=StatusEnum.SUCCESS,
            message="Matérias suportadas recuperadas com sucesso",
            subjects=subjects_data
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter matérias: {str(e)}"
        )


# Helper functions
def _get_subject_icon(subject: str) -> str:
    """Get icon for subject"""
    icons = {
        "matematica": "📊",
        "portugues": "📝",
        "literatura": "📚",
        "ingles": "🇺🇸",
        "espanhol": "🇪🇸",
        "fisica": "⚡",
        "quimica": "🧪",
        "biologia": "🧬",
        "historia": "🏛️",
        "geografia": "🌍",
        "filosofia": "🤔",
        "sociologia": "👥",
        "redacao": "✍️"
    }
    return icons.get(subject, "📖")

def _analyze_message_type(message: str) -> str:
    """Analyze message to determine explanation type"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["o que é", "define", "conceito", "significa"]):
        return "concept"
    elif any(word in message_lower for word in ["como resolver", "resolva", "calcule", "problema"]):
        return "problem"
    elif any(word in message_lower for word in ["exemplo", "mostre", "demonstre"]):
        return "example"
    else:
        return "general"

def _determine_difficulty_level(message: str, response: str) -> str:
    """Determine difficulty level of explanation"""
    # Simple heuristic based on content complexity
    if len(response) < 200:
        return "basic"
    elif len(response) < 500:
        return "intermediate"
    else:
        return "advanced"

def _extract_concept(message: str) -> Optional[str]:
    """Extract main concept from message"""
    # Simple extraction logic
    if "?" in message:
        return message.split("?")[0].strip()
    return None

def _extract_related_topics(content: str) -> List[str]:
    """Extract related topics from response"""
    # Placeholder implementation
    return ["Tópico relacionado 1", "Tópico relacionado 2"]

def _extract_examples(content: str) -> List[str]:
    """Extract examples from response"""
    # Placeholder implementation
    return ["Exemplo prático relacionado"]

def _extract_practice_suggestions(content: str) -> List[str]:
    """Extract practice suggestions from response"""
    # Placeholder implementation
    return ["Exercícios recomendados", "Material complementar"]

def _extract_learning_objectives(content: str) -> List[str]:
    """Extract learning objectives from response"""
    # Placeholder implementation
    return ["Dominar conceito fundamental", "Aplicar em contextos práticos"]

def _build_subject_tree(subject: str) -> List[Dict[str, Any]]:
    """Build hierarchical topic structure for subject"""
    # Placeholder implementation with sample data
    sample_topics = {
        "matematica": [
            {
                "id": "algebra",
                "name": "Álgebra",
                "description": "Equações, inequações e funções",
                "subtopics": ["Equações do 1º grau", "Equações do 2º grau", "Funções"],
                "difficulty": "medium",
                "estimated_hours": 20
            },
            {
                "id": "geometria",
                "name": "Geometria",
                "description": "Geometria plana e espacial",
                "subtopics": ["Figuras planas", "Volumes", "Trigonometria"],
                "difficulty": "high",
                "estimated_hours": 25
            }
        ]
    }
    
    return sample_topics.get(subject, [])

def _build_learning_path(subject: str, level: str, focus_areas: List[str]) -> List[Dict[str, Any]]:
    """Build personalized learning path"""
    # Placeholder implementation
    return [
        {
            "step": 1,
            "topic": "Fundamentos",
            "description": "Conceitos básicos essenciais",
            "duration": "2 semanas",
            "activities": ["Leitura", "Exercícios básicos"],
            "resources": ["Material teórico", "Vídeos explicativos"]
        },
        {
            "step": 2,
            "topic": "Aplicação Prática",
            "description": "Exercícios e problemas práticos",
            "duration": "3 semanas",
            "activities": ["Resolução de problemas", "Simulados"],
            "resources": ["Lista de exercícios", "Provas anteriores"]
        }
    ]

def _calculate_duration(learning_path: List[Dict[str, Any]]) -> str:
    """Calculate estimated duration for learning path"""
    return "5-6 semanas"

def _get_subject_description(subject: str) -> str:
    """Get description for subject"""
    descriptions = {
        "matematica": "Álgebra, geometria, estatística e matemática aplicada",
        "portugues": "Gramática, interpretação de texto e literatura",
        # Add more descriptions...
    }
    return descriptions.get(subject, "Matéria do ENEM")

def _get_subject_difficulty(subject: str) -> str:
    """Get difficulty level for subject"""
    return "medium"  # Placeholder

def _get_estimated_hours(subject: str) -> int:
    """Get estimated study hours for subject"""
    return 40  # Placeholder
