from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.conversations import router as conversations_router
from app.api.documents import router as documents_router
from app.api.jobs import router as jobs_router
from app.core.health import health_report
from app.database import init_db

app = FastAPI(title="Production AI Assistant", version="1.0.0")
app.include_router(chat_router)
app.include_router(conversations_router)
app.include_router(documents_router)
app.include_router(jobs_router)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
def root() -> dict[str, str]:
    return {"status": "success", "message": "AI API is running"}


@app.get("/health")
def health() -> dict[str, str]:
    return health_report()


@app.get("/health/database")
def database_health() -> dict[str, str]:
    return {"database": health_report()["database"]}


@app.get("/health/redis")
def redis_health() -> dict[str, str]:
    return {"redis": health_report()["redis"]}


@app.get("/health/ai")
def ai_health() -> dict[str, str]:
    return {"ai_service": health_report()["ai_service"]}
