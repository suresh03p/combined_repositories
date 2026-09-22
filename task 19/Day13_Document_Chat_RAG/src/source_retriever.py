"""Retrieval results that are ready for source-aware answers."""

from .vector_store import VectorStore


def retrieve(store: VectorStore, question: str, top_k: int = 5) -> list[dict]:
    return [{"content": item["content"], "source": item["metadata"]["source"],
             "page": item["metadata"]["page_number"], "section": item["metadata"].get("section", "General"),
             "document_id": item["metadata"]["document_id"], "score": item["score"]}
            for item in store.search(question, top_k)]