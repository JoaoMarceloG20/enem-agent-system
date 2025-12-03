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
    Envia uma mensagem para o orquestrador, que irá rotear para o agente adequado.
    
    O orquestrador analisa a intenção da mensagem e decide se deve responder diretamente
    ou encaminhar para um agente especializado (Tutor, Quiz, Essay, StudyPlan).
    
    Args:
        request: Objeto contendo a mensagem e metadados.
        
    Returns:
        OrchestratorChatResponse: Resposta do agente selecionado.
        
    Example:
        POST /api/v1/orchestrator/chat
        {
            "message": "Gostaria de um plano de estudos de matemática",
            "user_id": "user123"
        }
        
        Response:
        {
            "status": "success",
            "response": "Aqui está um plano de estudos focado em matemática...",
            "agent_id": "study_plan",
            "metadata": {
                "routed_to": "study_plan",
                "reason": "Solicitação de planejamento"
            }
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
    Retorna informações sobre o orquestrador e suas capacidades.
    
    Returns:
        Dict com detalhes do orquestrador.
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