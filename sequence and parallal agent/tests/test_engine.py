import asyncio
import json
import tempfile
import unittest
from pathlib import Path

from src.agents.demo_agents import Agent
from src.agents.validator import ValidatorAgent
from src.orchestration.models import AgentResult, RunStatus
from src.orchestration.supervisor import Supervisor


def valid_result(agent_name: str, **claims: object) -> AgentResult:
    return AgentResult(
        agent_name=agent_name,
        category="test",
        claims=claims,
        sources=["Test source"],
        evidence=["Observed test evidence"],
        citations=["https://example.test/source"],
    )


class BarrierAgent:
    active = 0
    peak_active = 0
    ready = asyncio.Event()

    def __init__(self, name: str) -> None:
        self.name = name

    async def run(self) -> AgentResult:
        type(self).active += 1
        type(self).peak_active = max(type(self).peak_active, type(self).active)
        if type(self).active >= 2:
            type(self).ready.set()
        try:
            await asyncio.wait_for(type(self).ready.wait(), timeout=0.5)
            return valid_result(self.name, shared="ok")
        finally:
            type(self).active -= 1


class FlakyAgent:
    name = "flaky"

    def __init__(self) -> None:
        self.calls = 0

    async def run(self) -> AgentResult:
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("temporary failure")
        return valid_result(self.name, answer="recovered")


class SuccessfulAgent:
    def __init__(self, name: str) -> None:
        self.name = name

    async def run(self) -> AgentResult:
        return valid_result(self.name, answer="backup result")


class AlwaysFailAgent:
    def __init__(self, name: str, delay: float = 0) -> None:
        self.name = name
        self.delay = delay
        self.calls = 0

    async def run(self) -> AgentResult:
        self.calls += 1
        if self.delay:
            await asyncio.sleep(self.delay)
        raise RuntimeError("unavailable")


class EngineTests(unittest.TestCase):
    def test_independent_agents_overlap(self) -> None:
        BarrierAgent.active = 0
        BarrierAgent.peak_active = 0
        BarrierAgent.ready = asyncio.Event()

        async def run_test() -> None:
            with tempfile.TemporaryDirectory() as temp_dir:
                supervisor = Supervisor(
                    [BarrierAgent("one"), BarrierAgent("two")],
                    trace_path=Path(temp_dir) / "trace.json",
                )
                state = await supervisor.run()
                self.assertEqual(len(state.results), 2)

        asyncio.run(run_test())
        self.assertGreaterEqual(BarrierAgent.peak_active, 2)

    def test_retry_then_fallback_and_trace(self) -> None:
        async def run_test() -> None:
            with tempfile.TemporaryDirectory() as temp_dir:
                primary = FlakyAgent()
                supervisor = Supervisor(
                    [primary], max_retries=1,
                    trace_path=Path(temp_dir) / "trace.json",
                )
                state = await supervisor.run()
                self.assertEqual(primary.calls, 2)
                self.assertEqual(state.results[0]["claims"]["answer"], "recovered")

                failed = AlwaysFailAgent("primary")
                backup = SuccessfulAgent("backup")
                supervisor = Supervisor(
                    [failed], fallback_agents={"primary": backup}, max_retries=1,
                    trace_path=Path(temp_dir) / "fallback-trace.json",
                )
                await supervisor.run()
                trace = json.loads((Path(temp_dir) / "fallback-trace.json").read_text())
                entry = trace["traces"][0]
                self.assertEqual(entry["status"], RunStatus.FALLBACK_SUCCEEDED.value)
                self.assertEqual(failed.calls, 2)
                self.assertTrue(any("backup.run fallback" in call for call in entry["tool_calls"]))
                self.assertTrue(entry["start_time"])
                self.assertTrue(entry["end_time"])
                self.assertIsNotNone(entry["result"])

        asyncio.run(run_test())

    def test_timeout_and_failed_fallback_become_controlled_error(self) -> None:
        async def run_test() -> None:
            with tempfile.TemporaryDirectory() as temp_dir:
                primary = AlwaysFailAgent("primary", delay=0.1)
                fallback = AlwaysFailAgent("backup", delay=0.1)
                supervisor = Supervisor(
                    [primary], fallback_agents={"primary": fallback},
                    max_retries=1, timeout_seconds=0.01,
                    trace_path=Path(temp_dir) / "trace.json",
                )
                state = await supervisor.run()
                self.assertEqual(primary.calls, 2)
                self.assertEqual(fallback.calls, 1)
                self.assertEqual(state.results[0]["status"], RunStatus.FAILED.value)
                self.assertIn("failed after 2 attempt(s) and fallback", state.results[0]["error"])
                self.assertFalse(state.validation["valid"])

        asyncio.run(run_test())

    def test_validator_checks_sources_evidence_calculation_citations_and_conflicts(self) -> None:
        result = AgentResult(
            agent_name="incomplete",
            category="test",
            calculations={"total": {"expected": 10.0, "actual": 12.0}},
        )
        report = ValidatorAgent().validate(
            [result], [{"claim": "revenue", "status": "CONFLICT DETECTED"}]
        )
        self.assertFalse(report.valid)
        self.assertTrue(any("missing source" in issue for issue in report.issues))
        self.assertTrue(any("missing evidence" in issue for issue in report.issues))
        self.assertTrue(any("citation" in issue for issue in report.issues))
        self.assertTrue(any("calculation check failed" in issue for issue in report.issues))
        self.assertTrue(any("CONFLICT DETECTED" in issue for issue in report.issues))


if __name__ == "__main__":
    unittest.main()