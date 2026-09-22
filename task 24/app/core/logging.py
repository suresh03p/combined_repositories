import logging
from time import perf_counter
from uuid import uuid4

logger = logging.getLogger("secure_ai")

def audit_event(endpoint: str, status: str, user_id: str | None = None, tenant_id: str | None = None, error_code: str | None = None, token_usage: int | None = None):
    event = {"request_id": f"REQ-{uuid4().hex[:8]}", "user_id": user_id, "tenant_id": tenant_id, "endpoint": endpoint, "status": status, "latency": round(perf_counter(), 5), "token_usage": token_usage, "error_code": error_code}
    logger.info("audit_event=%s", event)
    return event
