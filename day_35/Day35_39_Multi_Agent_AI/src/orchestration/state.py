from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class AgentState:
    conversation_id: str
    user_request: str
    current_agent: str = "supervisor"
    task_status: str = "pending"
    research_results: list[dict[str, Any]] = field(default_factory=list)
    retrieved_documents: list[dict[str, Any]] = field(default_factory=list)
    analysis_results: dict[str, Any] = field(default_factory=dict)
    validation_results: dict[str, Any] = field(default_factory=dict)
    final_response: str = ""
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
