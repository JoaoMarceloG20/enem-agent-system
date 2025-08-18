import uuid
from datetime import datetime
from typing import Optional, Dict, Any

from sqlmodel import Field, SQLModel, JSON, Column


# Base model for conversation sessions (compatible with PostgresAgentStorage)
class SessionBase(SQLModel):
    user_id: Optional[str] = Field(default=None, max_length=255)
    agent_id: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class SessionCreate(SessionBase):
    pass


class SessionUpdate(SQLModel):
    user_id: Optional[str] = Field(default=None, max_length=255)


# Database model
class Session(SessionBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


# Response model
class SessionPublic(SessionBase):
    id: uuid.UUID


# Base model for agent conversations
class ConversationBase(SQLModel):
    session_id: uuid.UUID = Field(foreign_key='session.id')
    message: str
    response: str
    model_used: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationCreate(ConversationBase):
    pass


# Database model
class Conversation(ConversationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


# Response model
class ConversationPublic(ConversationBase):
    id: uuid.UUID


# Generic message model
class Message(SQLModel):
    message: str


# ENEM-specific models

# Quiz Results Model
class QuizResultBase(SQLModel):
    user_id: str = Field(max_length=255)
    agent_id: str = Field(default='quiz', max_length=100)
    subject: str = Field(max_length=100)  # matematica, portugues, etc.
    topic: Optional[str] = Field(default=None, max_length=200)
    difficulty: str = Field(max_length=50)  # facil, medio, dificil
    num_questions: int
    correct_answers: int
    total_score: float
    time_taken: Optional[int] = Field(default=None)  # seconds
    questions_data: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)


class QuizResultCreate(QuizResultBase):
    pass


class QuizResult(QuizResultBase, table=True):
    __tablename__ = 'enem_quiz_results'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class QuizResultPublic(QuizResultBase):
    id: uuid.UUID


# Essay Grades Model
class EssayGradeBase(SQLModel):
    user_id: str = Field(max_length=255)
    agent_id: str = Field(default='essay_grader', max_length=100)
    theme: str = Field(max_length=500)
    essay_text: str
    competencia_1: int = Field(ge=0, le=200)
    competencia_2: int = Field(ge=0, le=200)
    competencia_3: int = Field(ge=0, le=200)
    competencia_4: int = Field(ge=0, le=200)
    competencia_5: int = Field(ge=0, le=200)
    total_score: int = Field(ge=0, le=1000)
    feedback: str
    word_count: int
    created_at: datetime = Field(default_factory=datetime.utcnow)


class EssayGradeCreate(EssayGradeBase):
    pass


class EssayGrade(EssayGradeBase, table=True):
    __tablename__ = 'enem_essay_grades'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class EssayGradePublic(EssayGradeBase):
    id: uuid.UUID


# Study Plans Model
class StudyPlanBase(SQLModel):
    user_id: str = Field(max_length=255)
    agent_id: str = Field(default='study_plan', max_length=100)
    plan_name: str = Field(max_length=200)
    subjects: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))  # list of subjects
    duration_weeks: int
    intensity: str = Field(max_length=50)  # light, moderate, intensive, extreme
    target_date: Optional[datetime] = Field(default=None)
    weekly_hours: int
    plan_data: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))  # detailed plan structure
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


class StudyPlanCreate(StudyPlanBase):
    pass


class StudyPlanUpdate(SQLModel):
    plan_name: Optional[str] = Field(default=None, max_length=200)
    is_active: Optional[bool] = Field(default=None)
    plan_data: Optional[Dict[str, Any]] = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class StudyPlan(StudyPlanBase, table=True):
    __tablename__ = 'enem_study_plans'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class StudyPlanPublic(StudyPlanBase):
    id: uuid.UUID


# User Progress Model
class UserProgressBase(SQLModel):
    user_id: str = Field(max_length=255)
    subject: str = Field(max_length=100)
    topic: Optional[str] = Field(default=None, max_length=200)
    progress_type: str = Field(max_length=50)  # quiz, essay, study_session, etc.
    progress_data: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    score: Optional[float] = Field(default=None)
    completion_percentage: Optional[float] = Field(default=None, ge=0, le=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserProgressCreate(UserProgressBase):
    pass


class UserProgress(UserProgressBase, table=True):
    __tablename__ = 'enem_user_progress'
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class UserProgressPublic(UserProgressBase):
    id: uuid.UUID
