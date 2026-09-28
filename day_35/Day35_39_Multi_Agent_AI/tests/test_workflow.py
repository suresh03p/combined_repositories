import unittest

from src.agents.supervisor import SupervisorAgent
from src.orchestration.state import AgentState


class SupervisorWorkflowTests(unittest.TestCase):
    def test_agents_return_results_before_supervisor_dispatches_next_stage(self) -> None:
        supervisor = SupervisorAgent()
        state = supervisor.run(AgentState(
            conversation_id="test-research",
            user_request="How can a supervisor coordinate specialized agents using shared state?",
        ))

        self.assertEqual(state.task_status, "completed")
        self.assertTrue(state.research_results)
        self.assertTrue(state.retrieved_documents)
        self.assertTrue(state.analysis_results)
        self.assertTrue(state.validation_results["is_valid"])
        self.assertTrue(state.final_response)

        for index, handoff in enumerate(supervisor.handoffs):
            if handoff["to"] == "supervisor" and index + 1 < len(supervisor.handoffs):
                next_handoff = supervisor.handoffs[index + 1]
                self.assertEqual(next_handoff["from"], "supervisor")

    def test_empty_search_results_complete_without_looping(self) -> None:
        supervisor = SupervisorAgent()
        state = supervisor.run(AgentState(
            conversation_id="test-no-results",
            user_request="quantum volcano",
        ))

        self.assertEqual(state.task_status, "completed")
        self.assertEqual(state.research_results, [])
        self.assertEqual(state.retrieved_documents, [])
        self.assertFalse(state.validation_results["is_valid"])
        self.assertIn("No evidence-backed conclusion", state.final_response)
        completed_agents = [
            handoff["from"]
            for handoff in supervisor.handoffs
            if handoff["to"] == "supervisor"
        ]
        self.assertEqual(
            completed_agents,
            ["researcher", "rag_agent", "analyst", "validator", "writer"],
        )

    def test_empty_request_fails_without_dispatch(self) -> None:
        supervisor = SupervisorAgent()
        state = supervisor.run(AgentState(
            conversation_id="test-empty",
            user_request="  ",
        ))

        self.assertEqual(state.task_status, "failed")
        self.assertEqual(supervisor.handoffs, [])
        self.assertTrue(state.errors)


if __name__ == "__main__":
    unittest.main()
