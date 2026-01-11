from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import models
from app.schemas import schemas
from app.dependencies import get_current_user

router = APIRouter(prefix="/moods", tags=["Mood Tracker"])

@router.post("/", response_model=schemas.MoodOut)
def create_mood(
    mood_data: schemas.MoodCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # PERBAIKAN DI SINI: Gunakan score & tags, jangan mood!
    new_mood = models.MoodLog(
        score=mood_data.score,
        tags=mood_data.tags,
        user_id=current_user.id
    )
    db.add(new_mood)
    db.commit()
    db.refresh(new_mood)
    return new_mood

@router.get("/", response_model=List[schemas.MoodOut])
def get_moods(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.MoodLog).filter(models.MoodLog.user_id == current_user.id).all()

@router.get("/stats", response_model=schemas.MoodStats)
def get_mood_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    user_moods = db.query(models.MoodLog).filter(models.MoodLog.user_id == current_user.id).all()
    
    if not user_moods:
        return schemas.MoodStats(
            total_logs=0,
            average_score=0.0,
            recent_trend=[]
        )
    
    total = len(user_moods)
    
    total_score = sum(mood.score for mood in user_moods)
    average = total_score / total
    
    sorted_moods = sorted(user_moods, key=lambda x: x.created_at, reverse=True)
    trend = [m.score for m in sorted_moods[:5]]
    
    return schemas.MoodStats(
        total_logs=total,
        average_score=round(average, 1),
        recent_trend=trend
    )