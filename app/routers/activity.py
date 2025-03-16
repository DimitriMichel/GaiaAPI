# app/routers/activity.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db
from ..utils.auth import get_current_user
from ..services.ai_service import AIService

router = APIRouter(prefix="/activities", tags=["activities"])

@router.get("/recommendations", response_model=List[schemas.ActivityRecommendation])
def get_activity_recommendations(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Get activity recommendations for the current user."""
    recommendations = db.query(models.ActivityRecommendation).filter(
        models.ActivityRecommendation.user_id == current_user.id
    ).order_by(models.ActivityRecommendation.created_at.desc()).all()
    
    return recommendations

@router.post("/recommendations", response_model=schemas.ActivityRecommendation)
def generate_recommendation(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Generate a new activity recommendation for the current user."""
    ai_service = AIService()
    recommendation = ai_service.generate_activity_recommendation(current_user.id, db)
    
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate recommendation"
        )
    
    return recommendation

@router.put("/recommendations/{recommendation_id}", response_model=schemas.ActivityRecommendation)
def update_recommendation_status(
    recommendation_id: int,
    update_data: schemas.ActivityRecommendationUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Update a recommendation (mark as completed, add rating)."""
    recommendation = db.query(models.ActivityRecommendation).filter(
        models.ActivityRecommendation.id == recommendation_id
    ).first()
    
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )
    
    # Check if user owns this recommendation
    if recommendation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this recommendation"
        )
    
    # Update fields
    if update_data.is_completed is not None:
        recommendation.is_completed = update_data.is_completed
    
    if update_data.user_rating is not None:
        recommendation.user_rating = update_data.user_rating
    
    db.commit()
    db.refresh(recommendation)
    
    return recommendation