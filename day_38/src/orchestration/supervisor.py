"""Run independent agents concurrently with timeout, retry, and fallback."""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Sequence

from src.agents.demo_agents import Agent
from src.agents.validator import ValidatorAgent
from src.orchestration.aggregator import aggregate_results
from src.orchestration.models import AgentResult, AgentTrace, RunStatus, UnifiedState


class AgentExecutionError(RuntimeError):
    """Raised internally when the primary and fallback both fail."""


class Supervisor:
    def __init__(
        self,
        agents: Sequence[Agent],
        *,
        fallback_agents: dict[str, Agent] | None = None,
        max_retries: int = 1,
        timeout_seconds: float = 2.0,
        trace_path: str | Path = "outputs/multi_agent_trace.json",
        validator: ValidatorAgent | None = None,
    ) -> None:
        if max_retries < 0:
            raise ValueError("max_retries must be zero or greater")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be greater than zero")
        self.agents = list(agents)
        self.fallback_agents = fallback_agents or {}
        self.max_retries = max_retries
        self.timeout_seconds = timeout_seconds
        self.trace_path = Path(trace_path)
        self.validator = validator or ValidatorAgent()
        self.traces: list[AgentTrace] = []

    async def run(self) -> UnifiedState:
        self.traces = []
        results = await asyncio.gather(*(self._run_one(agent) for agent in self.agents))
        state = aggregate_results(results)
        state.validation = self.validator.validate(results, state.conflicts).to_dict()
        self._write_trace()
        return state

    async def _run_one(self, agent: Agent) -> AgentResult:
        started = datetime.now(UTC)
        calls: list[str] = []
        errors: list[str] = []
        result: AgentResult | None = None
        status = RunStatus.FAILED
        used_fallback = False

        for attempt in range(1, self.max_retries + 2):
            calls.append(f"{agent.name}.run attempt {attempt}")
            try:
                result = await asyncio.wait_for(agent.run(), timeout=self.timeout_seconds)
                status = RunStatus.SUCCEEDED
                break
            except Exception as exc:
                message = f"{type(exc).__name__}: {exc}"
                errors.append(message)
                calls.append(f"{agent.name}.run failed: {message}")

        if result is None:
            fallback = self.fallback_agents.get(agent.name)
            if fallback is not None:
                used_fallback = True
                calls.append(f"{fallback.name}.run fallback")
                try:
                    result = await asyncio.wait_for(fallback.run(), timeout=self.timeout_seconds)
                    status = RunStatus.FALLBACK_SUCCEEDED
                except Exception as exc:
                    message = f"{type(exc).__name__}: {exc}"
                    errors.append(f"fallback {fallback.name} failed: {message}")
                    calls.append(f"{fallback.name}.run failed: {message}")

        if result is None:
            controlled_error = AgentExecutionError(
                f"{agent.name} failed after {self.max_retries + 1} attempt(s)"
                + (" and fallback" if used_fallback else "")
            )
            result = AgentResult(
                agent_name=agent.name,
                category="error",
                status=RunStatus.FAILED,
                error=f"{controlled_error}: {'; '.join(errors)}",
            )

        calls.extend(result.tool_calls)
        ended = datetime.now(UTC)
        trace = AgentTrace(
            agent=agent.name,
            start_time=started.isoformat(),
            end_time=ended.isoformat(),
            status=status,
            tool_calls=calls,
            result=result.to_dict(),
            error="; ".join(errors) if errors else None,
        )
        self.traces.append(trace)
        return result

    def _write_trace(self) -> None:
        self.trace_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"traces": [trace.to_dict() for trace in self.traces]}
        self.trace_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")