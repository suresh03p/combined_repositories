# Failure Simulation and Recovery

Run experiments only in a test environment and record timestamps, alarm behavior, logs, impact, and recovery duration.

| Failure | Impact | Detection | Recovery |
| --- | --- | --- | --- |
| Stop Docker container | API unavailable | Health check, container status, 5xx alarm | Restart the pinned image and inspect logs |
| Break Redis connectivity | Readiness or dependent requests fail | Dependency error logs and readiness check | Restore route/credentials, then restart only if needed |
| Invalid LLM credentials | Chat requests fail while health may remain healthy | AI failure metric and error logs | Rotate secret, validate provider access, retry safely |
| Invalid API request | A single request receives 4xx | Request metrics and application validation logs | No infrastructure recovery; return a useful 4xx |
| Restart EC2 | Brief outage unless another instance serves traffic | EC2 status checks and uptime monitor | Confirm Docker restart policy and verify health endpoints |

## Rollback

1. Stop promotion of the failing version and preserve logs.
2. Identify the last known-good immutable ECR tag, for example `v1.0.0`.
3. Pull that tag and replace the running container without changing secrets.
4. Check `/health`, `/ready`, representative `/chat`, and `/rag/query` requests.
5. Confirm alarms clear, then document the incident and root cause.

Never use `latest` as the rollback reference. Keep at least the last successful image and its configuration metadata available.
