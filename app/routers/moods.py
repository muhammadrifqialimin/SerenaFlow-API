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