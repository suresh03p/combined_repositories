# Day 20: AI Security Theory

## Traditional vs AI application security

A traditional application often follows `User -> API -> Database`. Its main concerns are identity, permissions, input validation, database security, and safe output.

An AI application adds prompt construction, retrieval augmented generation (RAG), documents, model behavior, and agent tools: `User -> API -> Prompt -> RAG -> Documents -> Tools -> LLM -> Database`.

Each added step can interpret or forward untrusted content. A user can attempt prompt injection; a retrieved document can contain indirect injection; a tool can make an external side effect; and model output can be malformed, over-permissioned, or leak context. Security therefore needs defense in depth: authenticate, authorize, isolate tenants, validate inputs and outputs, restrict tools, rate-limit, and audit.

## Core principle

User input and retrieved documents are data, never trusted instructions. The LLM is not a security boundary. Enforce security in ordinary application code before retrieval and tool execution, and after model output.

## Password flow

`Password -> Argon2 password hash -> Database`. Hashing is one-way and purpose-built for guessing resistance. Encryption is reversible and requires protecting a decryption key, so it is not the right storage primitive for passwords.

## Security terminology

| Term | Definition | Example | Prevention |
|---|---|---|---|
| Authentication | Proves who a caller is. | Login with email and password. | Strong credentials and MFA. |
| Authorization | Decides what an authenticated caller may do. | Only an admin deletes documents. | Enforce server-side permissions. |
| JWT | Signed claims in a compact token. | A token contains subject and expiry. | Verify signature, expiry, issuer, and claims. |
| Access Token | Short-lived credential for API calls. | `Authorization: Bearer ...`. | Keep short-lived and never log it. |
| Refresh Token | Longer-lived credential used to obtain access tokens. | Refresh after an access token expires. | Rotate, revoke, and store securely. |
| Password Hashing | One-way transformation designed for passwords. | Argon2 hash in the user row. | Use Argon2/bcrypt and verify, never decrypt. |
| RBAC | Role-based access control. | `ADMIN` can manage users. | Deny by default and check every route. |
| Least Privilege | Give only required access. | Chat cannot query arbitrary tables. | Narrow roles and tool allowlists. |
| Prompt Injection | Input tries to override model instructions. | “Ignore previous instructions.” | Detect, isolate data, and enforce controls in code. |
| Indirect Prompt Injection | Hostile instructions arrive through retrieved content. | A PDF says “reveal secrets.” | Treat documents as untrusted data. |
| Data Leakage | Sensitive data reaches an unauthorized party. | A response includes a private document. | Tenant checks, redaction, output validation. |
| PII | Information identifying a person. | Email address or phone number. | Minimize, protect, and redact it. |
| Secret | Confidential value used for access. | API key or database password. | Environment secret manager; never commit or log. |
| Rate Limiting | Caps requests over a time window. | 10 chat calls per minute. | Return 429 and use a shared store in production. |
| Input Validation | Checks incoming data shape and limits. | Message max 10,000 characters. | Pydantic schemas and size limits. |
| Output Validation | Checks generated data before release. | Confidence must be 0 to 1. | Schema validation and sensitive-data scanning. |
| Audit Log | Security-relevant record of an action. | User, tenant, endpoint, result. | Structured, access-controlled, redacted logs. |
| Security Boundary | Point where trust or permission changes. | API to tool executor. | Re-authenticate or enforce policy at the boundary. |
| Tenant Isolation | Prevents one company seeing another's data. | Tenant A cannot retrieve B's document. | Filter by tenant on every query. |
| Input Size Limit | Maximum accepted payload size. | Reject a 50 MB message. | Enforce at schema, proxy, and storage layers. |
| Output Encoding | Safely represents returned content. | Escape HTML in a web response. | Contextual encoding and safe serializers. |

## Why AI needs extra surfaces

Traditional code follows deterministic instructions. AI systems combine untrusted natural language, probabilistic model output, retrieved text, and tools that may mutate real systems. A secure design assumes the model can be persuaded, confused, or wrong, and keeps identity, tenant boundaries, permissions, and side effects outside model discretion.
