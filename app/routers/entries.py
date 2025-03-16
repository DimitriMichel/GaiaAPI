# app/routers/entries.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db
from ..utils.auth import get_current_user

router = APIRouter(tags=["entries"])

# Food Entries
@router.post("/daily-logs/{log_id}/food", response_model=schemas.FoodEntry, status_code=status.HTTP_201_CREATED)
def create_food_entry(
    log_id: int,
    entry: schemas.FoodEntryCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Add a food entry to a daily log."""
    # Verify log exists and belongs to user
    log = db.query(models.DailyLog).filter(models.DailyLog.id == log_id).first()
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    if log.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this log")
    
    # Create food entry
    db_entry = models.FoodEntry(**entry.dict(), daily_log_id=log_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.get("/daily-logs/{log_id}/food", response_model=List[schemas.FoodEntry])
def read_food_entries(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Get all food entries for a daily log."""
    # Verify log exists and belongs to user
    log = db.query(models.DailyLog).filter(models.DailyLog.id == log_id).first()
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    if log.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this log")
    
    entries = db.query(models.FoodEntry).filter(models.FoodEntry.daily_log_id == log_id).all()
    return entries

# Exercise Entries
@router.post("/daily-logs/{log_id}/exercise", response_model=schemas.ExerciseEntry, status_code=status.HTTP_201_CREATED)
def create_exercise_entry(
    log_id: int,
    entry: schemas.ExerciseEntryCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Add an exercise entry to a daily log."""
    # Verify log exists and belongs to user
    log = db.query(models.DailyLog).filter(models.DailyLog.id == log_id).first()
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    if log.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this log")
    
    # Create exercise entry
    db_entry = models.ExerciseEntry(**entry.dict(), daily_log_id=log_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.get("/daily-logs/{log_id}/exercise", response_model=List[schemas.ExerciseEntry])
def read_exercise_entries(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Get all exercise entries for a daily log."""
    # Verify log exists and belongs to user
    log = db.query(models.DailyLog).filter(models.DailyLog.id == log_id).first()
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    if log.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this log")
    
    entries = db.query(models.ExerciseEntry).filter(models.ExerciseEntry.daily_log_id == log_id).all()
    return entries

# Work Entries
@router.post("/daily-logs/{log_id}/work", response_model=schemas.WorkEntry, status_code=status.HTTP_201_CREATED)
def create_work_entry(
    log_id: int,
    entry: schemas.WorkEntryCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Add a work entry to a daily log."""
    # Verify log exists and belongs to user
    log = db.query(models.DailyLog).filter(models.DailyLog.id == log_id).first()
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    if log.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this log")
    
    # Create work entry
    db_entry = models.WorkEntry(**entry.dict(), daily_log_id=log_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

# Event Entries
@router.post("/daily-logs/{log_id}/events", response_model=schemas.EventEntry, status_code=status.HTTP_201_CREATED)
def create_event_entry(
    log_id: int,
    entry: schemas.EventEntryCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Add an event entry to a daily log."""
    # Verify log exists and belongs to user
    log = db.query(models.DailyLog).filter(models.DailyLog.id == log_id).first()
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    if log.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this log")
    
    # Create event entry
    db_entry = models.EventEntry(**entry.dict(), daily_log_id=log_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry

# Mood Entries
@router.post("/daily-logs/{log_id}/mood", response_model=schemas.MoodEntry, status_code=status.HTTP_201_CREATED)
def create_mood_entry(
    log_id: int,
    entry: schemas.MoodEntryCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Add a mood entry to a daily log."""
    # Verify log exists and belongs to user
    log = db.query(models.DailyLog).filter(models.DailyLog.id == log_id).first()
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    if log.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this log")
    
    # Create mood entry
    db_entry = models.MoodEntry(**entry.dict(), daily_log_id=log_id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry