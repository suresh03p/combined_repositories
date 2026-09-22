# Current Architecture

This Day 25 repository is the productionized implementation of the Day 24 API surface.

- `app/main.py` creates FastAPI, configures logging, adds request IDs, applies request-size limits, and manages startup/shutdown resources.
- `app/api/routes.py` exposes health, readiness, authentication, chat, RAG, and job status routes.
- `app/core/config.py` centralizes all environment variables through Pydantic Settings. No API key or password is hardcoded as a required value.
- `app/services/ai_service.py` owns the AI boundary and provides a local fallback for development.
- `app/rag/pipeline.py` combines supplied document context with a question before calling the AI service. A vector database/embedding provider can be added behind this boundary.
- `app/services/redis_service.py` owns the async Redis client and its lifecycle. Empty `REDIS_URL` means local development does not require Redis; Compose sets `redis://redis:6379`.
- Database readiness currently treats an absent database URL as acceptable for this minimal service because no database repository is implemented yet. Production should add PostgreSQL and make that check mandatory.
- `app/core/logging_config.py` emits JSON logs to stdout; request IDs are added by middleware.
- `tests/` verifies the critical HTTP contract using a local fallback and no external services.

Known deliberate gaps: the AI provider call is a placeholder, the job endpoint is an in-memory contract placeholder, and RAG uses supplied documents rather than a persistent embedding/vector store. These boundaries are explicit so they can be replaced without changing the API contract.
