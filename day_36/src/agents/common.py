"""Shared agent exceptions and response helpers."""


class AgentError(RuntimeError):
    """Base error for an agent execution failure."""


class MissingContextError(AgentError):
    """Raised when an agent cannot do useful work without upstream context."""


class InvalidAgentResponse(AgentError):
    """Raised when an agent response does not satisfy the response contract."""


def success(agent: str, **payload: object) -> dict[str, object]:
    return {"agent": agent, "status": "success", **payload}