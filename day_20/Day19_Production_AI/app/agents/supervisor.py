def route_request(message: str) -> str:
    """Small routing seam for a future multi-agent supervisor."""
    return "policy_retrieval" if "policy" in message.casefold() else "general_assistant"
