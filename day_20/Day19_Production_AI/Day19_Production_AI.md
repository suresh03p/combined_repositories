# Day 19: Production AI Architecture

See [docs/Day19_Production_AI_Architecture.md](docs/Day19_Production_AI_Architecture.md) for the full lesson.

The project demonstrates the production path:

```text
Client -> API -> Validation -> Service -> RAG / Agent -> LLM
       -> Database -> Cache -> Logging -> Monitoring
```

Training code produces a model prediction. A production AI application must also manage users, requests, authentication, business rules, history, failures, latency, cost, background work, and observability.
