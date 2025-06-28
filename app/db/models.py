
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB # For PostgreSQL JSON support
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    study_plans = relationship("StudyPlan", back_populates="user")
    user_progress = relationship("UserProgress", back_populates="user")

class StudyPlan(Base):
    __tablename__ = "study_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    goals = Column(Text, nullable=True)
    plan_details = Column(JSONB, nullable=False) # Store the structured plan as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="study_plans")

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String, nullable=False) # e.g., "Matemática", "História"
    score = Column(Integer, nullable=True) # e.g., score in a quiz/simulado
    difficulty_level = Column(String, nullable=True) # e.g., "easy", "medium", "hard"
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="user_progress")
