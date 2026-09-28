from typing import Any

from src.orchestration.state import AgentState


class ValidationAgent:
    """Check that a response has a request and traceable supporting evidence."""

    def run(self, state: AgentState) -> dict[str, Any]:
        evidence = state.research_results + state.retrieved_documents
        checks = {
            "request_present": bool(state.user_request.strip()),
            "evidence_present": bool(evidence),
            "evidence_has_source": all(
                bool(item.get("source") or item.get("title")) for item in evidence
            ),
        }
        return {
            "is_valid": all(checks.values()),
            "checks": checks,
            "notes": [] if all(checks.values()) else [
                name for name, passed in checks.items() if not passed
            ],
        }
