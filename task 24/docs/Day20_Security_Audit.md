# Day 20 Security Audit

| Security Area | Status | Risk | Fix |
|---|---|---|---|
| JWT | Implemented | Development fallback secret | Set a random managed secret in production |
| Passwords | Implemented | In-memory users only | Persist Argon2 hashes in a protected database |
| RAG | Implemented | Retriever is a teaching stub | Add ACL-aware production query filters |
| Prompt Injection | Partial | Detection is heuristic | Treat as defense-in-depth; keep policy in code |
| Tools | Implemented | Database tool is illustrative | Add per-action scopes and approvals |
| Secrets | Partial | No secret manager in demo | Use environment/secret manager and scanning |
| Logging | Implemented | Latency example is process-relative | Use request timers and redaction middleware |
| Rate Limit | Implemented | Process-local bucket | Use Redis/distributed limiter in production |
| Tenant Isolation | Implemented | In-memory records | Enforce tenant predicates at database layer |
| Input Validation | Implemented | Proxy limits not included | Configure gateway and upload limits |
| Output Validation | Implemented | Regex scanner is limited | Add DLP/redaction and structured schemas |
| Docker | Provided | Demo image needs hardening | Non-root user, pinned image, read-only filesystem |
| Environment Variables | Partial | Fallback exists for local learning | Fail closed when production configuration is absent |

## Attack scenario

The attacker must first authenticate. RBAC blocks restricted endpoints and the tool allowlist rejects unauthorized tools. Prompt screening blocks direct injection, tenant filtering blocks cross-company documents, output validation blocks fake secrets, and audit events record blocked requests. No single model instruction is treated as a security boundary.
