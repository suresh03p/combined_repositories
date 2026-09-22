# Production Architecture

## Request path

Users -> TLS load balancer/reverse proxy -> FastAPI containers -> AI and RAG services. Redis provides low-latency shared state and job coordination. PostgreSQL stores durable users, conversations, and job metadata. Background workers process long-running ingestion and generation tasks. The LLM provider remains outside the container and is reached with an environment-provided credential.

## Local versus production

Local development runs one Uvicorn process and can use the deterministic local AI fallback. Production runs immutable images, multiple workers/replicas, a reverse proxy, managed Redis/PostgreSQL, secret injection, restricted network access, and centralized logs/metrics.

## Deployment units

- Image: versioned Python application filesystem built from the Dockerfile.
- Container: one isolated running image instance; it is disposable and stateless.
- Application server: Uvicorn serves FastAPI; a process manager or platform controls replicas.
- Reverse proxy: terminates TLS, applies routing/request limits, and forwards to healthy containers.
- Health: `/health` proves the process responds.
- Readiness: `/ready` proves configured dependencies and AI configuration are usable.

## Operations

Logs are JSON on stdout and include request IDs, status-relevant events, and duration without secrets or sensitive prompts. Monitoring should collect availability, latency percentiles, error rate, token/provider latency, CPU, memory, Redis health, and queue depth. SIGTERM triggers FastAPI lifespan shutdown, closes Redis, and lets the server stop accepting new work.

## Compose topology

Compose runs `api` and `redis` on one private network. The API reaches Redis as `redis://redis:6379`; `localhost` would refer to the API container itself. Compose health ordering waits for Redis before starting API traffic.

## Image optimization

The image uses `python:3.12-slim`, copies `requirements.txt` before source for dependency-layer caching, installs without pip cache, excludes tests/secrets/caches through `.dockerignore`, and runs as `nobody`. An actual image-size comparison should be recorded from `docker image ls` after building a baseline and this optimized image.
