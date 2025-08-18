from fastapi import APIRouter

from app.agents.health import get_system_health, get_agents_health
from app.api.models import HealthCheckResponse, StatusEnum

router = APIRouter()


@router.get('/', response_model=HealthCheckResponse)
def health_check():
    """Check the health of the API"""
    return HealthCheckResponse(
        status=StatusEnum.SUCCESS,
        message='Edtech Agent API is running'
    )


@router.get('/detailed', response_model=HealthCheckResponse)
def detailed_health_check():
    """Get detailed health information for all system components"""
    try:
        system_health = get_system_health()
        agents_health = get_agents_health()
        
        # Combine health data
        services = {
            **system_health,
            **agents_health
        }
        
        # Determine overall status
        all_healthy = all(services.values())
        status = StatusEnum.SUCCESS if all_healthy else StatusEnum.PARTIAL
        
        return HealthCheckResponse(
            status=status,
            message='Detailed health check completed',
            services=services,
            version="1.0.0"
        )
    except Exception as e:
        return HealthCheckResponse(
            status=StatusEnum.ERROR,
            message=f'Health check failed: {str(e)}',
            services={}
        )


@router.get('/system', response_model=HealthCheckResponse)
def system_health_check():
    """Get system-level health checks (database, qdrant, api keys)"""
    try:
        system_health = get_system_health()
        
        all_healthy = all(system_health.values())
        status = StatusEnum.SUCCESS if all_healthy else StatusEnum.PARTIAL
        
        return HealthCheckResponse(
            status=status,
            message='System health check completed',
            services=system_health
        )
    except Exception as e:
        return HealthCheckResponse(
            status=StatusEnum.ERROR,
            message=f'System health check failed: {str(e)}',
            services={}
        )


@router.get('/agents', response_model=HealthCheckResponse)
def agents_health_check():
    """Get agent-specific health information"""
    try:
        agents_health = get_agents_health()
        
        all_healthy = all(agents_health.values())
        status = StatusEnum.SUCCESS if all_healthy else StatusEnum.PARTIAL
        
        return HealthCheckResponse(
            status=status,
            message='Agents health check completed',
            services=agents_health
        )
    except Exception as e:
        return HealthCheckResponse(
            status=StatusEnum.ERROR,
            message=f'Agents health check failed: {str(e)}',
            services={}
        )
