from typing import Any

from src.orchestration.state import AgentState
from src.tools.text import keywords


class AnalysisAgent:
    """Summarize the evidence set and expose simple, inspectable counts."""

    def run(self, state: AgentState) -> dict[str, Any]:
        evidence = state.research_results + state.retrieved_documents
        topics = sorted(
            set().union(*(keywords(item["title"]) for item in evidence))
        ) if evidence else []
        return {
            "evidence_count": len(evidence),
            "research_result_count": len(state.research_results),
            "retrieved_document_count": len(state.retrieved_documents),
            "topics": topics,
        }
