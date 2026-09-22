"""Small vector-capable local store using cosine similarity."""
from __future__ import annotations

import numpy as np
from .embeddings import EmbeddingModel
from .metadata import matches_filter


class VectorStore:
    def __init__(self, model: EmbeddingModel | None = None):
        self.model = model or EmbeddingModel()
        self.documents: list[dict] = []
        self.matrix = None

    def add_documents(self, documents: list[dict]) -> None:
        self.documents.extend(documents)
        self.model.fit([item["text"] for item in self.documents])
        self.matrix = self.model.encode([item["text"] for item in self.documents])

    def search(self, query: str, k: int = 5, filters: dict | None = None) -> list[dict]:
        if not self.documents:
            return []
        query_vector = self.model.encode([query])
        scores = (self.matrix @ query_vector.T).toarray().ravel()
        candidates = [(i, float(score)) for i, score in enumerate(scores)
                      if matches_filter(self.documents[i].get("metadata", {}), filters)]
        return [self._result(i, score) for i, score in sorted(candidates, key=lambda x: x[1], reverse=True)[:k]]

    def _result(self, index: int, score: float) -> dict:
        return {**self.documents[index], "score": round(score, 6)}

    def delete_document(self, document_id: str) -> None:
        self.documents = [item for item in self.documents if item.get("metadata", {}).get("document_id") != document_id]
        self.matrix = None
        if self.documents:
            self.model.fit([item["text"] for item in self.documents])
            self.matrix = self.model.encode([item["text"] for item in self.documents])

    def get_document(self, chunk_id: str) -> dict | None:
        return next((item for item in self.documents if item.get("metadata", {}).get("chunk_id") == chunk_id), None)
