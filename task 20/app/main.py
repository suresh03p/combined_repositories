from fastapi import FastAPI
from app.api import auth, chat, documents
from app.core.config import DATA_DIR
from app.core.logging import configure_logging
from app.database.vector_store import healthy

configure_logging()
app = FastAPI(title="Day 14 Production RAG API", version="1.0.0")
app.include_router(documents.router)
app.include_router(chat.router)
app.include_router(auth.router)

@app.on_event("startup")
def startup() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/health", tags=["health"])
def health():
    return {"status": "healthy"}

@app.get("/health/vector-db", tags=["health"])
def vector_db_health():
    return {"status": "healthy" if healthy() else "unhealthy"}

@app.get("/health/llm", tags=["health"])
def llm_health():
    return {"status": "healthy", "provider": "offline-demo"}
