import time
import uuid

from sqlalchemy.orm import Session

from app.models.ai_request import AIRequest
from app.services.cache import get_cached, set_cached


LEAVE_ANSWER = "Employees receive 18 annual leave days."


def generate_answer(db: Session, conversation_id: str, message: str) -> tuple[str, list[str]]:
    cache_key = f"answer:{message.casefold().strip()}"
    cached = get_cached(cache_key)
    if cached:
        return cached["answer"], cached["sources"]

    started = time.perf_counter()
    answer = LEAVE_ANSWER if "leave" in message.casefold() else (
        "I am a mock AI assistant. Connect a model and document retriever for this question."
    )
    sources = ["leave_policy.pdf"] if "leave" in message.casefold() else []
    elapsed = time.perf_counter() - started
    input_tokens = len(message.split())
    output_tokens = len(answer.split())
    db.add(AIRequest(
        request_id=f"REQ-{uuid.uuid4().hex[:12]}",
        conversation_id=conversation_id,
        model="mock-gpt",
        status="success",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        llm_time=elapsed,
        latency=elapsed,
    ))
    set_cached(cache_key, {"answer": answer, "sources": sources})
    return answer, sources
