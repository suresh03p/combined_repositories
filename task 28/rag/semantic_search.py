from .vector_store import VectorStore


def search(query: str, store: VectorStore, k: int = 5, filters: dict | None = None) -> list[dict]:
    return store.search(query, k=k, filters=filters)


def format_results(results: list[dict]) -> list[dict]:
    return [{"chunk": result["text"], "similarity_score": result["score"],
             "document": result["metadata"]["document_name"], "page": result["metadata"]["page_number"]}
            for result in results]
