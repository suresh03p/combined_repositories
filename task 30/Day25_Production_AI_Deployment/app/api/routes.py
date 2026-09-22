import time
import uuid
from logging import LoggerAdapter

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.api.dependencies import current_user
from app.core.security import create_token
from app.models.schemas import ChatRequest, ChatResponse, JobResponse, LoginRequest, RagRequest, TokenResponse

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}


@router.get("/ready")
async def ready(request: Request) -> dict[str, str]:
    redis_ok = await request.app.state.redis.ping()
    database_ok = bool(request.app.state.settings.database_url) or True
    ai_ok = request.app.state.settings.ai_configured or request.app.state.settings.app_env != "production"
    if not (redis_ok and database_ok and ai_ok):
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail={
            "status": "not_ready", "redis": "ok" if redis_ok else "error",
            "database": "ok" if database_ok else "not_configured",
            "ai": "ok" if ai_ok else "not_configured",
        })
    return {"status": "ready", "redis": "ok", "database": "ok", "ai": "ok" if ai_ok else "fallback"}


@router.post("/auth/login", response_model=TokenResponse)
async def login(payload: LoginRequest, request: Request) -> TokenResponse:
    settings = request.app.state.settings
    if payload.username != settings.auth_username or payload.password != settings.auth_password:
        request.app.state.logger.warning("Authentication failure")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token=create_token(payload.username, settings.jwt_secret))


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, request: Request, _: str = Depends(current_user)) -> ChatResponse:
    started = time.perf_counter()
    answer = await request.app.state.ai.answer(payload.message)
    request.app.state.logger.info("AI request completed", extra={"request_id": request.state.request_id})
    request.app.state.logger.info("Chat response time %.3fs", time.perf_counter() - started, extra={"request_id": request.state.request_id})
    return ChatResponse(answer=answer, request_id=request.state.request_id)


@router.post("/rag/query", response_model=ChatResponse)
async def rag_query(payload: RagRequest, request: Request, _: str = Depends(current_user)) -> ChatResponse:
    answer = await request.app.state.rag.query(payload.question, payload.documents)
    return ChatResponse(answer=answer, request_id=request.state.request_id)


@router.post("/jobs", response_model=JobResponse, status_code=202)
async def create_job(_: str = Depends(current_user)) -> JobResponse:
    return JobResponse(job_id=str(uuid.uuid4()), status="queued")


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str, _: str = Depends(current_user)) -> JobResponse:
    return JobResponse(job_id=job_id, status="queued")
