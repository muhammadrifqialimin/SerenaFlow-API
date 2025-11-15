from fastapi import FastAPI

app = FastAPI(
    title="SerenaFlow API",
    description="API untuk pelacak kesehatan mental dan jurnal terenkripsi.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Selamat datang di SerenaFlow API!",
            "status": "running",
            "tech_stack": "FastAPI + Python"
            }

@app.get("/health")
def health_check():
    return {"status": "ok"}