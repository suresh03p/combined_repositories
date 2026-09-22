# Security Checklist

- [x] `.env` is ignored and only `.env.example` is tracked.
- [x] Secrets are read from environment variables.
- [x] Production hides interactive API docs.
- [x] Sensitive values are excluded from logs.
- [x] Authentication and bearer-token validation protect chat, RAG, and jobs.
- [x] Pydantic validates request shape, length, and collection size.
- [x] Middleware rejects oversized requests.
- [x] Docker runs as `nobody` with a read-only root filesystem in Compose.
- [ ] Add a real identity provider, rotation, refresh/revocation, and rate limiting before public exposure.
- [ ] Add PostgreSQL TLS, migrations, least-privilege credentials, and mandatory production connectivity.
- [ ] Add provider retry budgets, prompt/data redaction policy, and dependency vulnerability scanning.
