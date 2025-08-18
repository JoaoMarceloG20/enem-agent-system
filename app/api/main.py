from fastapi import APIRouter

from app.api.routes import agents, health, playground, tutor, quiz, essay, study_plan, orchestrator

api_router = APIRouter()

# Health and system routes
api_router.include_router(health.router, prefix='/health', tags=['health'])

# General agents route (legacy)
api_router.include_router(agents.router, prefix='/agents', tags=['agents'])

# Agent-specific routes (new structure)
api_router.include_router(tutor.router, prefix='/tutor', tags=['tutor'])
api_router.include_router(quiz.router, prefix='/quiz', tags=['quiz'])
api_router.include_router(essay.router, prefix='/essay', tags=['essay'])
api_router.include_router(study_plan.router, prefix='/study-plan', tags=['study-plan'])
api_router.include_router(orchestrator.router, prefix='/orchestrator', tags=['orchestrator'])

# Playground
api_router.include_router(playground.router, prefix='/playground', tags=['playground'])
