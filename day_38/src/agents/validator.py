"""Validate evidence quality and surface contradictions for human review."""

import math
from collections.abc import Iterable

from src.orchestration.models import AgentResult, RunStatus, ValidationReport


class ValidatorAgent:
    name = "validator_agent"

    def validate(
        self,
        results: Iterable[AgentResult],
        conflicts: list[dict[str, object]],
    ) -> ValidationReport:
        issues: list[str] = []
        for result in results:
            if result.status is RunStatus.FAILED:
                issues.append(f"{result.agent_name}: execution failed: {result.error or 'unknown error'}")
                continue
            if not any(source.strip() for source in result.sources):
                issues.append(f"{result.agent_name}: missing source")
            if not any(item.strip() for item in result.evidence):
                issues.append(f"{result.agent_name}: missing evidence")
            if not result.citations or any(not self._is_citation(item) for item in result.citations):
                issues.append(f"{result.agent_name}: missing or malformed citation")
            for name, calculation in result.calculations.items():
                expected = calculation.get("expected")
                actual = calculation.get("actual")
                tolerance = calculation.get("tolerance", 0.0)
                if expected is None or actual is None or not math.isclose(
                    expected, actual, rel_tol=0.0, abs_tol=tolerance
                ):
                    issues.append(f"{result.agent_name}: calculation check failed for {name}")

        for conflict in conflicts:
            issues.append(f"CONFLICT DETECTED for {conflict['claim']}: validation required")
        return ValidationReport(valid=not issues, issues=issues)

    @staticmethod
    def _is_citation(value: str) -> bool:
        citation = value.strip().lower()
        return citation.startswith(("https://", "http://", "doi:", "demo:"))