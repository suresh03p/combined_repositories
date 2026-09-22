"""Simple BM25-style lexical retrieval with IDF weighting."""
from __future__ import annotations
from collections import Counter
import math
import re


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def search(query: str, documents: list[dict], k: int = 5, filters: dict | None = None) -> list[dict]:
    query_terms = set(tokens(query))
    eligible = [doc for doc in documents if not filters or all(doc.get("metadata", {}).get(k) == v for k, v in filters.items())]
    n = len(eligible) or 1
    df = Counter(term for doc in eligible for term in set(tokens(doc["text"])))
    scored = []
    for doc in eligible:
        counts = Counter(tokens(doc["text"]))
        score = sum((1 + math.log(counts[t])) * math.log((n + 1) / (df[t] + 1)) for t in query_terms if counts[t])
        scored.append({**doc, "score": round(score, 6)})
    return sorted(scored, key=lambda item: item["score"], reverse=True)[:k]
