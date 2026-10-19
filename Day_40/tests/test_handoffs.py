import json
import unittest
from pathlib import Path

from durable_agent_runner.handoffs import (
    AgentHandoffError,
    HandoffValidationError,
    make_handoff,
    validate_handoff,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class HandoffContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.task_id = "task-123"
        self.planner_payload = {
            "goal": "Summarize the topic",
            "research_questions": ["What are the key facts?"],
        }
        self.planner_handoff = make_handoff(
            "plan", self.task_id, self.planner_payload
        )

    def test_valid_planner_handoff_passes_and_preserves_payload(self) -> None:
        payload = validate_handoff(
            self.planner_handoff, "plan", self.task_id
        )
        self.assertEqual(payload, self.planner_payload)

    def test_wrong_recipient_is_rejected(self) -> None:
        handoff = {**self.planner_handoff, "to_role": "validator"}
        with self.assertRaisesRegex(HandoffValidationError, "to_role"):
            validate_handoff(handoff, "plan", self.task_id)

    def test_wrong_execution_and_extra_fields_are_rejected(self) -> None:
        with self.assertRaisesRegex(HandoffValidationError, "task_id"):
            validate_handoff(self.planner_handoff, "plan", "another-task")

        handoff = {**self.planner_handoff, "uncontracted": True}
        with self.assertRaisesRegex(HandoffValidationError, "fields must be exactly"):
            validate_handoff(handoff, "plan", self.task_id)

    def test_malformed_role_payload_is_rejected(self) -> None:
        handoff = {
            **self.planner_handoff,
            "payload": {"goal": "No questions"},
        }
        with self.assertRaisesRegex(HandoffValidationError, "goal and research_questions"):
            validate_handoff(handoff, "plan", self.task_id)

    def test_structured_agent_error_is_not_treated_as_completed_output(self) -> None:
        handoff = {
            "schema_version": "1.0",
            "from_role": "planner",
            "to_role": "researcher",
            "task_id": self.task_id,
            "status": "error",
            "error": {"code": "planning_failed", "message": "No plan available."},
        }
        with self.assertRaisesRegex(AgentHandoffError, "planning_failed"):
            validate_handoff(handoff, "plan", self.task_id)

    def test_json_schema_documents_all_role_contracts(self) -> None:
        handoff_schema = json.loads(
            (PROJECT_ROOT / "schemas" / "agent-handoff.schema.json").read_text(
                encoding="utf-8"
            )
        )
        role_schema = json.loads(
            (PROJECT_ROOT / "schemas" / "role-contracts.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(handoff_schema["$schema"], role_schema["$schema"])
        self.assertEqual(
            set(role_schema["$defs"]),
            {
                "plannerInput",
                "plannerOutput",
                "researcherInput",
                "researcherOutput",
                "validatorInput",
                "validatorOutput",
            },
        )
        self.assertEqual(len(handoff_schema["allOf"][1]["oneOf"]), 6)


if __name__ == "__main__":
    unittest.main()
