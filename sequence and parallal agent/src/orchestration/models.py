"""Shared data models for agent results, traces, and aggregate state."""

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class RunStatus(str, Enum):
    SUCCEEDED = "succeeded"
    FALLBACK_SUCCEEDED = "fallback_succeeded"
    FAILED = "failed"


@dataclass
class AgentResult:
    agent_name: str
    category: str
    claims: dict[str, Any] = field(default_factory=dict)
    sources: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    citations: list[str] = field(default_factory=list)
    calculations: dict[str, dict[str, float]] = field(default_factory=dict)
    tool_calls: list[str] = field(default_factory=list)
    status: RunStatus = RunStatus.SUCCEEDED
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        return payload


@dataclass
class AgentTrace:
    agent: str
    start_time: str
    end_time: str
    status: RunStatus
    tool_calls: list[str] = field(default_factory=list)
    result: dict[str, Any] | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["status"] = self.status.value
        return payload


@dataclass
class ValidationReport:
    valid: bool
    issues: list[str] = field(default_factory=list)
    validated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class UnifiedState:
    results: list[dict[str, Any]]
    claims: dict[str, list[dict[str, Any]]]
    conflicts: list[dict[str, Any]]
    validation: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)