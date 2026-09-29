"""Evidence and citation validation agent."""

from __future__ import annotations

from typing import Any

from src.agents.common import MissingContextError, success
from src.memory.shared_state import SharedState
from src.tools.registry import ToolRegistry


class ValidatorAgent:
    name = "validator"

    def __init__(self, tools: ToolRegistry) -> None:
        self.tools = tools

    def run(self, state: SharedState) -> dict[str, Any]:
        retrieval = state.read(self.name, "retrieval")
        analysis = state.read(self.name, "analysis")
        if not retrieval or not analysis:
            raise MissingContextError("Validation requires retrieval context and analysis")
        citations = [citation["id"] for citation in retrieval.get("citations", [])]
        source_ids = [document["id"] for document in retrieval.get("context", [])]
        validation = self.tools.execute(
            "Validation Tool",
            answer=analysis.get("summary", ""),
            citations=citations,
            source_ids=source_ids,
        )
        result = success(
            self.name,
            validated=validation["is_valid"],
            issues=validation["issues"],
            citations=citations,
        )
        state.write(self.name, "validation", result)
        return result