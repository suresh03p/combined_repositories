# Day19 Production AI Assistant

A layered FastAPI training project for production AI architecture. It demonstrates chat, conversation history, request validation, persistence, caching concepts, job APIs, health checks, observability fields, and Celery scaffolding.

## Architecture

```mermaid
flowchart TD
  Client --> API[FastAPI API]
  API --> Chat[Chat API]
  API --> Jobs[Job API]
  Chat --> Service[AI Service]
  Service --> RAG[Retriever / RAG]
  Service --> LLM[Mock LLM]
  Service --> Cache[Cache]
  Service --> DB[(PostgreSQL or SQLite)]
  Jobs --> Queue[Redis Queue]
  Queue --> Worker[Celery Worker]
  Worker --> DB
```

## Features

- `POST /api/v1/chat` with Pydantic validation and mock policy answers
- `GET /api/v1/conversations/{conversation_id}` with stored messages
- `POST /api/v1/documents/process` and `GET /api/v1/jobs/{job_id}`
- Database-backed AI request telemetry: tokens, model, latency, and status
- Health endpoints for the API, database, Redis/cache, and AI service
- Docker Compose services for API, PostgreSQL, Redis, and worker

## Tech stack

Python 3.12, FastAPI, Uvicorn, SQLAlchemy, Pydantic Settings, PostgreSQL, Redis, Celery, pytest, and Docker.

## Installation

```powershell
cd Day19_Production_AI
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env`. Local development defaults to SQLite, so PostgreSQL and Redis are optional for the first run.

## Run

```powershell
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for Swagger UI.

## Environment variables

`DATABASE_URL`, `REDIS_URL`, `LLM_API_KEY`, `VECTOR_DB_URL`, `APP_ENV`, `LOG_LEVEL`, `CACHE_TTL`, and `AI_TIMEOUT` are supported. Never commit `.env` or API keys to source control.

## Docker setup

```powershell
docker compose up --build
```

This starts `api`, `postgres`, `redis`, and `worker`.

## Testing

```powershell
pytest -q
```

## Troubleshooting

- If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass`.
- If port 8000 is busy, run Uvicorn with `--port 8001`.
- For PostgreSQL, use `postgresql+psycopg://user:password@localhost:5432/ai_db`.
- The current AI and cache are intentionally mock/local implementations for training.

## Production considerations

Add authentication and authorization, database migrations, real Redis cache access, provider timeouts and retries, structured logs and metrics, rate limits, cost accounting, vector database integration, secret management, and a real worker status update flow before deployment.

See `docs/Day19_Production_AI_Architecture.md`, `docs/async_vs_background.md`, and `docs/production_checklist.md` for the learning notes.
