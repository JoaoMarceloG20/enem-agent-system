"""
Health Check System for ENEM Agents

This module provides health check utilities for monitoring
the status of all ENEM agents and their dependencies.
"""

from typing import Dict, Any
import time
from datetime import datetime

from app.core.config import settings


def check_database_connection() -> Dict[str, Any]:
    """
    Check PostgreSQL database connection.
    
    Returns:
        Dict with connection status and timing
    """
    try:
        start_time = time.time()
        from app.core.db import engine
        
        with engine.connect() as conn:
            # Simple query to test connection
            result = conn.execute("SELECT 1")
            result.fetchone()
        
        response_time = round((time.time() - start_time) * 1000, 2)
        
        return {
            'status': 'healthy',
            'response_time_ms': response_time,
            'message': 'Database connection successful'
        }
    except Exception as e:
        return {
            'status': 'unhealthy', 
            'error': str(e),
            'message': 'Database connection failed'
        }


def check_qdrant_connection() -> Dict[str, Any]:
    """
    Check Qdrant vector database connection.
    
    Returns:
        Dict with connection status and collections info
    """
    try:
        start_time = time.time()
        from app.core.qdrant import get_qdrant_client
        
        client = get_qdrant_client()
        collections = client.get_collections()
        
        response_time = round((time.time() - start_time) * 1000, 2)
        
        return {
            'status': 'healthy',
            'response_time_ms': response_time,
            'collections_count': len(collections.collections),
            'collections': [c.name for c in collections.collections],
            'message': 'Qdrant connection successful'
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e), 
            'message': 'Qdrant connection failed'
        }


def check_google_api_key() -> Dict[str, Any]:
    """
    Check Google API key availability.
    
    Returns:
        Dict with API key status
    """
    api_key = settings.GOOGLE_API_KEY
    
    if not api_key:
        return {
            'status': 'unhealthy',
            'message': 'Google API key not configured',
            'configured': False
        }
    
    if api_key.startswith('your_') or api_key == 'changethis':
        return {
            'status': 'unhealthy', 
            'message': 'Google API key is placeholder value',
            'configured': False
        }
    
    return {
        'status': 'healthy',
        'message': 'Google API key configured',
        'configured': True,
        'key_length': len(api_key)
    }


def get_system_health() -> Dict[str, Any]:
    """
    Get comprehensive system health status.
    
    Returns:
        Dict with all system health checks
    """
    # Perform all health checks
    db_health = check_database_connection()
    qdrant_health = check_qdrant_connection() 
    api_health = check_google_api_key()
    
    # Determine overall health
    all_healthy = all([
        db_health['status'] == 'healthy',
        qdrant_health['status'] == 'healthy', 
        api_health['status'] == 'healthy'
    ])
    
    return {
        'timestamp': datetime.utcnow().isoformat(),
        'overall_status': 'healthy' if all_healthy else 'unhealthy',
        'components': {
            'database': db_health,
            'qdrant': qdrant_health,
            'google_api': api_health
        },
        'system_info': {
            'project_name': settings.PROJECT_NAME,
            'environment': settings.ENVIRONMENT,
            'api_version': settings.API_V1_STR
        }
    }


def get_agents_health() -> Dict[str, Any]:
    """
    Get health status for all ENEM agents.
    
    Returns:
        Dict with agent-specific health information
    """
    agents_status = {
        'total_agents': 0,
        'healthy_agents': 0,
        'agents': {}
    }
    
    # Test implemented agents
    try:
        from .test_agent import TestENEMAgent
        test_agent = TestENEMAgent()
        test_health = test_agent.health_check()
        
        agents_status['agents']['test_enem'] = test_health
        agents_status['total_agents'] += 1
        if test_health.get('healthy', False):
            agents_status['healthy_agents'] += 1
            
    except Exception as e:
        agents_status['agents']['test_enem'] = {'error': str(e), 'healthy': False}
    
    # TutorAgent health check
    try:
        from .tutor_agent import TutorAgent
        tutor_agent = TutorAgent()
        tutor_health = tutor_agent.health_check()
        
        agents_status['agents']['tutor'] = tutor_health
        agents_status['total_agents'] += 1
        if tutor_health.get('healthy', False):
            agents_status['healthy_agents'] += 1
            
    except Exception as e:
        agents_status['agents']['tutor'] = {'error': str(e), 'healthy': False}
    
    # QuizAgent health check
    try:
        from .quiz_agent import QuizAgent
        quiz_agent = QuizAgent()
        quiz_health = quiz_agent.health_check()
        
        agents_status['agents']['quiz'] = quiz_health
        agents_status['total_agents'] += 1
        if quiz_health.get('healthy', False):
            agents_status['healthy_agents'] += 1
            
    except Exception as e:
        agents_status['agents']['quiz'] = {'error': str(e), 'healthy': False}
    
    # TODO: Add other agents as they are implemented
    # EssayGraderAgent, StudyPlanAgent, OrchestratorAgent
    
    agents_status['health_percentage'] = (
        (agents_status['healthy_agents'] / agents_status['total_agents'] * 100) 
        if agents_status['total_agents'] > 0 else 0
    )
    
    return agents_status