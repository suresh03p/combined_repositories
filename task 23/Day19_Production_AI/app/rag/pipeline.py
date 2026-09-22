from app.rag.retriever import retrieve


def build_context(query: str) -> tuple[str, list[str]]:
    documents = retrieve(query)
    return "\n".join(item["content"] for item in documents), [item["source"] for item in documents]
