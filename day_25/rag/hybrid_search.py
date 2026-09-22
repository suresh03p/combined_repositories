from __future__ import annotations
from .keyword_search import search as keyword_search
from .vector_store import VectorStore


def search(query: str, store: VectorStore, k: int = 5, semantic_weight: float = .7,
           keyword_weight: float = .3, filters: dict | None = None) -> list[dict]:
    semantic = store.search(query, k=max(k, 20), filters=filters)
    lexical = keyword_search(query, store.documents, k=max(k, 20), filters=filters)
    scores: dict[str, dict] = {}
    for rank, item in enumerate(semantic):
        scores.setdefault(item["metadata"]["chunk_id"], {**item, "semantic_score": item["score"], "keyword_score": 0})["semantic_rank"] = rank
    for rank, item in enumerate(lexical):
        entry = scores.setdefault(item["metadata"]["chunk_id"], {**item, "semantic_score": 0, "keyword_score": item["score"]})
        entry["keyword_score"] = item["score"]
        entry["keyword_rank"] = rank
    max_keyword = max((item["keyword_score"] for item in scores.values()), default=1) or 1
    for item in scores.values():
        item["score"] = semantic_weight * item["semantic_score"] + keyword_weight * item["keyword_score"] / max_keyword
    return sorted(scores.values(), key=lambda item: item["score"], reverse=True)[:k]
