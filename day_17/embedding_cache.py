import hashlib
from app.services.embedding_service import cached_embed

def calculate_embedding_reuse(chunks: list[str]) -> dict[str, int]:
    seen: set[str] = set()
    new_embeddings = 0
    reused_embeddings = 0
    for chunk in chunks:
        digest = hashlib.sha256(chunk.encode()).hexdigest()
        if digest in seen:
            reused_embeddings += 1
        else:
            _, reused = cached_embed(chunk)
            new_embeddings += not reused
            reused_embeddings += reused
            seen.add(digest)
    return {"total_chunks": len(chunks), "new_embeddings": new_embeddings, "reused_embeddings": reused_embeddings}
