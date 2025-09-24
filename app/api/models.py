"""
API Response Models

Modelos Pydantic para estruturar as respostas das APIs do sistema.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Union
from enum import Enum

from pydantic import BaseModel, Field


class StatusEnum(str, Enum):
    """Status enumeration for responses"""
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"


class AgentTypeEnum(str, Enum):
    """Available agent types"""
    TEST = "test_enem"
    TUTOR = "tutor"
    QUIZ = "quiz"
    ESSAY = "essay_grader"
    STUDY_PLAN = "study_plan"
    ORCHESTRATOR = "orchestrator"


class SubjectEnum(str, Enum):
    """ENEM subjects"""
    MATEMATICA = "matematica"
    PORTUGUES = "portugues"
    LITERATURA = "literatura"
    INGLES = "ingles"
    ESPANHOL = "espanhol"
    FISICA = "fisica"
    QUIMICA = "quimica"
    BIOLOGIA = "biologia"
    HISTORIA = "historia"
    GEOGRAFIA = "geografia"
    FILOSOFIA = "filosofia"
    SOCIOLOGIA = "sociologia"
    REDACAO = "redacao"


class DifficultyEnum(str, Enum):
    """Quiz difficulty levels"""
    FACIL = "facil"
    MEDIO = "medio"
    DIFICIL = "dificil"


class IntensityEnum(str, Enum):
    """Study plan intensity levels"""
    LIGHT = "light"
    MODERATE = "moderate"
    INTENSIVE = "intensive"
    EXTREME = "extreme"


# Base Response Models
class BaseResponse(BaseModel):
    """Base response model"""
    status: StatusEnum
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(BaseResponse):
    """Error response model"""
    status: StatusEnum = StatusEnum.ERROR
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


# Health Check Models
class HealthCheckResponse(BaseResponse):
    """Health check response model"""
    status: StatusEnum = StatusEnum.SUCCESS
    message: str = "Edtech Agent API is running"
    services: Optional[Dict[str, bool]] = None
    version: Optional[str] = None


# Agent Info Models
class AgentInfo(BaseModel):
    """Agent information model"""
    agent_id: str
    name: str
    description: str
    supports_subject: bool = False
    supports_difficulty: bool = False
    supports_intensity: bool = False
    temperature: float
    max_tokens: int
    subjects: Optional[List[str]] = None
    difficulties: Optional[List[str]] = None
    intensities: Optional[List[str]] = None
    features: Optional[List[str]] = None


class AgentListResponse(BaseResponse):
    """Response for listing agents"""
    status: StatusEnum = StatusEnum.SUCCESS
    agents: List[str]
    total_count: int


class AgentInfoResponse(BaseResponse):
    """Response for agent information"""
    status: StatusEnum = StatusEnum.SUCCESS
    agents: Dict[str, AgentInfo]


# Agent Creation Models
class AgentCreationRequest(BaseModel):
    """Request model for agent creation"""
    agent_id: AgentTypeEnum
    subject: Optional[SubjectEnum] = None
    difficulty: Optional[DifficultyEnum] = None
    intensity: Optional[IntensityEnum] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    debug_mode: bool = True


class AgentCreationResponse(BaseResponse):
    """Response for agent creation"""
    status: StatusEnum = StatusEnum.SUCCESS
    agent_id: str
    agent_name: str
    session_id: str
    created_at: datetime = Field(default_factory=datetime.now)
    configuration: Dict[str, Any]


# Agent Run Models
class AgentRunRequest(BaseModel):
    """Request model for agent execution"""
    message: str = Field(..., min_length=1, max_length=10000)
    stream: bool = False
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class AgentRunMetadata(BaseModel):
    """Metadata for agent run"""
    agent_id: str
    agent_name: str
    model_used: str
    temperature: float
    max_tokens: int
    tokens_used: Optional[int] = None
    processing_time_ms: Optional[int] = None
    subject: Optional[str] = None
    difficulty: Optional[str] = None
    intensity: Optional[str] = None


class AgentRunResponse(BaseResponse):
    """Response for agent execution"""
    status: StatusEnum = StatusEnum.SUCCESS
    content: str
    metadata: AgentRunMetadata
    session_id: str
    run_id: Optional[str] = None


# Quiz Specific Models
class QuizQuestion(BaseModel):
    """Quiz question model with complete ENEM structure"""
    question_id: str = Field(..., description="Unique identifier for the question")
    context: str = Field(..., description="Contextual text or situation for the question")
    command: str = Field(..., description="The specific question being asked")
    alternatives: Dict[str, str] = Field(..., description="5 alternatives A-E")
    correct_answer: str = Field(..., pattern="^[A-E]$", description="Correct answer letter")
    explanation: str = Field(..., description="Detailed explanation of the correct answer")
    topic: str = Field(..., description="Main topic covered by the question")
    difficulty: DifficultyEnum = Field(..., description="Question difficulty level")
    subject: SubjectEnum = Field(..., description="Academic subject")

    # Legacy field for backward compatibility
    question_text: Optional[str] = Field(None, description="Deprecated: use command instead")

    def model_post_init(self, __context):
        """Ensure backward compatibility"""
        if self.question_text and not self.command:
            self.command = self.question_text
        elif not self.question_text and self.command:
            self.question_text = self.command


class QuizResponse(AgentRunResponse):
    """Response for quiz generation with auto-generated content"""
    questions: List[QuizQuestion] = Field(..., description="Structured quiz questions")
    quiz_metadata: Optional[Dict[str, Any]] = None

    def model_post_init(self, __context):
        """Auto-generate content from structured questions"""
        if self.questions and not self.content:
            self.content = self._generate_content_from_questions()

    def _generate_content_from_questions(self) -> str:
        """Generate markdown content from structured questions"""
        if not self.questions:
            return ""

        content_parts = []

        for i, question in enumerate(self.questions, 1):
            content_parts.append(f"## Questão {i}")
            content_parts.append("")

            if question.context:
                content_parts.append(f"**Contexto:** {question.context}")
                content_parts.append("")

            content_parts.append(f"**Comando:** {question.command}")
            content_parts.append("")

            # Add alternatives
            for letter, alternative in sorted(question.alternatives.items()):
                content_parts.append(f"{letter}) {alternative}")
            content_parts.append("")

            # Add answer and explanation
            content_parts.append(f"**Gabarito:** {question.correct_answer}")
            content_parts.append(f"**Explicação:** {question.explanation}")
            content_parts.append(f"**Tópico:** {question.topic}")
            content_parts.append(f"**Dificuldade:** {question.difficulty}")
            content_parts.append("")
            content_parts.append("---")
            content_parts.append("")

        return "\n".join(content_parts)


# Essay Grading Models
class EssayCompetency(BaseModel):
    """Essay competency grading"""
    competency_number: int
    competency_name: str
    score: int = Field(..., ge=0, le=200)
    feedback: str
    strengths: List[str] = []
    improvements: List[str] = []


class EssayGradeResponse(AgentRunResponse):
    """Response for essay grading"""
    total_score: Optional[int] = Field(None, ge=0, le=1000)
    competencies: Optional[List[EssayCompetency]] = None
    general_feedback: Optional[str] = None
    suggestions: Optional[List[str]] = None


# Study Plan Models
class StudySession(BaseModel):
    """Study session model"""
    day: str
    time_slot: str
    subject: str
    duration_hours: float
    activities: List[str]
    priority: str = "medium"


class WeeklyPlan(BaseModel):
    """Weekly study plan"""
    week_number: int
    total_hours: float
    sessions: List[StudySession]
    goals: List[str]
    milestones: List[str]


class StudyPlanResponse(AgentRunResponse):
    """Response for study plan creation"""
    plan_id: Optional[str] = None
    intensity: Optional[IntensityEnum] = None
    total_weeks: Optional[int] = None
    hours_per_week: Optional[float] = None
    subject_distribution: Optional[Dict[str, float]] = None
    weekly_plans: Optional[List[WeeklyPlan]] = None
    phases: Optional[List[Dict[str, Any]]] = None


# Tutor Specific Models
class TutorResponse(AgentRunResponse):
    """Response for tutor interaction"""
    concept_explained: Optional[str] = None
    related_topics: Optional[List[str]] = None
    examples: Optional[List[str]] = None
    practice_suggestions: Optional[List[str]] = None


# Subject and Utility Models
class SubjectListResponse(BaseResponse):
    """Response for subject listing"""
    status: StatusEnum = StatusEnum.SUCCESS
    subjects: List[Dict[str, str]]  # [{"key": "matematica", "name": "Matemática e suas Tecnologias"}]


class TopicListResponse(BaseResponse):
    """Response for topic listing"""
    status: StatusEnum = StatusEnum.SUCCESS
    subject: str
    topics: List[str]


class DifficultyListResponse(BaseResponse):
    """Response for difficulty listing"""
    status: StatusEnum = StatusEnum.SUCCESS
    difficulties: List[Dict[str, str]]  # [{"key": "facil", "description": "Fácil - Conceitos básicos"}]


class IntensityListResponse(BaseResponse):
    """Response for intensity listing"""
    status: StatusEnum = StatusEnum.SUCCESS
    intensities: List[Dict[str, str]]


# Streaming Response Models
class StreamChunk(BaseModel):
    """Streaming response chunk"""
    chunk_id: int
    content: str
    is_final: bool = False
    metadata: Optional[Dict[str, Any]] = None


class StreamResponse(BaseResponse):
    """Response for streaming"""
    status: StatusEnum = StatusEnum.SUCCESS
    stream_id: str
    chunks: List[StreamChunk]


# Validation Error Model
class ValidationErrorDetail(BaseModel):
    """Validation error detail"""
    field: str
    message: str
    invalid_value: Any


class ValidationErrorResponse(ErrorResponse):
    """Validation error response"""
    error_code: str = "VALIDATION_ERROR"
    validation_errors: List[ValidationErrorDetail]


# Agent State Models
class AgentSessionInfo(BaseModel):
    """Agent session information"""
    session_id: str
    agent_id: str
    created_at: datetime
    last_interaction: datetime
    total_interactions: int
    current_state: Dict[str, Any]


class AgentSessionListResponse(BaseResponse):
    """Response for agent session listing"""
    status: StatusEnum = StatusEnum.SUCCESS
    sessions: List[AgentSessionInfo]
    total_count: int


# Performance and Analytics Models
class PerformanceMetrics(BaseModel):
    """Performance metrics model"""
    total_requests: int
    avg_response_time_ms: float
    success_rate: float
    error_rate: float
    agents_usage: Dict[str, int]
    peak_hours: List[str]


class AnalyticsResponse(BaseResponse):
    """Analytics response"""
    status: StatusEnum = StatusEnum.SUCCESS
    period_start: datetime
    period_end: datetime
    metrics: PerformanceMetrics


# Export all models for easy import
__all__ = [
    # Base
    "BaseResponse",
    "ErrorResponse",
    "ValidationErrorResponse",
    "ValidationErrorDetail",

    # Enums
    "StatusEnum",
    "AgentTypeEnum",
    "SubjectEnum",
    "DifficultyEnum",
    "IntensityEnum",

    # Health
    "HealthCheckResponse",

    # Agent Info
    "AgentInfo",
    "AgentListResponse",
    "AgentInfoResponse",

    # Agent Creation
    "AgentCreationRequest",
    "AgentCreationResponse",

    # Agent Run
    "AgentRunRequest",
    "AgentRunResponse",
    "AgentRunMetadata",

    # Specific Responses
    "QuizResponse",
    "QuizQuestion",
    "EssayGradeResponse",
    "EssayCompetency",
    "StudyPlanResponse",
    "StudySession",
    "WeeklyPlan",
    "TutorResponse",

    # Utility
    "SubjectListResponse",
    "TopicListResponse",
    "DifficultyListResponse",
    "IntensityListResponse",

    # Streaming
    "StreamResponse",
    "StreamChunk",

    # Sessions
    "AgentSessionInfo",
    "AgentSessionListResponse",

    # Analytics
    "PerformanceMetrics",
    "AnalyticsResponse",
]
