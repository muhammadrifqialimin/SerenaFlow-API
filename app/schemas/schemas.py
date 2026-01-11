from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)

class UserOut(BaseModel):
    id : int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class JournalCreate(BaseModel):
    title: str
    content: str

class JournalOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

class Config:
    from_attributes = True

class MoodCreate(BaseModel):
    score: int               # Wajib angka (1-10)
    tags: Optional[List[str]] = []  # List text

class MoodOut(BaseModel):
    id: int
    score: int
    tags: Optional[List[str]]
    created_at: datetime

    class Config:
        from_attributes = True

class MoodStats(BaseModel):
    total_logs: int
    average_score: float
    recent_trend: List[int]