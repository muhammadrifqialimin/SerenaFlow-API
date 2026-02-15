from fastapi import FastAPI
from app.routers import auth, journals, moods
from app.core.database import engine
from app.models import models
from app.core.scheduler import start_scheduler

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="serenaFlow API",
    description="API Kesehatan Mental & Jurnal Terenskripsi",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    start_scheduler()

app.include_router(auth.router)
app.include_router(journals.router)
app.include_router(moods.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to SerenaFlow API", "status": "active"}