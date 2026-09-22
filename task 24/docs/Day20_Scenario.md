# Final Security Scenario

| Attack | Detection | Protection | Final result |
|---|---|---|---|
| Login without valid credentials | JWT validation | 401 response | Stopped |
| Prompt injection in chat | Prompt pattern check | Reject before model | Stopped |
| Restricted data request | RBAC and tenant filter | 403 or filtered retrieval | Stopped |
| Cross-tenant document access | `tenant_id` comparison | Document excluded | Stopped |
| Unauthorized tool | Role/tool allowlist | 403 before execution | Stopped |
| Sensitive response | Output scanner/schema | Reject response and audit | Stopped |

Audit events record the endpoint, actor, tenant, result, and error code without recording secrets or authorization headers.
