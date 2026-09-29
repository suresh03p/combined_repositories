"""Shared state with per-agent field-level read and write permissions."""

from __future__ import annotations

from copy import deepcopy
from typing import Any


class StateAccessError(PermissionError):
    """Raised when an agent accesses a field outside its permissions."""


_PERMISSIONS: dict[str, dict[str, set[str]]] = {
    "researcher": {"read": {"question"}, "write": {"research"}},
    "rag": {"read": {"question", "research"}, "write": {"retrieval"}},
    "analyst": {
        "read": {"question", "research", "retrieval"},
        "write": {"analysis"},
    },
    "validator": {
        "read": {"question", "research", "retrieval", "analysis"},
        "write": {"validation"},
    },
    "writer": {
        "read": {"question", "research", "retrieval", "analysis", "validation"},
        "write": {"draft"},
    },
    "supervisor": {
        "read": {"question", "research", "retrieval", "analysis", "validation", "draft", "result"},
        "write": {"question", "research", "retrieval", "analysis", "validation", "draft", "result"},
    },
}


class SharedState:
    def __init__(self, question: str) -> None:
        self._values: dict[str, Any] = {
            "question": question,
            "research": None,
            "retrieval": None,
            "analysis": None,
            "validation": None,
            "draft": None,
            "result": None,
        }

    def read(self, agent: str, field: str) -> Any:
        permissions = _PERMISSIONS.get(agent)
        if permissions is None or field not in permissions["read"]:
            raise StateAccessError(f"Agent {agent!r} cannot read field {field!r}")
        if field not in self._values:
            raise KeyError(f"Unknown shared-state field: {field}")
        return deepcopy(self._values[field])

    def write(self, agent: str, field: str, value: Any) -> None:
        permissions = _PERMISSIONS.get(agent)
        if permissions is None or field not in permissions["write"]:
            raise StateAccessError(f"Agent {agent!r} cannot write field {field!r}")
        if field not in self._values:
            raise KeyError(f"Unknown shared-state field: {field}")
        self._values[field] = deepcopy(value)

    def snapshot(self, agent: str) -> dict[str, Any]:
        permissions = _PERMISSIONS.get(agent)
        if permissions is None:
            raise StateAccessError(f"Unknown agent: {agent!r}")
        readable = permissions["read"]
        return {field: deepcopy(value) for field, value in self._values.items() if field in readable}