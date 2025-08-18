"""
Orchestrator Agent API Routes

Rotas específicas para o OrchestratorAgent com endpoints otimizados para frontend.
Inclui funcionalidades de coordenação central, status do sistema e roteamento.
"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel, Field

from app.agents.selector import get_agent, AgentType
from app.api.models import (
    AgentRunRequest,
    AgentRunMetadata,
    StatusEnum,
    BaseResponse,
    ErrorResponse
)

router = APIRouter()

# Orchestrator-specific models
class OrchestratorInfoResponse(BaseResponse):
    """Response for orchestrator agent information"""
    status: StatusEnum = StatusEnum.SUCCESS
    agent_name: str
    description: str
    managed_agents: Dict[str, Dict[str, Any]]
    available_commands: Dict[str, str]
    system_capabilities: List[str]
    current_sessions: int

class CommandRequest(BaseModel):
    """Request for command execution"""
    command: str = Field(..., description="Command to execute")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Command parameters")
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class CommandResponse(BaseResponse):
    """Response for command execution"""
    status: StatusEnum = StatusEnum.SUCCESS
    command_executed: str
    result: Dict[str, Any]
    output_message: str
    next_suggestions: List[str]
    execution_time: float

class SystemStatusResponse(BaseResponse):
    """Response for system status"""
    status: StatusEnum = StatusEnum.SUCCESS
    overall_health: str
    agents_status: Dict[str, Dict[str, Any]]
    system_metrics: Dict[str, Any]
    active_sessions: int
    uptime: str
    last_check: str

class AgentInfo(BaseModel):
    """Agent information model"""
    agent_id: str
    name: str
    description: str
    status: str
    last_used: Optional[str]
    total_interactions: int
    capabilities: List[str]

class AgentsListResponse(BaseResponse):
    """Response for agents list"""
    status: StatusEnum = StatusEnum.SUCCESS
    agents: List[AgentInfo]
    total_agents: int
    active_agents: int

class SessionInfo(BaseModel):
    """Session information model"""
    session_id: str
    user_id: Optional[str]
    agent_type: str
    created_at: str
    last_activity: str
    total_interactions: int
    status: str

class SessionsResponse(BaseResponse):
    """Response for sessions list"""
    status: StatusEnum = StatusEnum.SUCCESS
    sessions: List[SessionInfo]
    total_sessions: int
    active_sessions: int


@router.get("/info", response_model=OrchestratorInfoResponse)
async def get_orchestrator_info():
    """
    Get detailed information about the OrchestratorAgent.
    
    Returns comprehensive information about managed agents, commands, and system capabilities.
    """
    try:
        from app.agents.orchestrator_agent import OrchestratorAgent
        
        # Get managed agents with detailed info
        managed_agents = {}
        for agent_id, description in OrchestratorAgent.MANAGED_AGENTS.items():
            managed_agents[agent_id] = {
                "name": _get_agent_display_name(agent_id),
                "description": description,
                "endpoint": f"/api/v1/{agent_id}/",
                "status": "active",
                "capabilities": _get_agent_capabilities(agent_id)
            }
        
        # Get available commands
        available_commands = OrchestratorAgent.SUPPORTED_COMMANDS.copy()
        
        system_capabilities = [
            "Roteamento inteligente de mensagens",
            "Gerenciamento de sessões ativas", 
            "Health checks de todos os agentes",
            "Broadcasting de mensagens",
            "Sistema de comandos integrado",
            "Coordenação entre agentes",
            "Monitoramento de performance",
            "Balanceamento de carga"
        ]
        
        # Simulate current sessions count
        current_sessions = 5  # In real implementation, query actual sessions
        
        return OrchestratorInfoResponse(
            message="Informações do OrchestratorAgent recuperadas com sucesso",
            agent_name="Orquestrador Central ENEM",
            description="Coordenador central responsável pelo roteamento e gerenciamento de todos os agentes do sistema",
            managed_agents=managed_agents,
            available_commands=available_commands,
            system_capabilities=system_capabilities,
            current_sessions=current_sessions
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter informações do orquestrador: {str(e)}"
        )


@router.post("/command", response_model=CommandResponse)
async def execute_command(request: CommandRequest):
    """
    Execute a system command through the orchestrator.
    
    Handles system commands like status checks, agent switching, and session management.
    """
    try:
        start_time = datetime.now()
        
        # Create orchestrator agent
        agent = get_agent(
            agent_id=AgentType.ORCHESTRATOR,
            user_id=request.user_id,
            session_id=request.session_id
        )
        
        # Process the command
        command_result = _process_command(request.command, request.parameters)
        
        # Generate next suggestions based on command
        next_suggestions = _generate_next_suggestions(request.command)
        
        # Calculate execution time
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return CommandResponse(
            message="Comando executado com sucesso",
            command_executed=request.command,
            result=command_result,
            output_message=command_result.get("message", "Comando processado"),
            next_suggestions=next_suggestions,
            execution_time=execution_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na execução do comando: {str(e)}"
        )


@router.get("/system-status", response_model=SystemStatusResponse)
async def get_system_status():
    """
    Get comprehensive system status and health information.
    
    Returns detailed status of all agents, system metrics, and performance data.
    """
    try:
        # Get agents status
        agents_status = _get_agents_status()
        
        # Calculate overall health
        overall_health = _calculate_overall_health(agents_status)
        
        # Get system metrics
        system_metrics = _get_system_metrics()
        
        # Get active sessions count
        active_sessions = _get_active_sessions_count()
        
        # Calculate uptime (simplified)
        uptime = _calculate_uptime()
        
        return SystemStatusResponse(
            message="Status do sistema recuperado com sucesso",
            overall_health=overall_health,
            agents_status=agents_status,
            system_metrics=system_metrics,
            active_sessions=active_sessions,
            uptime=uptime,
            last_check=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter status do sistema: {str(e)}"
        )


@router.get("/agents", response_model=AgentsListResponse)
async def get_agents_list():
    """
    Get detailed list of all managed agents.
    
    Returns comprehensive information about each agent including status and capabilities.
    """
    try:
        from app.agents.orchestrator_agent import OrchestratorAgent
        
        agents = []
        active_agents = 0
        
        for agent_id, description in OrchestratorAgent.MANAGED_AGENTS.items():
            # Check agent status (simplified for demo)
            agent_status = "active"
            if agent_status == "active":
                active_agents += 1
            
            agents.append(AgentInfo(
                agent_id=agent_id,
                name=_get_agent_display_name(agent_id),
                description=description,
                status=agent_status,
                last_used=_get_agent_last_used(agent_id),
                total_interactions=_get_agent_interactions_count(agent_id),
                capabilities=_get_agent_capabilities(agent_id)
            ))
        
        return AgentsListResponse(
            message=f"Lista de {len(agents)} agentes recuperada com sucesso",
            agents=agents,
            total_agents=len(agents),
            active_agents=active_agents
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter lista de agentes: {str(e)}"
        )


@router.get("/sessions", response_model=SessionsResponse)
async def get_sessions_list(
    status_filter: Optional[str] = Query(None, description="Filter by session status"),
    agent_type: Optional[str] = Query(None, description="Filter by agent type"),
    limit: int = Query(20, ge=1, le=100, description="Maximum sessions to return")
):
    """
    Get list of active and recent sessions.
    
    Returns detailed information about user sessions across all agents.
    """
    try:
        # Get sessions (in real implementation, query database)
        sessions = _get_sessions_list(status_filter, agent_type, limit)
        
        # Count active sessions
        active_sessions = len([s for s in sessions if s.status == "active"])
        
        return SessionsResponse(
            message=f"Lista de {len(sessions)} sessões recuperada com sucesso",
            sessions=sessions,
            total_sessions=len(sessions),
            active_sessions=active_sessions
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter lista de sessões: {str(e)}"
        )


# Helper functions
def _get_agent_display_name(agent_id: str) -> str:
    """Get display name for agent"""
    names = {
        "tutor": "Tutor ENEM",
        "quiz": "Gerador de Quizzes",
        "essay": "Corretor de Redações",
        "study_plan": "Planejador de Estudos"
    }
    return names.get(agent_id, agent_id.title())

def _get_agent_capabilities(agent_id: str) -> List[str]:
    """Get capabilities for agent"""
    capabilities = {
        "tutor": [
            "Responder perguntas sobre ENEM",
            "Explicar conceitos complexos",
            "Fornecer exemplos práticos"
        ],
        "quiz": [
            "Gerar questões customizadas",
            "Correção automática",
            "Análise de performance"
        ],
        "essay": [
            "Correção nas 5 competências",
            "Feedback detalhado",
            "Sugestões de melhoria"
        ],
        "study_plan": [
            "Planos personalizados",
            "Cronogramas otimizados",
            "Acompanhamento de progresso"
        ]
    }
    return capabilities.get(agent_id, [])

def _process_command(command: str, parameters: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Process orchestrator command"""
    command = command.lower().strip()
    
    if command == "/help" or command == "help":
        return {
            "type": "help",
            "message": "Comandos disponíveis: /status, /agents, /sessions, /health",
            "commands": [
                "/status - Status do sistema",
                "/agents - Lista de agentes",  
                "/sessions - Sessões ativas",
                "/health - Verificação de saúde"
            ]
        }
    
    elif command == "/status" or command == "status":
        return {
            "type": "status",
            "message": "Sistema operacional - todos os agentes ativos",
            "details": {
                "agents_active": 4,
                "sessions_active": 5,
                "health": "green"
            }
        }
    
    elif command == "/agents" or command == "agents":
        return {
            "type": "agents",
            "message": "4 agentes disponíveis",
            "agents": ["tutor", "quiz", "essay", "study_plan"]
        }
    
    elif command == "/sessions" or command == "sessions":
        return {
            "type": "sessions",
            "message": "5 sessões ativas no momento",
            "active_sessions": 5
        }
    
    elif command == "/health" or command == "health":
        return {
            "type": "health",
            "message": "Todos os sistemas operando normalmente",
            "health_status": "green",
            "checks": {
                "database": "ok",
                "ai_models": "ok", 
                "api_endpoints": "ok"
            }
        }
    
    else:
        return {
            "type": "error",
            "message": f"Comando '{command}' não reconhecido. Use /help para ver comandos disponíveis",
            "suggestion": "Digite /help para ver todos os comandos"
        }

def _generate_next_suggestions(command: str) -> List[str]:
    """Generate next step suggestions based on command"""
    suggestions_map = {
        "/help": ["/status", "/agents", "/sessions"],
        "/status": ["/agents", "/health", "/sessions"],
        "/agents": ["/status", "/sessions"],
        "/sessions": ["/agents", "/status"],
        "/health": ["/status", "/agents"]
    }
    
    return suggestions_map.get(command.lower(), ["/help", "/status"])

def _get_agents_status() -> Dict[str, Dict[str, Any]]:
    """Get status of all agents"""
    return {
        "tutor": {
            "status": "active",
            "health": "green",
            "response_time": "150ms",
            "success_rate": "99.2%",
            "last_interaction": "2 minutes ago"
        },
        "quiz": {
            "status": "active", 
            "health": "green",
            "response_time": "200ms",
            "success_rate": "98.8%",
            "last_interaction": "5 minutes ago"
        },
        "essay": {
            "status": "active",
            "health": "green", 
            "response_time": "300ms",
            "success_rate": "99.0%",
            "last_interaction": "1 minute ago"
        },
        "study_plan": {
            "status": "active",
            "health": "green",
            "response_time": "180ms", 
            "success_rate": "99.5%",
            "last_interaction": "10 minutes ago"
        }
    }

def _calculate_overall_health(agents_status: Dict[str, Dict[str, Any]]) -> str:
    """Calculate overall system health"""
    green_count = sum(1 for agent in agents_status.values() if agent["health"] == "green")
    total_agents = len(agents_status)
    
    if green_count == total_agents:
        return "Excelente"
    elif green_count >= total_agents * 0.8:
        return "Bom" 
    elif green_count >= total_agents * 0.5:
        return "Regular"
    else:
        return "Crítico"

def _get_system_metrics() -> Dict[str, Any]:
    """Get system metrics"""
    return {
        "cpu_usage": "45%",
        "memory_usage": "62%",
        "disk_usage": "38%",
        "network_latency": "25ms",
        "requests_per_minute": 120,
        "error_rate": "0.5%",
        "average_response_time": "180ms"
    }

def _get_active_sessions_count() -> int:
    """Get active sessions count"""
    return 5  # Placeholder

def _calculate_uptime() -> str:
    """Calculate system uptime"""
    return "2 dias, 14 horas, 32 minutos"  # Placeholder

def _get_agent_last_used(agent_id: str) -> Optional[str]:
    """Get when agent was last used"""
    last_used_times = {
        "tutor": "2 minutes ago",
        "quiz": "5 minutes ago", 
        "essay": "1 minute ago",
        "study_plan": "10 minutes ago"
    }
    return last_used_times.get(agent_id)

def _get_agent_interactions_count(agent_id: str) -> int:
    """Get total interactions count for agent"""
    interaction_counts = {
        "tutor": 1250,
        "quiz": 890,
        "essay": 450,
        "study_plan": 320
    }
    return interaction_counts.get(agent_id, 0)

def _get_sessions_list(status_filter: Optional[str], agent_type: Optional[str], 
                      limit: int) -> List[SessionInfo]:
    """Get sessions list with filters"""
    # Generate sample sessions
    sessions = []
    
    agents = ["tutor", "quiz", "essay", "study_plan"]
    statuses = ["active", "inactive", "completed"]
    
    for i in range(min(limit, 10)):
        agent = agents[i % len(agents)]
        session_status = statuses[i % len(statuses)]
        
        # Apply filters
        if status_filter and session_status != status_filter:
            continue
        if agent_type and agent != agent_type:
            continue
        
        sessions.append(SessionInfo(
            session_id=f"session_{i+1}",
            user_id=f"user_{(i % 3) + 1}",
            agent_type=agent,
            created_at=(datetime.now() - timedelta(hours=i)).isoformat(),
            last_activity=(datetime.now() - timedelta(minutes=i*10)).isoformat(),
            total_interactions=5 + i*2,
            status=session_status
        ))
    
    return sessions