"""
Orchestrator Agent API Routes

Rotas para o OrchestratorAgent.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

from app.agents.orchestrator_agent import get_orchestrator_agent
from app.api.models import BaseResponse, StatusEnum

router = APIRouter()

class OrchestratorChatRequest(BaseModel):
    message: str = Field(..., description="Mensagem do usuário para o orquestrador")
    user_id: Optional[str] = Field(None, description="ID do usuário para contexto")
    session_id: Optional[str] = Field(None, description="ID da sessão para continuidade")

class OrchestratorChatResponse(BaseResponse):
    status: StatusEnum = StatusEnum.SUCCESS
    response: str
    agent_id: str
    metadata: Optional[Dict[str, Any]] = None

@router.post("/chat", response_model=OrchestratorChatResponse)
async def chat_with_orchestrator(request: OrchestratorChatRequest):
    """
    Send a message to the orchestrator to route to the appropriate agent.
    
    The orchestrator analyzes the intent of the message and decides whether to respond
    directly or forward it to a specialized agent (Tutor, Quiz, Essay, StudyPlan).
    
    Args:
        request (OrchestratorChatRequest): Object containing the message and metadata.
        
    Returns:
        OrchestratorChatResponse: Response from the selected agent.
        
    Example:
        POST /api/v1/orchestrator/chat
        {
            "message": "I would like a math study plan",
            "user_id": "user123"
        }
    """
    try:
        orchestrator = get_orchestrator_agent()
        
        result = orchestrator.process_message(
            message=request.message,
            user_id=request.user_id,
            session_id=request.session_id
        )
        
        return OrchestratorChatResponse(
            message="Mensagem processada com sucesso",
            response=result["content"],
            agent_id=result["agent_id"],
            metadata=result.get("metadata")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro no orquestrador: {str(e)}"
        )

@router.get("/info")
async def get_orchestrator_info():
    """
    Get information about the orchestrator and its capabilities.
    
    Returns:
        Dict: Details about the orchestrator and routing capabilities.
    """
    return {
        "name": "Orchestrator ENEM",
        "description": "Coordenador central que roteia mensagens para agentes especializados.",
        "capabilities": [
            "Roteamento inteligente",
            "Tutor (Matérias)",
            "Quiz (Questões)",
            "Essay (Redação)",
            "Study Plan (Cronogramas)"
        ]
    }