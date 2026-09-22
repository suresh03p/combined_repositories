"""End-to-end offline RAG pipeline with answer plus sources."""
from __future__ import annotations
from pathlib import Path
from .ingestion import ingest_directory
from .text_cleaning import clean_pages
from .recursive_chunking import recursive_chunks
from .metadata import make_metadata
from .vector_store import VectorStore
from .hybrid_search import search as hybrid_search
from .reranker import rerank


class AdvancedRAG:
    def __init__(self, documents_dir: str | Path = "documents", chunk_size: int = 500, overlap: int = 50):
        pages = clean_pages(ingest_directory(documents_dir))
        records = []
        for page in pages:
            for index, text in enumerate(recursive_chunks(page["text"], chunk_size, overlap), start=1):
                records.append({"text": text, "metadata": make_metadata(page["document"], page["page"], index)})
        self.documents = records
        self.store = VectorStore()
        self.store.add_documents(records)

    def ask(self, query: str, k: int = 5, filters: dict | None = None) -> dict:
        candidates = hybrid_search(query.strip(), self.store, k=20, filters=filters)
        results = rerank(query, candidates, k=k)
        if not results:
            return {"answer": "I could not find supporting information in the permitted documents.", "sources": []}
        context = "\n".join(f"[{item['metadata']['document_name']} p.{item['metadata']['page_number']}] {item['text']}" for item in results)
        answer = self._grounded_answer(query, results)
        return {"answer": answer, "sources": [{"document": item["metadata"]["document_name"], "page": item["metadata"]["page_number"]} for item in results], "context": context}

    @staticmethod
    def _grounded_answer(query: str, results: list[dict]) -> str:
        # This deterministic fallback is intentionally transparent; replace with an LLM call in production.
        best = results[0]
        return f"Based on {best['metadata']['document_name']} page {best['metadata']['page_number']}: {best['text']}"


def main() -> None:
    pipeline = AdvancedRAG()
    print(pipeline.ask("How many annual leave days do employees receive?"))


if __name__ == "__main__":
    main()
