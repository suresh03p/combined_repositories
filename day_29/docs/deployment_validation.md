# Deployment Validation

A deployment is considered successful only when the application is actually healthy and reachable.

## Validation checks

- Container is running
- API is reachable over HTTP
- `/health` returns `{"status": "healthy"}`
- `/ready` returns `{"status": "ready"}`
- Redis connectivity works
- RAG retrieval works
- AI request flow works

## Why validation matters

A build may succeed while the application is still misconfigured or unreachable. Health and readiness checks provide a simple way to confirm the service is operational before considering the deployment finished.
