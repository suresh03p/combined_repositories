from __future__ import annotations

import unittest

from src.memory.shared_state import SharedState, StateAccessError
from src.supervisor import Supervisor
from src.tools.registry import create_default_tool_registry


QUESTION = "How did customer retention and revenue change in 2025, and what trends explain it?"


class PipelineTests(unittest.TestCase):
    def test_happy_path_returns_cited_validated_analysis(self) -> None:
        result = Supervisor().run(QUESTION)

        self.assertEqual(result["status"], "success")
        self.assertTrue(result["validation"]["validated"])
        self.assertTrue(result["sources"])
        self.assertTrue(result["analysis"]["trends"])
        self.assertIn("Sources:", result["answer"])

    def test_registry_exposes_requested_tools(self) -> None:
        self.assertEqual(
            set(create_default_tool_registry().names()),
            {"RAG Search", "Calculator", "Document Search", "Document Reader", "Validation Tool"},
        )

    def test_research_failure_retries_then_succeeds(self) -> None:
        result = Supervisor().run(QUESTION, {"researcher": ["research_failure"]})

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["decisions"][0]["decision"], "retry")

    def test_persistent_research_failure_is_skipped(self) -> None:
        result = Supervisor().run(QUESTION, {"researcher": "research_failure"})

        self.assertEqual(result["status"], "success")
        self.assertEqual(result["research"]["status"], "skipped")
        self.assertTrue(any(item["decision"] == "skip" for item in result["decisions"]))

    def test_rag_failure_delegates_to_researcher(self) -> None:
        result = Supervisor().run(QUESTION, {"rag": ["rag_failure", "rag_failure"]})

        self.assertEqual(result["status"], "success")
        self.assertTrue(any(item["decision"] == "delegate" for item in result["decisions"]))

    def test_timeout_and_invalid_response_are_retried(self) -> None:
        for fault in ("timeout", "invalid_response"):
            with self.subTest(fault=fault):
                result = Supervisor().run(QUESTION, {"analyst": [fault]})
                self.assertEqual(result["status"], "success")
                self.assertEqual(result["decisions"][0]["decision"], "retry")

    def test_missing_context_is_detected_and_delegated(self) -> None:
        result = Supervisor().run(QUESTION, {"rag": ["missing_context", "missing_context"]})

        self.assertEqual(result["status"], "success")
        self.assertTrue(any(item["decision"] == "delegate" for item in result["decisions"]))

    def test_downstream_failure_stops_workflow(self) -> None:
        result = Supervisor().run(QUESTION, {"analyst": "fail"})

        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["failed_agent"], "analyst")
        self.assertEqual(result["decisions"][-1]["decision"], "stop")

    def test_supervisor_assigns_tasks_by_capability(self) -> None:
        supervisor = Supervisor()

        self.assertEqual(supervisor.assign_task("research"), "researcher")
        self.assertEqual(supervisor.assign_task("retrieval"), "rag")
        self.assertEqual(supervisor.assign_task("analysis"), "analyst")

    def test_shared_state_enforces_agent_field_permissions(self) -> None:
        state = SharedState(QUESTION)

        with self.assertRaises(StateAccessError):
            state.read("researcher", "retrieval")
        with self.assertRaises(StateAccessError):
            state.write("analyst", "research", {})


if __name__ == "__main__":
    unittest.main()