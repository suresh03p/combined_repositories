# CloudWatch Monitoring

## Logs

Send structured application logs to `production-ai-logs` or a service-specific log group. Include timestamp, level, request ID, route, status code, duration, and a safe error category. Never log tokens, passwords, prompts containing sensitive data, or full authorization headers.

For Docker on EC2, use the `awslogs` Docker logging driver or the CloudWatch agent. Set retention rather than keeping logs forever. For a future ECS deployment, use the `awslogs` log configuration on the task definition.

Monitor application startup, requests, 4xx/5xx errors, AI provider failures, Redis/database failures, and container exits. EC2 also provides CPU, network, and status-check metrics; memory requires an agent or container-level metric.

## Metrics and alerts

Track request count, error count and rate, p50/p95 response time, CPU, memory, container status, AI failure count, Redis health, and database connections. Start with these alarms:

| Signal | Example response |
| --- | --- |
| 5xx rate above threshold | Page on-call and inspect logs |
| p95 latency high | Check dependencies and CPU |
| EC2 status check failed | Recover or replace instance |
| Container stopped | Restart and inspect exit reason |
| Repeated AI failures | Check provider status, quota, and credentials |
| Memory pressure | Reduce concurrency or scale |

Use dashboards for trend visibility and alarms for action. Validate each alarm with a controlled test before production.
