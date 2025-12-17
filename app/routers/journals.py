from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import models
from app.schemas import schemas
from app.core import security
from app.dependencies import get_current_user 

router = APIRouter(prefix="/journals", tags=["Journals"])

@router.post("/", response_model=schemas.JournalOut)
def create_journal(
    journal: schemas.JournalCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    encrypted_title = security.encrypt_text(journal.title)
    encrypted_content = security.encrypt_text(journal.content)

    new_journal = models.Journal(
        title_encrypted=encrypted_title,
        content_encrypted=encrypted_content,
        iv="fernet_managed", 
        user_id=current_user.id
    )
    
    db.add(new_journal)
    db.commit()
    db.refresh(new_journal)

    return schemas.JournalOut(
        id=new_journal.id,
        title=journal.title,
        content=journal.content,
        created_at=new_journal.created_at
    )

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
                created_at=j.created_at
            ))
        except:
            continue
            
    return results