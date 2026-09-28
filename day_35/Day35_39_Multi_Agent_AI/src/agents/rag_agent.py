from typing import Any

from src.retrieval.retriever import LocalRetriever


class RAGAgent:
    """Ground the request in matching passages from the local knowledge base."""

    def __init__(self, retriever: LocalRetriever | None = None) -> None:
        self.retriever = retriever or LocalRetriever()

    def run(self, question: str) -> list[dict[str, Any]]:
        return self.retriever.retrieve(question)
