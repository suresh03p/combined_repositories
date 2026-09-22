"""Cheap second-stage reranker using query-term coverage."""
from __future__ import annotations
from .keyword_search import tokens


def rerank(query: str, candidates: list[dict], k: int = 5) -> list[dict]:
    wanted = set(tokens(query))
    rescored = []
    for item in candidates:
        terms = set(tokens(item["text"]))
        coverage = len(wanted & terms) / max(len(wanted), 1)
        item = {**item, "rerank_score": round(.7 * item.get("score", 0) + .3 * coverage, 6)}
        rescored.append(item)
    return sorted(rescored, key=lambda item: item["rerank_score"], reverse=True)[:k]
