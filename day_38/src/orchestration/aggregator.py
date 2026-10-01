"""Combine agent outputs without silently resolving disagreements."""

import json
from typing import Any, Iterable

from src.orchestration.models import AgentResult, UnifiedState


def _comparable(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=True, default=str)


def aggregate_results(results: Iterable[AgentResult]) -> UnifiedState:
    result_list = list(results)
    claims: dict[str, list[dict[str, Any]]] = {}
    for result in result_list:
        if result.status.value == "failed":
            continue
        for name, value in result.claims.items():
            claims.setdefault(name, []).append({"agent": result.agent_name, "value": value})

    conflicts = []
    for name, entries in claims.items():
        distinct_values = {_comparable(entry["value"]) for entry in entries}
        if len(distinct_values) > 1:
            conflicts.append({"claim": name, "status": "CONFLICT DETECTED", "values": entries})

    return UnifiedState(
        results=[result.to_dict() for result in result_list],
        claims=claims,
        conflicts=conflicts,
        validation={},
    )