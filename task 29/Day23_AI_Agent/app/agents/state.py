from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:
    conversation_id: str
    user_message: str
    plan: list[str] = field(default_factory=list)
    observations: list[str] = field(default_factory=list)
    response: str = ""
    steps: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)
