"""Small dependency-light vector store with cosine TF-IDF-style retrieval."""

import math
import re


def _tokens(text: str) -> list[str]:
    stopwords = {"a", "an", "and", "are", "for", "is", "of", "the", "to", "what", "who", "how", "do", "i"}
    tokens = [token for token in re.findall(r"[a-z0-9]+", text.lower()) if token not in stopwords]
    return [token[:-2] if token.endswith("ed") else token[:-1] if token.endswith("s") else token for token in tokens]


class VectorStore:
    def __init__(self):
        self._records: dict[str, dict] = {}

    def add_documents(self, chunks: list[dict]) -> None:
        for chunk in chunks:
            self._records[chunk["chunk_id"]] = chunk

    def delete_document(self, document_id: str) -> int:
        removed = [key for key, value in self._records.items()
                   if value["metadata"]["document_id"] == document_id]
        for key in removed:
            del self._records[key]
        return len(removed)

    def get_document(self, document_id: str) -> list[dict]:
        return [value for value in self._records.values()
                if value["metadata"]["document_id"] == document_id]

    def search(self, query: str, top_k: int = 5) -> list[dict]:
        query_terms = set(_tokens(query))
        scored = []
        for chunk in self._records.values():
            terms = set(_tokens(chunk["text"]))
            overlap = len(query_terms & terms)
            score = overlap / math.sqrt(max(len(query_terms) * len(terms), 1))
            if score >= 0.25:
                scored.append({"content": chunk["text"], "metadata": chunk["metadata"], "score": score})
        return sorted(scored, key=lambda item: item["score"], reverse=True)[:top_k]