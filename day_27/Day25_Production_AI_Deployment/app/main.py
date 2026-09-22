import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging_config import configure_logging
from app.rag.pipeline import RagPipeline
from app.services.ai_service import AIService
from app.services.redis_service import RedisService


def build_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)
    logger = logging.getLogger(settings.app_name)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.settings = settings
        app.state.logger = logger
        app.state.redis = RedisService(settings.redis_url)
        app.state.ai = AIService(settings.llm_api_key, settings.request_timeout)
        app.state.rag = RagPipeline(app.state.ai)
        logger.info("Application started")
        yield
        await app.state.redis.close()
        logger.info("Application shutdown complete")

    app = FastAPI(title=settings.app_name, lifespan=lifespan, docs_url=None if settings.app_env == "production" else "/docs")

    @app.middleware("http")
    async def request_context(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", f"req-{uuid.uuid4().hex[:8]}")
        request.state.request_id = request_id
        started = time.perf_counter()
        if request.headers.get("content-length") and int(request.headers["content-length"]) > settings.max_request_size:
            return JSONResponse(status_code=413, content={"detail": "Request too large", "request_id": request_id})
        try:
            response = await call_next(request)
        except Exception:
            logger.exception("Unhandled request error", extra={"request_id": request_id})
            response = JSONResponse(status_code=500, content={"detail": "Internal server error", "request_id": request_id})
        response.headers["X-Request-ID"] = request_id
        logger.info("Request completed in %.3fs", time.perf_counter() - started, extra={"request_id": request_id})
        return response

    app.include_router(router)
    return app


app = build_app()
