from dataclasses import dataclass
from enum import Enum
class ExecutionStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class StepContext:
    task_id: str
    conversation_id: str
    input_text: str
    previous_outputs: dict[str, object]
    idempotency_key: str
