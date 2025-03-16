from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, date

from .. import models, schemas
from ..database import get_db
from ..utils.auth import get_current_user

router = APIRouter(prefix="/daily-logs", tags=["daily logs"])

@router.post("/", response_model=schemas.DailyLog, status_code=status.HTTP_201_CREATED)
def create_daily_log(
    log: schemas.DailyLogCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Create a new daily log for the current user."""
    # Check if user already has a log for this date
    log_date = log.date or datetime.utcnow()
    existing_log = db.query(models.DailyLog).filter(
        models.DailyLog.user_id == current_user.id,
        models.DailyLog.date == log_date.date()
    ).first()
    
    if existing_log:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A log for this date already exists"
        )
    
    # Create new log
    db_log = models.DailyLog(
        **log.dict(),
        user_id=current_user.id
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/", response_model=List[schemas.DailyLog])
def read_daily_logs(
    skip: int = 0, 
    limit: int = 100, 
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Get all daily logs for the current user with optional date filtering."""
    query = db.query(models.DailyLog).filter(models.DailyLog.user_id == current_user.id)
    
    if start_date:
        query = query.filter(models.DailyLog.date >= start_date)
    if end_date:
        query = query.filter(models.DailyLog.date <= end_date)
    
    logs = query.order_by(models.DailyLog.date.desc()).offset(skip).limit(limit).all()
    return logs

@router.get("/{log_id}", response_model=schemas.DailyLogWithInsights)
def read_daily_log(
    log_id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Get a specific daily log by ID."""
    log = db.query(models.DailyLog).filter(models.DailyLog.id == log_id).first()
    if log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    if log.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this log")
    return log

@router.put("/{log_id}", response_model=schemas.DailyLog)
def update_daily_log(
    log_id: int, 
    log_update: schemas.DailyLogCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Update a daily log."""
    db_log = db.query(models.DailyLog).filter(models.DailyLog.id == log_id).first()
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    if db_log.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this log")
    
    # Update log fields
    for key, value in log_update.dict().items():
        setattr(db_log, key, value)
    
    db.commit()
    db.refresh(db_log)
    return db_log

@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_daily_log(
    log_id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    """Delete a daily log."""
    db_log = db.query(models.DailyLog).filter(models.DailyLog.id == log_id).first()
    if db_log is None:
        raise HTTPException(status_code=404, detail="Log not found")
    if db_log.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this log")
    
    db.delete(db_log)
    db.commit()
    return None