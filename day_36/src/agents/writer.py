"""Writer agent that produces a sourced result after validation."""

from __future__ import annotations

from typing import Any

from src.agents.common import MissingContextError, success
from src.memory.shared_state import SharedState


class WriterAgent:
    name = "writer"

    def run(self, state: SharedState) -> dict[str, Any]:
        question = state.read(self.name, "question")
        retrieval = state.read(self.name, "retrieval")
        analysis = state.read(self.name, "analysis")
        validation = state.read(self.name, "validation")
        if not validation or not validation.get("validated"):
            raise MissingContextError("Writer requires a validated analysis")
        if not retrieval or not analysis:
            raise MissingContextError("Writer requires retrieval context and analysis")

        citations = retrieval.get("citations", [])
        citation_text = ", ".join(
            f"{citation['title']} ({citation['id']})" for citation in citations
        )
        findings = " ".join(analysis.get("findings", []))
        answer = (
            f"Question: {question}\n\n{analysis['summary']} {findings}\n\n"
            f"Sources: {citation_text}"
        )
        result = success(self.name, answer=answer, citations=citations)
        state.write(self.name, "draft", result)
        return result