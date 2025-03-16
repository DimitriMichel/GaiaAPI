from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from enum import Enum

class MealTypeEnum(str, Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"
    snack = "snack"
    other = "other"

class IntensityLevelEnum(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    very_high = "very_high"

class EventTypeEnum(str, Enum):
    social = "social"
    personal = "personal"
    professional = "professional"
    family = "family"
    health = "health"
    other = "other"

class InsightTypeEnum(str, Enum):
    mood_correlation = "mood_correlation"
    habit_suggestion = "habit_suggestion"
    pattern_recognition = "pattern_recognition"
    general_observation = "general_observation"

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str   

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Profile schemas
class ProfileBase(BaseModel):
    bio: Optional[str] = Field(None, max_length=180)
    timezone: Optional[str] = "UTC"
    activity_preferences: Optional[Dict[str, Any]] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Food Entry schemas
class FoodEntryBase(BaseModel):
    food_name: str
    description: Optional[str] = None
    meal_type: MealTypeEnum
    calories: Optional[int] = None
    timestamp: Optional[datetime] = None

class FoodEntryCreate(FoodEntryBase):
    pass

class FoodEntry(FoodEntryBase):
    id: int
    daily_log_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Exercise Entry schemas
class ExerciseEntryBase(BaseModel):
    exercise_type: str
    description: Optional[str] = None
    duration_minutes: int
    intensity: IntensityLevelEnum
    calories_burned: Optional[int] = None
    timestamp: Optional[datetime] = None

class ExerciseEntryCreate(ExerciseEntryBase):
    pass

class ExerciseEntry(ExerciseEntryBase):
    id: int
    daily_log_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Work Entry schemas
class WorkEntryBase(BaseModel):
    description: str
    start_time: datetime
    end_time: datetime
    productivity_rating: int = Field(..., ge=1, le=10)
    stress_level: int = Field(..., ge=1, le=10)

    @validator('end_time')
    def end_time_after_start_time(cls, v, values):
        if 'start_time' in values and v < values['start_time']:
            raise ValueError('end_time must be after start_time')
        return v

class WorkEntryCreate(WorkEntryBase):
    pass

class WorkEntry(WorkEntryBase):
    id: int
    daily_log_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Event Entry schemas
class EventEntryBase(BaseModel):
    description: str
    event_type: EventTypeEnum
    impact_rating: int = Field(..., ge=-5, le=5)
    timestamp: Optional[datetime] = None

class EventEntryCreate(EventEntryBase):
    pass

class EventEntry(EventEntryBase):
    id: int
    daily_log_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Mood Entry schemas
class MoodEntryBase(BaseModel):
    mood_rating: int = Field(..., ge=1, le=10)
    description: Optional[str] = None
    factors: Optional[Dict[str, Any]] = None
    timestamp: Optional[datetime] = None

class MoodEntryCreate(MoodEntryBase):
    pass

class MoodEntry(MoodEntryBase):
    id: int
    daily_log_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Daily Log schemas
class DailyLogBase(BaseModel):
    date: Optional[datetime] = None
    overall_mood: int = Field(..., ge=1, le=10)
    notes: Optional[str] = None

class DailyLogCreate(DailyLogBase):
    pass

class DailyLog(DailyLogBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    food_entries: List[FoodEntry] = []
    exercise_entries: List[ExerciseEntry] = []
    work_entries: List[WorkEntry] = []
    event_entries: List[EventEntry] = []
    mood_entries: List[MoodEntry] = []

    class Config:
        orm_mode = True

# AI Insight schemas
class AIInsightBase(BaseModel):
    insight_type: InsightTypeEnum
    content: str
    related_factors: Optional[Dict[str, Any]] = None
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)

class AIInsightCreate(AIInsightBase):
    pass

class AIInsight(AIInsightBase):
    id: int
    daily_log_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Activity Recommendation schemas
class ActivityRecommendationBase(BaseModel):
    activity_name: str
    description: str
    duration_minutes: int
    expected_benefit: str

class ActivityRecommendationCreate(ActivityRecommendationBase):
    pass

class ActivityRecommendationUpdate(BaseModel):
    is_completed: Optional[bool] = None
    user_rating: Optional[int] = Field(None, ge=1, le=5)

class ActivityRecommendation(ActivityRecommendationBase):
    id: int
    user_id: int
    is_completed: bool
    user_rating: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True

# Combined schemas for nested responses
class UserWithProfile(User):
    profile: Optional[Profile] = None

    class Config:
        orm_mode = True

class DailyLogWithInsights(DailyLog):
    ai_insights: List[AIInsight] = []

    class Config:
        orm_mode = True

class UserComplete(UserWithProfile):
    daily_logs: List[DailyLog] = []
    activity_recommendations: List[ActivityRecommendation] = []

    class Config:
        orm_mode = True
