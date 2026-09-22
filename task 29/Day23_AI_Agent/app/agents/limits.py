from dataclasses import dataclass


@dataclass(frozen=True)
class AgentLimits:
    max_steps: int = 5
    max_message_length: int = 4_000


class LimitExceededError(RuntimeError):
    pass
