from fastapi import FastAPI
from app.routers import auth

app = FastAPI(
    title="serenaFlow API",
    description="API Kesehatan Mental & Jurnal Terenskripsi",
    version="1.0.0"
)

app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to SerenaFlow API", "status": "active"}