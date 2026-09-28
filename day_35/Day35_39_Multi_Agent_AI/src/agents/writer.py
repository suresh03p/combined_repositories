from src.orchestration.state import AgentState


class WriterAgent:
    """Turn the shared evidence and validation outcome into a cited answer."""

    def run(self, state: AgentState) -> str:
        evidence = state.research_results + state.retrieved_documents
        if not evidence:
            return (
                "I could not find supporting material in the bundled research sources "
                "or local knowledge base. No evidence-backed conclusion is available."
            )

        unique_sources = list(dict.fromkeys(
            item.get("source", item["title"]) for item in evidence
        ))
        findings = "\n".join(
            f"- {item['content']} [{item.get('source', item['title'])}]"
            for item in evidence
        )
        answer = f"Findings for: {state.user_request}\n{findings}\nSources: "
        answer += "; ".join(unique_sources)
        if not state.validation_results.get("is_valid", False):
            answer += "\n\nNote: validation found gaps in the available evidence."
        return answer
