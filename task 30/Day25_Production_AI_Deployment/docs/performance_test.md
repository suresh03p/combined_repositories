# Performance Test

No load benchmark is reported automatically because results depend on the host, Docker runtime, Redis, and LLM provider. The included PowerShell helper probes `/health` with 10, 50, or 100 requests:

```powershell
./scripts/run_load_test.ps1 -Count 10
./scripts/run_load_test.ps1 -Count 50
./scripts/run_load_test.ps1 -Count 100
```

Record date, image tag, concurrency, request count, p50/p95/p99 latency, error count, CPU, memory, Redis latency, and AI provider latency here after running against a deployed environment. Health-only numbers do not represent end-to-end AI latency.
