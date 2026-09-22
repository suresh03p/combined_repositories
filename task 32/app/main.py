from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Production AI API", version="1.0.0")


class HealthResponse(BaseModel):
    status: str = Field(..., examples=["healthy"]) 


class AuthRequest(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)


class ChatRequest(BaseModel):
    message: str = Field(...)
    user_id: str | None = None


class RAGRequest(BaseModel):
    query: str = Field(...)
    limit: int = Field(default=3, ge=1, le=10)


@app.get("/health", response_model=HealthResponse)
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/ready", response_model=HealthResponse)
def readiness() -> dict[str, str]:
    return {"status": "ready"}


@app.post("/auth/login")
def login(payload: AuthRequest) -> dict[str, Any]:
    if payload.username.lower() == "admin" and payload.password == "secret123":
        return {"token": "demo-token", "user": payload.username}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


@app.post("/chat")
def chat(payload: ChatRequest) -> dict[str, Any]:
    if not payload.message.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message cannot be empty")
    return {
        "reply": f"AI response to: {payload.message.strip()}",
        "user_id": payload.user_id or "anonymous",
        "status": "ok",
    }


@app.post("/rag/query")
def rag_query(payload: RAGRequest) -> dict[str, Any]:
    if not payload.query.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Query cannot be empty")
    return {
        "query": payload.query.strip(),
        "limit": payload.limit,
        "results": [
            {"id": 1, "text": "RAG: supporting context from knowledge base"},
            {"id": 2, "text": "RAG: retrieved from indexed documents"},
        ][: payload.limit],
        "status": "ok",
    }


@app.get("/redis/status")
def redis_status() -> dict[str, Any]:
    return {"redis": "working", "status": "ok"}


@app.get("/validate")
def validate_input() -> dict[str, str]:
    return {"status": "validated"}


@app.get("/error-demo")
def error_demo() -> None:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Simulated backend failure")
