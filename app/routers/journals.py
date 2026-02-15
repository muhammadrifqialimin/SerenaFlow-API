from typing import List
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from deep_translator import GoogleTranslator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from app.core.database import get_db
from app.models import models
from app.schemas import schemas
from app.core import security
from app.dependencies import get_current_user
from app.core.email_utils import send_email_notification

router = APIRouter(prefix="/journals", tags=["Journals"])

@router.post("/", response_model=schemas.JournalOut)
async def create_journal(
    journal: schemas.JournalCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    encrypted_title = security.encrypt_text(journal.title)
    encrypted_content = security.encrypt_text(journal.content)

    try:
        translated_text = GoogleTranslator(source='auto', target='en').translate(journal.content)
    except:
        translated_text = journal.content

    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(translated_text)['compound']

    if score >= 0.05:
        mood_label = "Positive"
    elif score <= -0.05:
        mood_label = "Negative"
    else:
        mood_label = "Neutral"

    new_journal = models.Journal(
        title_encrypted=encrypted_title,
        content_encrypted=encrypted_content,
        iv="fernet_managed", 
        sentiment=mood_label,
        user_id=current_user.id
    )
    
    db.add(new_journal)
    db.commit()
    db.refresh(new_journal)

    email_subject = "Jurnal Baru Berhasil Disimpan! 📝"
    email_body = f"""
    <h3>Halo {current_user.email}!</h3>
    <p>Jurnal kamu hari ini berhasil disimpan dengan aman.</p>
    <p><b>Mood Terdeteksi:</b> {mood_label}</p>
    <br>
    <p>Tetap semangat menjalani hari!</p>
    <p><i>- SereneFlow Bot 🤖</i></p>
    """
    
    background_tasks.add_task(
        send_email_notification, 
        [current_user.email], 
        email_subject, 
        email_body
    )

    return schemas.JournalOut(
        id=new_journal.id,
        title=journal.title,
        content=journal.content,
        sentiment=mood_label,
        created_at=new_journal.created_at
    )

@router.get("/stats")
def get_journal_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    journals = db.query(models.Journal).filter(models.Journal.user_id == current_user.id).all()
    
    total = len(journals)
    pos = sum(1 for j in journals if j.sentiment == "Positive")
    neg = sum(1 for j in journals if j.sentiment == "Negative")
    neu = sum(1 for j in journals if j.sentiment == "Neutral")

    status = "No Data"
    if total > 0:
        if pos > neg and pos > neu:
            status = "Mostly Happy"
        elif neg > pos:
            status = "Mostly Sad/Tired"
        else:
            status = "Stable/Neutral"
            
    return {
        "total_entries": total,
        "summary": {
            "positive": pos,
            "negative": neg,
            "neutral": neu
        },
        "mood_analysis": status
    }

@router.get("/", response_model=List[schemas.JournalOut])
def read_journals(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    journals = db.query(models.Journal).filter(models.Journal.user_id == current_user.id).all()
    results = []

    for j in journals:
        try:
            decrypted_title = security.decrypt_text(j.title_encrypted)
            decrypted_content = security.decrypt_text(j.content_encrypted)
            
            results.append(schemas.JournalOut(
                id=j.id,
                title=decrypted_title,
                content=decrypted_content,
                sentiment=j.sentiment,
                created_at=j.created_at
            ))
        except:
            continue
            
    return results