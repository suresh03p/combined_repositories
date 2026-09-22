from .vector_store import VectorStore


def filtered_search(store: VectorStore, query: str, filters: dict, k: int = 5) -> list[dict]:
    """Authorization must produce filters before retrieval; never filter after generation."""
    return store.search(query, k=k, filters=filters)
