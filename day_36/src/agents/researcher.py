"""Document research agent: discovers sources and extracts evidence."""

from __future__ import annotations

from typing import Any

from src.agents.common import MissingContextError, success
from src.memory.shared_state import SharedState
from src.tools.registry import ToolRegistry


class ResearchAgent:
    name = "researcher"

    def __init__(self, tools: ToolRegistry) -> None:
        self.tools = tools

    def run(self, state: SharedState) -> dict[str, Any]:
        question = state.read(self.name, "question")
        documents = self.tools.execute("Document Search", query=question)
        sources = [
            {
                "id": document["id"],
                "title": document["title"],
                "source": document["source"],
            }
            for document in documents
        ]
        findings = [
            {"source_id": document["id"], "text": fact}
            for document in documents
            for fact in document.get("facts", [])
        ]
        result = {"agent": self.name, "status": "success", "sources": sources, "findings": findings}
        state.write(self.name, "research", result)
        return result

    def provide_retrieval(self, question: str, research: dict[str, Any] | None) -> dict[str, Any]:
        """Provide a limited retrieval fallback when the RAG agent is unavailable."""
        if not research or not research.get("sources"):
            raise MissingContextError("Researcher has no sources to delegate as retrieval context")
        source_ids = {source["id"] for source in research["sources"]}
        contexts = []
        for source_id in source_ids:
            document = self.tools.execute("Document Reader", document_id=source_id)
            if document is not None:
                contexts.append(document)
        if not contexts:
            raise MissingContextError("Research sources could not be read")
        citations = [
            {"id": item["id"], "title": item["title"], "source": item["source"]}
            for item in contexts
        ]
        return {
            "query": question,
            "context": contexts,
            "citations": citations,
            "delegated_from": self.name,
        }