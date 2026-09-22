from fastapi import FastAPI
from .auth.models import User

USERS: dict[str, User] = {}
DOCUMENTS: list[dict] = [
    {"document_id": "doc-a", "tenant_id": "tenant-a", "owner_id": "user-a", "access_level": "shared", "created_at": "2026-01-01", "content": "Company A policy: support hours are nine to five."},
    {"document_id": "doc-b", "tenant_id": "tenant-b", "owner_id": "user-b", "access_level": "shared", "created_at": "2026-01-01", "content": "Company B policy: internal support process."},
]
CONVERSATIONS: dict[str, dict] = {}

app = FastAPI(title="Day 20 Secure AI Assistant", version="1.0.0")
from .auth.routes import router as auth_router
from .api.chat import router as chat_router
from .api.conversations import router as conversations_router
from .api.documents import router as documents_router
from .api.jobs import router as jobs_router
from .core.health import router as health_router
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(conversations_router)
app.include_router(documents_router)
app.include_router(jobs_router)
app.include_router(health_router)
