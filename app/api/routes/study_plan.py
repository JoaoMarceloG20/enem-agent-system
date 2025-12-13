"""
Study Plan Agent API Routes

Rotas específicas para o StudyPlanAgent com endpoints otimizados para frontend.
Inclui funcionalidades de criação e gestão de planos de estudo personalizados.
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel, Field

from app.agents.selector import get_agent, AgentType
from app.api.models import (
    AgentRunRequest,
    AgentRunMetadata,
    StatusEnum,
    BaseResponse,
    SubjectEnum,
    DifficultyEnum,
    ErrorResponse
)

router = APIRouter()

# Study Plan specific models
class StudyPlanInfoResponse(BaseResponse):
    """Response for study plan agent information"""
    status: StatusEnum = StatusEnum.SUCCESS
    agent_name: str
    description: str
    study_intensities: List[Dict[str, Any]]
    subject_weights: Dict[str, Dict[str, Any]]
    capabilities: List[str]
    available_templates: List[Dict[str, Any]]

class StudyPlanRequest(BaseModel):
    """Request for study plan generation"""
    available_hours_per_day: int = Field(..., ge=1, le=16, description="Hours available per day")
    study_days_per_week: int = Field(..., ge=1, le=7, description="Days per week for studying")
    target_exam_date: Optional[str] = Field(None, description="ENEM exam date (YYYY-MM-DD)")
    priority_subjects: Optional[List[SubjectEnum]] = Field(None, description="Priority subjects")
    weak_subjects: Optional[List[SubjectEnum]] = Field(None, description="Subjects needing more focus")
    study_intensity: str = Field("medium", description="Study intensity level")
    include_breaks: bool = Field(True, description="Include break periods")
    include_weekends: bool = Field(True, description="Include weekend studying")
    student_id: Optional[str] = None
    session_id: Optional[str] = None

class WeeklySchedule(BaseModel):
    """Weekly schedule model"""
    week_number: int
    start_date: str
    end_date: str
    total_hours: int
    subjects_distribution: Dict[str, int]
    daily_schedule: Dict[str, List[Dict[str, Any]]]
    milestones: List[str]
    focus_areas: List[str]

class StudyPlanResponse(BaseResponse):
    """Response for study plan generation"""
    status: StatusEnum = StatusEnum.SUCCESS
    plan_id: str
    total_duration_weeks: int
    total_study_hours: int
    weekly_schedules: List[WeeklySchedule]
    subject_distribution: Dict[str, Dict[str, Any]]
    study_timeline: List[Dict[str, Any]]
    recommendations: List[str]
    progress_milestones: List[Dict[str, Any]]
    estimated_preparation_level: str

class ProgressUpdateRequest(BaseModel):
    """Request for progress update"""
    plan_id: str
    completed_hours: Dict[str, int]  # subject -> hours completed
    difficulty_feedback: Dict[str, str]  # subject -> "easy"|"medium"|"hard"
    topics_mastered: Optional[List[str]] = None
    current_week: Optional[int] = None
    student_id: Optional[str] = None

class ProgressUpdateResponse(BaseResponse):
    """Response for progress update"""
    status: StatusEnum = StatusEnum.SUCCESS
    updated_plan_id: str
    adjustments_made: List[str]
    new_recommendations: List[str]
    performance_analysis: Dict[str, Any]
    next_week_focus: List[str]
    completion_percentage: float

class StudyTemplate(BaseModel):
    """Study template model"""
    template_id: str
    name: str
    description: str
    target_audience: str
    duration_weeks: int
    intensity_level: str
    subjects_covered: List[str]
    daily_hours_range: str
    success_rate: str

class TemplatesResponse(BaseResponse):
    """Response for study templates"""
    status: StatusEnum = StatusEnum.SUCCESS
    templates: List[StudyTemplate]
    total_count: int
    recommended_template: Optional[str]


@router.get("/info", response_model=StudyPlanInfoResponse)
async def get_study_plan_info():
    """
    Get detailed information about the StudyPlanAgent.
    
    Returns:
        StudyPlanInfoResponse: Information about available study intensities,
        subject weights, and pre-configured templates.
    """
    try:
        from app.agents.study_plan_agent import StudyPlanAgent
        
        # Get study intensities
        study_intensities = [
            {
                "level": "light",
                "name": "Leve",
                "description": "2-4 horas/dia, foco em revisão",
                "daily_hours": "2-4",
                "recommended_for": "Estudantes com pouco tempo"
            },
            {
                "level": "medium",
                "name": "Médio", 
                "description": "4-6 horas/dia, estudo equilibrado",
                "daily_hours": "4-6",
                "recommended_for": "Maioria dos estudantes"
            },
            {
                "level": "intensive",
                "name": "Intensivo",
                "description": "6-8 horas/dia, preparação completa",
                "daily_hours": "6-8",
                "recommended_for": "Vestibulandos dedicados"
            },
            {
                "level": "extreme",
                "name": "Extremo",
                "description": "8+ horas/dia, preparação máxima",
                "daily_hours": "8+",
                "recommended_for": "Último ano de preparação"
            }
        ]
        
        # Get subject weights
        subject_weights = {}
        for subject, data in StudyPlanAgent.SUBJECT_WEIGHTS.items():
            subject_weights[subject] = {
                "hours_per_week": str(data["hours_per_week"]),
                "difficulty": data["difficulty"],
                "weight": str(data["weight"]),
                "description": data["description"]
            }
        
        capabilities = [
            "Planos de estudo personalizados",
            "Distribuição inteligente por matéria",
            "Cronogramas semanais detalhados",
            "Sistema de marcos e milestones",
            "Adaptação baseada em progresso",
            "Múltiplos níveis de intensidade",
            "Otimização de tempo disponível",
            "Recomendações específicas"
        ]
        
        available_templates = [
            {
                "id": "enem_6_months",
                "name": "ENEM 6 Meses",
                "description": "Plano completo para 6 meses de preparação",
                "intensity": "medium"
            },
            {
                "id": "enem_3_months",
                "name": "ENEM 3 Meses",
                "description": "Preparação intensiva para 3 meses",
                "intensity": "intensive"
            },
            {
                "id": "enem_1_year",
                "name": "ENEM 1 Ano",
                "description": "Preparação completa para 1 ano",
                "intensity": "light"
            }
        ]
        
        return StudyPlanInfoResponse(
            message="Informações do StudyPlanAgent recuperadas com sucesso",
            agent_name="Planejador de Estudos ENEM",
            description="Criador de planos de estudo personalizados e adaptativos para preparação ENEM",
            study_intensities=study_intensities,
            subject_weights=subject_weights,
            capabilities=capabilities,
            available_templates=available_templates
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter informações do planejador: {str(e)}"
        )


@router.post("/generate", response_model=StudyPlanResponse)
async def generate_study_plan(request: StudyPlanRequest):
    """
    Generate a personalized study plan based on available time and preferences.
    
    Creates comprehensive weekly schedules with subject distribution and milestones.

    Args:
        request (StudyPlanRequest): User constraints and preferences (hours per day,
        subjects, exam date).

    Returns:
        StudyPlanResponse: The complete study plan including weekly schedules and timeline.
    """
    try:
        # Create study plan agent
        agent = get_agent(
            agent_id=AgentType.STUDY_PLAN,
            user_id=request.student_id,
            session_id=request.session_id
        )
        
        # Build planning prompt
        prompt = _build_planning_prompt(request)
        
        # Execute study plan generation
        response = agent.run(prompt)
        
        # Extract content from response
        if hasattr(response, 'content'):
            content = response.content
        elif hasattr(response, 'messages') and response.messages:
            content = response.messages[-1].content
        else:
            content = str(response)
        
        # Generate plan components
        plan_id = str(uuid.uuid4())
        duration_weeks = _calculate_duration_weeks(request)
        total_study_hours = request.available_hours_per_day * request.study_days_per_week * duration_weeks
        
        # Generate weekly schedules
        weekly_schedules = _generate_weekly_schedules(request, duration_weeks)
        
        # Calculate subject distribution
        subject_distribution = _calculate_subject_distribution(request)
        
        # Generate study timeline
        study_timeline = _generate_study_timeline(duration_weeks, request)
        
        # Generate recommendations
        recommendations = _generate_recommendations(request)
        
        # Generate progress milestones
        progress_milestones = _generate_progress_milestones(duration_weeks)
        
        # Estimate preparation level
        preparation_level = _estimate_preparation_level(request)
        
        return StudyPlanResponse(
            message="Plano de estudos gerado com sucesso",
            plan_id=plan_id,
            total_duration_weeks=duration_weeks,
            total_study_hours=total_study_hours,
            weekly_schedules=weekly_schedules,
            subject_distribution=subject_distribution,
            study_timeline=study_timeline,
            recommendations=recommendations,
            progress_milestones=progress_milestones,
            estimated_preparation_level=preparation_level
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na geração do plano de estudos: {str(e)}"
        )


@router.put("/update-progress", response_model=ProgressUpdateResponse)
async def update_progress(request: ProgressUpdateRequest):
    """
    Update study plan progress and get adaptive recommendations.
    
    Adjusts the study plan based on completed hours and difficulty feedback.

    Args:
        request (ProgressUpdateRequest): Progress data (hours studied per subject, difficulty).

    Returns:
        ProgressUpdateResponse: Updates to the plan, including new recommendations and focus areas.
    """
    try:
        # Simulate progress analysis (in real implementation, retrieve stored plan)
        adjustments_made = _analyze_progress_and_adjust(request)
        
        # Generate new recommendations based on progress
        new_recommendations = _generate_adaptive_recommendations(request)
        
        # Analyze performance
        performance_analysis = _analyze_performance(request)
        
        # Determine next week focus
        next_week_focus = _determine_next_week_focus(request)
        
        # Calculate completion percentage
        completion_percentage = _calculate_completion_percentage(request)
        
        updated_plan_id = f"{request.plan_id}_updated_{datetime.now().strftime('%Y%m%d')}"
        
        return ProgressUpdateResponse(
            message="Progresso atualizado e plano ajustado com sucesso",
            updated_plan_id=updated_plan_id,
            adjustments_made=adjustments_made,
            new_recommendations=new_recommendations,
            performance_analysis=performance_analysis,
            next_week_focus=next_week_focus,
            completion_percentage=completion_percentage
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na atualização do progresso: {str(e)}"
        )


@router.get("/templates", response_model=TemplatesResponse)
async def get_study_templates(
    intensity: Optional[str] = Query(None, description="Filter by intensity level"),
    duration_weeks: Optional[int] = Query(None, ge=1, le=52, description="Filter by duration"),
    daily_hours: Optional[int] = Query(None, ge=1, le=16, description="Filter by daily hours")
):
    """
    Get available study plan templates.
    
    Returns pre-configured templates for different study scenarios and intensities.

    Args:
        intensity (Optional[str]): Filter by intensity (light, medium, intensive).
        duration_weeks (Optional[int]): Filter by duration.
        daily_hours (Optional[int]): Filter by daily study hours.

    Returns:
        TemplatesResponse: A list of matching templates.
    """
    try:
        # Generate templates (in real implementation, fetch from database)
        templates = _generate_study_templates(intensity, duration_weeks, daily_hours)
        
        # Determine recommended template based on filters
        recommended_template = _determine_recommended_template(intensity, duration_weeks, daily_hours)
        
        return TemplatesResponse(
            message=f"Retornados {len(templates)} templates de estudo",
            templates=templates,
            total_count=len(templates),
            recommended_template=recommended_template
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter templates: {str(e)}"
        )


# Helper functions
def _build_planning_prompt(request: StudyPlanRequest) -> str:
    """Build prompt for study plan generation"""
    priority_part = ""
    if request.priority_subjects:
        priority_part = f"\nMatérias prioritárias: {', '.join(request.priority_subjects)}"
    
    weak_part = ""
    if request.weak_subjects:
        weak_part = f"\nMatérias que precisam de mais atenção: {', '.join(request.weak_subjects)}"
    
    return f"""Crie um plano de estudos personalizado com estas especificações:

- Horas disponíveis por dia: {request.available_hours_per_day}
- Dias de estudo por semana: {request.study_days_per_week}
- Intensidade de estudo: {request.study_intensity}
- Data do ENEM: {request.target_exam_date or 'Não especificada'}
- Incluir fins de semana: {request.include_weekends}
- Incluir pausas: {request.include_breaks}{priority_part}{weak_part}

Forneça:
1. Cronograma semanal detalhado
2. Distribuição de horas por matéria
3. Marcos de progresso
4. Recomendações específicas"""

def _calculate_duration_weeks(request: StudyPlanRequest) -> int:
    """Calculate duration in weeks based on target date or default"""
    if request.target_exam_date:
        try:
            target_date = datetime.strptime(request.target_exam_date, '%Y-%m-%d')
            weeks_until_exam = (target_date - datetime.now()).days // 7
            return max(weeks_until_exam, 4)  # Minimum 4 weeks
        except ValueError:
            pass
    
    # Default duration based on intensity
    intensity_duration = {
        "light": 26,      # 6 months
        "medium": 20,     # 5 months
        "intensive": 16,  # 4 months
        "extreme": 12     # 3 months
    }
    
    return intensity_duration.get(request.study_intensity, 20)

def _generate_weekly_schedules(request: StudyPlanRequest, duration_weeks: int) -> List[WeeklySchedule]:
    """Generate weekly schedules for the study plan"""
    schedules = []
    start_date = datetime.now()
    
    for week in range(min(duration_weeks, 4)):  # Return first 4 weeks for demo
        week_start = start_date + timedelta(weeks=week)
        week_end = week_start + timedelta(days=6)
        
        # Calculate total hours for the week
        total_hours = request.available_hours_per_day * request.study_days_per_week
        
        # Distribute subjects
        subjects_distribution = _distribute_subjects_for_week(request, week, total_hours)
        
        # Generate daily schedule
        daily_schedule = _generate_daily_schedule(request, week)
        
        # Generate milestones for this week
        milestones = _generate_week_milestones(week)
        
        # Focus areas for this week
        focus_areas = _generate_week_focus_areas(week)
        
        schedules.append(WeeklySchedule(
            week_number=week + 1,
            start_date=week_start.strftime('%Y-%m-%d'),
            end_date=week_end.strftime('%Y-%m-%d'),
            total_hours=total_hours,
            subjects_distribution=subjects_distribution,
            daily_schedule=daily_schedule,
            milestones=milestones,
            focus_areas=focus_areas
        ))
    
    return schedules

def _calculate_subject_distribution(request: StudyPlanRequest) -> Dict[str, Dict[str, Any]]:
    """Calculate how hours should be distributed among subjects"""
    from app.agents.study_plan_agent import StudyPlanAgent
    
    distribution = {}
    total_weight = sum(data["weight"] for data in StudyPlanAgent.SUBJECT_WEIGHTS.values())
    
    for subject, data in StudyPlanAgent.SUBJECT_WEIGHTS.items():
        percentage = (data["weight"] / total_weight) * 100
        
        # Adjust for priority and weak subjects
        adjustment = 1.0
        if request.priority_subjects and subject in request.priority_subjects:
            adjustment += 0.2
        if request.weak_subjects and subject in request.weak_subjects:
            adjustment += 0.3
        
        final_percentage = min(percentage * adjustment, 30)  # Cap at 30%
        
        distribution[subject] = {
            "percentage": f"{final_percentage:.1f}%",
            "recommended_hours_per_week": str(int(data["hours_per_week"] * adjustment)),
            "difficulty_level": data["difficulty"],
            "priority_adjustment": f"{(adjustment - 1) * 100:+.0f}%" if adjustment != 1.0 else "0%"
        }
    
    return distribution

def _generate_study_timeline(duration_weeks: int, request: StudyPlanRequest) -> List[Dict[str, Any]]:
    """Generate study timeline with phases"""
    phases = []
    
    if duration_weeks >= 16:
        phases = [
            {
                "phase": "Fase 1: Fundamentos",
                "weeks": "1-6",
                "focus": "Conceitos básicos e revisão",
                "goals": ["Revisar conceitos fundamentais", "Identificar lacunas"]
            },
            {
                "phase": "Fase 2: Aprofundamento", 
                "weeks": "7-12",
                "focus": "Exercícios e aplicação",
                "goals": ["Praticar exercícios", "Aprofundar conhecimentos"]
            },
            {
                "phase": "Fase 3: Revisão",
                "weeks": "13-16",
                "focus": "Simulados e revisão final",
                "goals": ["Simulados regulares", "Revisão intensiva"]
            }
        ]
    else:
        phases = [
            {
                "phase": "Fase 1: Revisão Intensiva",
                "weeks": f"1-{duration_weeks//2}",
                "focus": "Conceitos e exercícios",
                "goals": ["Revisar todo conteúdo", "Resolver exercícios"]
            },
            {
                "phase": "Fase 2: Simulados",
                "weeks": f"{duration_weeks//2 + 1}-{duration_weeks}",
                "focus": "Simulados e ajustes finais",
                "goals": ["Simulados semanais", "Ajustar estratégia"]
            }
        ]
    
    return phases

def _generate_recommendations(request: StudyPlanRequest) -> List[str]:
    """Generate personalized recommendations"""
    recommendations = [
        "Mantenha consistência nos horários de estudo",
        "Faça pausas regulares durante o estudo",
        "Intercale matérias de diferentes áreas"
    ]
    
    if request.study_intensity == "extreme":
        recommendations.append("Cuidado com o burnout - inclua momentos de descanso")
    
    if request.available_hours_per_day <= 3:
        recommendations.append("Foque na qualidade do estudo devido ao tempo limitado")
    
    if request.weak_subjects:
        recommendations.append("Dedique tempo extra às matérias identificadas como fracas")
    
    return recommendations

def _generate_progress_milestones(duration_weeks: int) -> List[Dict[str, Any]]:
    """Generate progress milestones"""
    milestones = []
    
    milestone_intervals = max(duration_weeks // 4, 2)
    
    for i in range(0, duration_weeks, milestone_intervals):
        week = i + milestone_intervals
        percentage = (week / duration_weeks) * 100
        
        milestones.append({
            "week": week,
            "milestone": f"Marco {len(milestones) + 1}",
            "completion_percentage": f"{min(percentage, 100):.0f}%",
            "evaluation": f"Avaliar progresso na semana {week}",
            "adjustments": "Ajustar plano se necessário"
        })
    
    return milestones

def _estimate_preparation_level(request: StudyPlanRequest) -> str:
    """Estimate preparation level based on plan parameters"""
    total_weekly_hours = request.available_hours_per_day * request.study_days_per_week
    
    if total_weekly_hours >= 35:
        return "Alto - Preparação intensiva"
    elif total_weekly_hours >= 25:
        return "Médio-Alto - Boa preparação"
    elif total_weekly_hours >= 15:
        return "Médio - Preparação adequada"
    else:
        return "Básico - Preparação mínima"

def _distribute_subjects_for_week(request: StudyPlanRequest, week: int, total_hours: int) -> Dict[str, int]:
    """Distribute subjects for a specific week"""
    # Simplified distribution for demo
    subjects = ["matematica", "portugues", "fisica", "quimica", "biologia"]
    distribution = {}
    
    hours_per_subject = total_hours // len(subjects)
    remaining_hours = total_hours % len(subjects)
    
    for i, subject in enumerate(subjects):
        distribution[subject] = hours_per_subject
        if i < remaining_hours:
            distribution[subject] += 1
    
    return distribution

def _generate_daily_schedule(request: StudyPlanRequest, week: int) -> Dict[str, List[Dict[str, Any]]]:
    """Generate daily schedule for a week"""
    daily_schedule = {}
    days = ["monday", "tuesday", "wednesday", "thursday", "friday"]
    
    if request.include_weekends:
        days.extend(["saturday", "sunday"])
    
    for day in days[:request.study_days_per_week]:
        schedule = []
        hours_per_day = request.available_hours_per_day
        
        # Distribute hours throughout the day
        for hour in range(min(hours_per_day, 3)):  # Show first 3 hours for demo
            schedule.append({
                "time_slot": f"{9 + hour * 2}:00-{11 + hour * 2}:00",
                "subject": ["matematica", "portugues", "fisica"][hour % 3],
                "activity": "Estudo teórico e exercícios",
                "duration_minutes": 120
            })
        
        daily_schedule[day] = schedule
    
    return daily_schedule

def _generate_week_milestones(week: int) -> List[str]:
    """Generate milestones for a specific week"""
    milestones = [
        f"Completar {3 + week} horas de matemática",
        f"Resolver {10 + week * 5} exercícios",
        f"Revisar {2 + week} tópicos importantes"
    ]
    return milestones

def _generate_week_focus_areas(week: int) -> List[str]:
    """Generate focus areas for a specific week"""
    focus_rotation = [
        ["Álgebra", "Interpretação de texto"],
        ["Geometria", "Literatura"],
        ["Estatística", "Gramática"],
        ["Funções", "Redação"]
    ]
    return focus_rotation[week % len(focus_rotation)]

def _analyze_progress_and_adjust(request: ProgressUpdateRequest) -> List[str]:
    """Analyze progress and suggest adjustments"""
    adjustments = []
    
    for subject, hours in request.completed_hours.items():
        if hours < 5:  # Below expected progress
            adjustments.append(f"Aumentar horas de {subject} na próxima semana")
        elif hours > 15:  # Exceeding expected
            adjustments.append(f"Manter ritmo atual em {subject}")
    
    return adjustments

def _generate_adaptive_recommendations(request: ProgressUpdateRequest) -> List[str]:
    """Generate adaptive recommendations based on progress"""
    recommendations = [
        "Continue com a dedicação atual",
        "Ajuste o foco nas matérias com maior dificuldade"
    ]
    
    for subject, difficulty in request.difficulty_feedback.items():
        if difficulty == "hard":
            recommendations.append(f"Dedicar mais tempo a {subject} - considerar aula particular")
    
    return recommendations

def _analyze_performance(request: ProgressUpdateRequest) -> Dict[str, Any]:
    """Analyze student performance"""
    total_completed = sum(request.completed_hours.values())
    
    return {
        "total_hours_completed": total_completed,
        "average_daily_hours": round(total_completed / 7, 1),
        "consistency_score": "Alta" if total_completed > 20 else "Média",
        "subjects_on_track": len([h for h in request.completed_hours.values() if h >= 5]),
        "subjects_needing_attention": [s for s, h in request.completed_hours.items() if h < 5]
    }

def _determine_next_week_focus(request: ProgressUpdateRequest) -> List[str]:
    """Determine focus areas for next week"""
    focus_areas = []
    
    # Focus on subjects with low completion
    low_completion = [s for s, h in request.completed_hours.items() if h < 5]
    if low_completion:
        focus_areas.extend([f"Intensificar {subject}" for subject in low_completion[:2]])
    
    focus_areas.append("Manter simulados regulares")
    return focus_areas

def _calculate_completion_percentage(request: ProgressUpdateRequest) -> float:
    """Calculate completion percentage"""
    expected_hours_per_week = 25  # Example baseline
    total_completed = sum(request.completed_hours.values())
    return min((total_completed / expected_hours_per_week) * 100, 100.0)

def _generate_study_templates(intensity: Optional[str], duration_weeks: Optional[int], 
                            daily_hours: Optional[int]) -> List[StudyTemplate]:
    """Generate study templates"""
    templates = [
        StudyTemplate(
            template_id="enem_intensive_6m",
            name="ENEM Intensivo 6 Meses",
            description="Preparação completa e intensiva para o ENEM em 6 meses",
            target_audience="Vestibulandos dedicados",
            duration_weeks=24,
            intensity_level="intensive",
            subjects_covered=["Todas as matérias ENEM"],
            daily_hours_range="6-8 horas",
            success_rate="85%"
        ),
        StudyTemplate(
            template_id="enem_balanced_1y",
            name="ENEM Equilibrado 1 Ano",
            description="Preparação equilibrada ao longo de 1 ano",
            target_audience="Estudantes do 2º ano EM",
            duration_weeks=48,
            intensity_level="medium",
            subjects_covered=["Todas as matérias ENEM"],
            daily_hours_range="4-6 horas",
            success_rate="78%"
        )
    ]
    
    # Filter templates based on criteria
    filtered_templates = templates
    if intensity:
        filtered_templates = [t for t in filtered_templates if t.intensity_level == intensity]
    
    return filtered_templates

def _determine_recommended_template(intensity: Optional[str], duration_weeks: Optional[int], 
                                  daily_hours: Optional[int]) -> Optional[str]:
    """Determine recommended template based on criteria"""
    if intensity == "intensive" and duration_weeks and duration_weeks <= 26:
        return "enem_intensive_6m"
    elif intensity == "medium" or (duration_weeks and duration_weeks > 40):
        return "enem_balanced_1y"
    
    return None