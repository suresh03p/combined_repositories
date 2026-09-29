"""Agent registry with capability-based task assignment."""

from __future__ import annotations

from typing import Any, Iterable


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, Any] = {}
        self._capabilities: dict[str, set[str]] = {}

    def register(self, name: str, agent: Any, capabilities: Iterable[str]) -> None:
        if name in self._agents:
            raise ValueError(f"Agent already registered: {name}")
        self._agents[name] = agent
        self._capabilities[name] = set(capabilities)

    def get(self, name: str) -> Any:
        try:
            return self._agents[name]
        except KeyError as error:
            raise KeyError(f"Unknown agent: {name}") from error

    def assign(self, task: str) -> str:
        matches = [
            name for name, capabilities in self._capabilities.items()
            if task in capabilities
        ]
        if not matches:
            raise LookupError(f"No agent registered for task: {task}")
        return matches[0]

    def names(self) -> tuple[str, ...]:
        return tuple(self._agents)