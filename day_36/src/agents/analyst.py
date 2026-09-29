"""Analysis agent: compares retrieved metrics and identifies trends."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from src.agents.common import MissingContextError, success
from src.memory.shared_state import SharedState
from src.tools.registry import ToolRegistry


class AnalystAgent:
    name = "analyst"

    def __init__(self, tools: ToolRegistry) -> None:
        self.tools = tools

    def run(self, state: SharedState) -> dict[str, Any]:
        retrieval = state.read(self.name, "retrieval")
        if not retrieval or not retrieval.get("context"):
            raise MissingContextError("Analyst requires retrieved document context")

        facts = list(
            dict.fromkeys(
                fact
                for document in retrieval["context"]
                for fact in document.get("facts", [])
            )
        )
        grouped_metrics: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for document in retrieval["context"]:
            for metric in document.get("metrics", []):
                grouped_metrics[(metric["name"], metric["unit"])].append(metric)

        comparisons: list[dict[str, Any]] = []
        for (name, unit), observations in grouped_metrics.items():
            observations.sort(key=lambda metric: metric["period"])
            for earlier, later in zip(observations, observations[1:]):
                difference = self.tools.execute(
                    "Calculator",
                    expression=f"{later['value']} - {earlier['value']}",
                )["result"]
                comparison: dict[str, Any] = {
                    "metric": name,
                    "from": earlier["period"],
                    "to": later["period"],
                    "change": difference,
                    "unit": unit,
                }
                if earlier["value"] != 0:
                    comparison["relative_change_percent"] = self.tools.execute(
                        "Calculator",
                        expression=f"({difference} / {earlier['value']}) * 100",
                    )["result"]
                comparisons.append(comparison)

        trends = [
            {
                **comparison,
                "direction": "up" if comparison["change"] > 0 else "down" if comparison["change"] < 0 else "unchanged",
            }
            for comparison in comparisons
        ]
        summary = f"Reviewed {len(retrieval['context'])} sources and identified {len(trends)} comparable trends."
        result = success(
            self.name,
            summary=summary,
            findings=facts,
            comparisons=comparisons,
            trends=trends,
        )
        state.write(self.name, "analysis", result)
        return result