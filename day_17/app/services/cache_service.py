import hashlib
from app.schemas.chat import ChatResponse

_response_cache: dict[str, ChatResponse] = {}

def cache_key(question: str, document_version: str) -> str:
    return hashlib.sha256(f"{question.strip().lower()}::{document_version}".encode()).hexdigest()

def get(question: str, document_version: str) -> ChatResponse | None:
    return _response_cache.get(cache_key(question, document_version))

def put(question: str, document_version: str, response: ChatResponse) -> None:
    _response_cache[cache_key(question, document_version)] = response

def clear() -> None:
    _response_cache.clear()
