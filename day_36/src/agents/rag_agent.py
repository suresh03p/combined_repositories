"""RAG agent: query transformation, retrieval, ranking, and citations."""

from __future__ import annotations

import re
from typing import Any

from src.agents.common import MissingContextError, success
from src.memory.shared_state import SharedState
from src.tools.registry import ToolRegistry


class RAGAgent:
    name = "rag"

    def __init__(self, tools: ToolRegistry, context_limit: int = 4) -> None:
        self.tools = tools
        self.context_limit = context_limit

    @staticmethod
    def transform_query(question: str, findings: list[dict[str, Any]]) -> str:
        terms = re.findall(r"[a-z0-9]+", question.lower())
        evidence_terms = [
            term
            for finding in findings
            for term in re.findall(r"[a-z0-9]+", finding.get("text", "").lower())
        ]
        return " ".join(dict.fromkeys([*terms, *evidence_terms]))

    def run(self, state: SharedState) -> dict[str, Any]:
        question = state.read(self.name, "question")
        research = state.read(self.name, "research") or {}
        query = self.transform_query(question, research.get("findings", []))
        documents = self.tools.execute("RAG Search", query=query)
        documents.sort(key=lambda document: (-document.get("score", 0), document["id"]))
        context = documents[: self.context_limit]
        if not context:
            raise MissingContextError("RAG search returned no supporting documents")
        citations = [
            {"id": document["id"], "title": document["title"], "source": document["source"]}
            for document in context
        ]
        result = success(
            self.name,
            query=query,
            context=context,
            citations=citations,
        )
        state.write(self.name, "retrieval", result)
        return result