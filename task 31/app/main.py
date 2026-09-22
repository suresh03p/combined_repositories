from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from app.settings import settings


app = FastAPI(title="Production AI API", version="1.0.0")


class LoginRequest(BaseModel):
    username: str
    password: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class RagRequest(BaseModel):
    query: str = Field(min_length=1, max_length=4000)


class JobResponse(BaseModel):
    job_id: str
    status: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/ready")
def ready() -> dict[str, str]:
    return {"status": "ready", "environment": settings.app_env}


@app.post("/auth/login")
def login(payload: LoginRequest) -> dict[str, str]:
    if not payload.username or not payload.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": f"local-{uuid4()}", "token_type": "bearer"}


@app.post("/chat")
def chat(payload: ChatRequest) -> dict[str, str]:
    return {
        "response": f"Configured AI provider would answer: {payload.message}",
        "model": settings.llm_model,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/rag/query")
def rag_query(payload: RagRequest) -> dict[str, object]:
    return {
        "answer": f"No external vector store is configured. Query received: {payload.query}",
        "sources": [],
    }


@app.get("/jobs/{job_id}", response_model=JobResponse)
def get_job(job_id: str) -> JobResponse:
    if not job_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return JobResponse(job_id=job_id, status="completed")
