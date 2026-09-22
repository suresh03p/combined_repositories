# Production AI API

A compact Day 25 deployment foundation for a FastAPI AI service. It demonstrates configuration, authentication, Redis-aware readiness, RAG service boundaries, request correlation, structured logs, Docker, Compose, and tests.

## Architecture

Client -> FastAPI -> AI service / RAG pipeline; Redis supports shared state and readiness checks. In production, place a TLS-terminating load balancer or reverse proxy in front of multiple API containers, add PostgreSQL for durable state, and run background workers for long jobs.

## Setup

```powershell
cd Day25_Production_AI_Deployment
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

The local fallback AI response allows startup without an API key. Set `APP_ENV=production` and `LLM_API_KEY` for a production readiness check.

## Docker

```powershell
docker build -t production-ai-api .
docker run --env-file .env -p 8000:8000 production-ai-api
```

## Docker Compose

```powershell
Copy-Item .env.example .env
docker compose up --build
docker compose down
```

Compose uses `redis://redis:6379`; service names resolve over the Compose network, while `localhost` would point back to the API container.

## API

- `GET /health`: process liveness.
- `GET /ready`: Redis, database configuration, and AI readiness.
- `POST /auth/login`: returns a short-lived bearer token.
- `POST /chat`: authenticated chat request.
- `POST /rag/query`: authenticated context-plus-question request.
- `GET /jobs/{job_id}`: authenticated job status placeholder.

## Testing

```powershell
pytest
```

## Security

Secrets are environment-provided and `.env` is ignored. The app avoids logging credentials, prompts, and tokens, validates request sizes and payloads, uses non-root Docker execution, and disables interactive API docs in production. Replace the demonstration HMAC token with an established identity provider before exposing the service publicly.

## Performance

No benchmark is claimed in this starter repository. Run `scripts/run_load_test.ps1` against a running service and record p50/p95 latency, error rate, CPU, memory, Redis latency, and provider latency in `docs/performance_test.md`.
