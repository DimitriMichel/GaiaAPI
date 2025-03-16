# app/routers/insights.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db
from app.services.ai_service import AIService
from app.utils.auth import get_current_user

router = APIRouter(prefix="/insights", tags=["insights"])

@router.get("/analyze/{user_id}", response_model=schemas.AIInsight)
def analyze_user_data(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """
    Analyze user data to generate insights about mood patterns.
    Requires at least 7 days of data.
    """
    # Check if user is requesting their own data
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's data"
        )
    
    # Check if user has enough data
    log_count = db.query(models.DailyLog).filter(models.DailyLog.user_id == user_id).count()
    if log_count < 7:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User needs at least 7 days of data for analysis. Currently has {log_count} days."
        )
    
    # Generate insights
    ai_service = AIService()
    insight = ai_service.analyze_mood_patterns(user_id, db)
    
    if not insight:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate insights"
        )
    
    return insight

@router.get("/recommendations/{user_id}", response_model=List[schemas.ActivityRecommendation])
def get_recommendations(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """
    Get activity recommendations for a user.
    """
    # Check if user is requesting their own data
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's data"
        )
    
    # Get existing recommendations
    recommendations = db.query(models.ActivityRecommendation).filter(
        models.ActivityRecommendation.user_id == user_id
    ).all()
    
    return recommendations

@router.post("/recommendations/{user_id}", response_model=schemas.ActivityRecommendation)
def create_recommendation(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """
    Generate a new activity recommendation for a user.
    """

    # Check if user is requesting their own data
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's data"
        )
    
    # Generate recommendation
    ai_service = AIService()
    recommendation = ai_service.generate_activity_recommendation(user_id, db)
    
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate recommendation"
        )
    
    return recommendation