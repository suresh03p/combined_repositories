from dataclasses import dataclass
from app.services.embedding_service import cached_embed, cosine_similarity

@dataclass
class Chunk:
    chunk_id: str
    document_id: str
    file_name: str
    text: str
    vector: list[float]
    page: int | None = None

_chunks: dict[str, Chunk] = {}

def add_chunks(chunks: list[Chunk]) -> None:
    for chunk in chunks:
        _chunks[chunk.chunk_id] = chunk

def delete_document(document_id: str) -> None:
    for chunk_id in [key for key, item in _chunks.items() if item.document_id == document_id]:
        del _chunks[chunk_id]

def search(question: str, top_k: int = 3) -> list[tuple[Chunk, float]]:
    query_vector, _ = cached_embed(question)
    ranked = [(chunk, cosine_similarity(query_vector, chunk.vector)) for chunk in _chunks.values()]
    return sorted(ranked, key=lambda item: item[1], reverse=True)[:top_k]

def count_for_document(document_id: str) -> int:
    return sum(chunk.document_id == document_id for chunk in _chunks.values())

def healthy() -> bool:
    return True
