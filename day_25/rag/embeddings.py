"""Deterministic local embeddings; swap in a hosted/model encoder in production."""
from __future__ import annotations

import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer


class EmbeddingModel:
    def __init__(self, max_features: int = 2048):
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=max_features)

    def fit(self, texts: list[str]) -> None:
        self.vectorizer.fit(texts)

    def encode(self, texts: list[str]):
        return self.vectorizer.transform(texts)

    @property
    def dimension(self) -> int:
        return len(self.vectorizer.vocabulary_)


def save_records(records: list[dict], path: str | Path) -> None:
    Path(path).write_text(json.dumps(records), encoding="utf-8")


def load_records(path: str | Path) -> list[dict]:
    return json.loads(Path(path).read_text(encoding="utf-8"))
