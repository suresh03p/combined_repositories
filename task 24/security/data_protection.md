# Sensitive Information Protection

Protect API keys, passwords, database credentials, access tokens, PII, financial information, internal system prompts, and private documents. This project uses only fake values such as `FAKE_API_KEY_12345` and `FAKE_PASSWORD_123`.

Logs record request ID, user ID, tenant ID, endpoint, status, latency, token usage, and error code. They do not record passwords, JWTs, API keys, authorization headers, or full sensitive documents. Responses are scanned before returning. Production systems also need centralized redaction, DLP, secret scanning, retention controls, and access-controlled logs.
