from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Float, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False)
    daily_logs = relationship("DailyLog", back_populates="user")
    activity_recommendations = relationship("ActivityRecommendation", back_populates="user")

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    bio = Column(String(180), nullable=True)
    timezone = Column(String, default="UTC")
    activity_preferences = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")

class DailyLog(Base):
    __tablename__ = "daily_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime(timezone=True), default=datetime.utcnow)
    overall_mood = Column(Integer)  # 1-10 scale
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="daily_logs")
    food_entries = relationship("FoodEntry", back_populates="daily_log")
    exercise_entries = relationship("ExerciseEntry", back_populates="daily_log")
    work_entries = relationship("WorkEntry", back_populates="daily_log")
    event_entries = relationship("EventEntry", back_populates="daily_log")
    mood_entries = relationship("MoodEntry", back_populates="daily_log")
    ai_insights = relationship("AIInsight", back_populates="daily_log")

class MealType(enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"
    other = "other"

class FoodEntry(Base):
    __tablename__ = "food_entries"

    id = Column(Integer, primary_key=True, index=True)
    daily_log_id = Column(Integer, ForeignKey("daily_logs.id"))
    food_name = Column(String)
    description = Column(Text, nullable=True)
    meal_type = Column(Enum(MealType))
    calories = Column(Integer, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    daily_log = relationship("DailyLog", back_populates="food_entries")

class IntensityLevel(enum.Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    very_high = "very_high"

class ExerciseEntry(Base):
    __tablename__ = "exercise_entries"

    id = Column(Integer, primary_key=True, index=True)
    daily_log_id = Column(Integer, ForeignKey("daily_logs.id"))
    exercise_type = Column(String)
    description = Column(Text, nullable=True)
    duration_minutes = Column(Integer)
    intensity = Column(Enum(IntensityLevel))
    calories_burned = Column(Integer, nullable=True)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    daily_log = relationship("DailyLog", back_populates="exercise_entries")

class WorkEntry(Base):
    __tablename__ = "work_entries"

    id = Column(Integer, primary_key=True, index=True)
    daily_log_id = Column(Integer, ForeignKey("daily_logs.id"))
    description = Column(Text)
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    productivity_rating = Column(Integer)  # 1-10 scale
    stress_level = Column(Integer)  # 1-10 scale
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    daily_log = relationship("DailyLog", back_populates="work_entries")

class EventType(enum.Enum):
    social = "social"
    personal = "personal"
    professional = "professional"
    family = "family"
    health = "health"
    other = "other"

class EventEntry(Base):
    __tablename__ = "event_entries"

    id = Column(Integer, primary_key=True, index=True)
    daily_log_id = Column(Integer, ForeignKey("daily_logs.id"))
    description = Column(Text)
    event_type = Column(Enum(EventType))
    impact_rating = Column(Integer)  # -5 to +5 scale
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    daily_log = relationship("DailyLog", back_populates="event_entries")

class MoodEntry(Base):
    __tablename__ = "mood_entries"

    id = Column(Integer, primary_key=True, index=True)
    daily_log_id = Column(Integer, ForeignKey("daily_logs.id"))
    mood_rating = Column(Integer)  # 1-10 scale
    description = Column(Text, nullable=True)
    factors = Column(JSON, nullable=True)  
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    daily_log = relationship("DailyLog", back_populates="mood_entries")

class InsightType(enum.Enum):
    mood_correlation = "mood_correlation"
    habit_suggestion = "habit_suggestion"
    pattern_recognition = "pattern_recognition"
    general_observation = "general_observation"

class AIInsight(Base):
    __tablename__ = "ai_insights"

    id = Column(Integer, primary_key=True, index=True)
    daily_log_id = Column(Integer, ForeignKey("daily_logs.id"))
    insight_type = Column(Enum(InsightType))
    content = Column(Text)
    related_factors = Column(JSON, nullable=True)  # What factors contributed to this insight
    confidence_score = Column(Float, nullable=True)  # 0.0 to 1.0
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    daily_log = relationship("DailyLog", back_populates="ai_insights")

class ActivityRecommendation(Base):
    __tablename__ = "activity_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_name = Column(String)
    description = Column(Text)
    duration_minutes = Column(Integer)
    expected_benefit = Column(String)
    is_completed = Column(Boolean, default=False)
    user_rating = Column(Integer, nullable=True)  # 1-5 scale
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="activity_recommendations")