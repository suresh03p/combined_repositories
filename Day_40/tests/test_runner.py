import json
import tempfile
import threading
import time
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from durable_agent_runner.api import create_server
from durable_agent_runner.handoffs import make_handoff
from durable_agent_runner.models import ExecutionStatus
from durable_agent_runner.runner import DurableAgentRunner, STEP_NAMES
from durable_agent_runner.store import ExecutionStore, IdempotencyConflict


def valid_handoff(step: str, task_id: str):
    payloads = {
        "plan": {"goal": "test goal", "research_questions": ["test question"]},
        "research": {
            "findings": [{"claim": "test claim", "evidence": "test evidence"}],
            "limitations": [],
        },
        "respond": {"accepted": True, "answer": "test answer", "issues": []},
    }
    return make_handoff(step, task_id, payloads[step])


class SimulatedProcessCrash(BaseException):
    pass


class DurableAgentRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.store = ExecutionStore(
            self.root / "state.sqlite3", self.root / "history"
        )
        self.runner = DurableAgentRunner(self.store)

    def tearDown(self) -> None:
        self.runner.close()
        self.temp_dir.cleanup()

    def test_workflow_persists_checkpoints_and_json_history(self) -> None:
        execution, created = self.runner.create_execution(
            "Build a durable workflow", "request-1"
        )
        self.assertTrue(created)
        finished = self.runner.wait_for(execution["task_id"])

        self.assertEqual(finished["status"], ExecutionStatus.COMPLETED)
        self.assertEqual(finished["conversation_id"], execution["conversation_id"])
        self.assertEqual(
            [finished["checkpoints"][step]["status"] for step in STEP_NAMES],
            ["completed", "completed", "completed"],
        )
        history_path = self.root / "history" / f"{execution['task_id']}.json"
        history = json.loads(history_path.read_text(encoding="utf-8"))
        self.assertEqual(history["execution"]["status"], ExecutionStatus.COMPLETED)
        self.assertEqual(
            sum(event["event"] == "step_checkpointed" for event in history["events"]),
            len(STEP_NAMES),
        )

    def test_task_idempotency_returns_original_task_and_rejects_conflicts(self) -> None:
        original, created = self.runner.create_execution("same request", "same-key")
        duplicate, duplicate_created = self.runner.create_execution(
            "same request", "same-key"
        )
        self.assertTrue(created)
        self.assertFalse(duplicate_created)
        self.assertEqual(original["task_id"], duplicate["task_id"])
        with self.assertRaises(IdempotencyConflict):
            self.runner.create_execution("different request", "same-key")

    def test_restart_resumes_from_last_completed_checkpoint(self) -> None:
        calls: dict[str, int] = {step: 0 for step in STEP_NAMES}
        step_keys: dict[str, list[str]] = {step: [] for step in STEP_NAMES}
        crash_once = True

        def handler_for(step: str):
            def handle(context):
                nonlocal crash_once
                calls[step] += 1
                step_keys[step].append(context.idempotency_key)
                if step == "research" and crash_once:
                    crash_once = False
                    raise SimulatedProcessCrash()
                return valid_handoff(step, context.task_id)
            return handle

        handlers = {step: handler_for(step) for step in STEP_NAMES}
        self.runner.close()
        first_process = DurableAgentRunner(
            self.store, handlers, recover_on_start=False
        )
        execution, _ = first_process.create_execution("resume me", "restart-key")
        with self.assertRaises(SimulatedProcessCrash):
            first_process.wait_for(execution["task_id"])
        self.assertEqual(self.store.get(execution["task_id"])["status"], ExecutionStatus.RUNNING)
        self.assertEqual(calls["plan"], 1)
        self.assertEqual(calls["research"], 1)
        first_process.close()

        restarted_process = DurableAgentRunner(self.store, handlers)
        try:
            finished = restarted_process.wait_for(execution["task_id"])
            self.assertEqual(finished["status"], ExecutionStatus.COMPLETED)
            self.assertEqual(calls["plan"], 1, "completed work must not be repeated")
            self.assertEqual(calls["research"], 2)
            self.assertEqual(calls["respond"], 1)
            self.assertEqual(step_keys["research"][0], step_keys["research"][1])
        finally:
            restarted_process.close()
            self.runner = DurableAgentRunner(self.store, recover_on_start=False)

    def test_failed_step_can_resume_without_repeating_completed_work(self) -> None:
        calls = {"plan": 0, "research": 0, "respond": 0}

        def make_handler(step: str):
            def handler(context):
                calls[step] += 1
                if step == "research" and calls[step] == 1:
                    raise RuntimeError("temporary tool error")
                return valid_handoff(step, context.task_id)
            return handler

        self.runner.close()
        self.runner = DurableAgentRunner(
            self.store,
            {step: make_handler(step) for step in STEP_NAMES},
            recover_on_start=False,
            retry_budget=0,
        )
        execution, _ = self.runner.create_execution("retry me", "retry-key")
        failed = self.runner.wait_for(execution["task_id"])
        self.assertEqual(failed["status"], ExecutionStatus.FAILED)
        self.assertEqual(len(failed["errors"]), 1)

        self.runner.resume(execution["task_id"])
        completed = self.runner.wait_for(execution["task_id"])
        self.assertEqual(completed["status"], ExecutionStatus.COMPLETED)
        self.assertEqual(calls, {"plan": 1, "research": 2, "respond": 1})

    def test_pause_enters_waiting_and_resume_continues_at_next_step(self) -> None:
        entered = threading.Event()
        release = threading.Event()
        calls = {step: 0 for step in STEP_NAMES}

        def make_handler(step: str):
            def handler(context):
                calls[step] += 1
                if step == "plan" and calls[step] == 1:
                    entered.set()
                    self.assertTrue(release.wait(timeout=3))
                return valid_handoff(step, context.task_id)
            return handler

        self.runner.close()
        self.runner = DurableAgentRunner(
            self.store,
            {step: make_handler(step) for step in STEP_NAMES},
            recover_on_start=False,
        )
        execution, _ = self.runner.create_execution("pause me", "pause-key")
        self.assertTrue(entered.wait(timeout=2))
        self.runner.pause(execution["task_id"])
        release.set()
        waiting = self.runner.wait_for(execution["task_id"])
        self.assertEqual(waiting["status"], ExecutionStatus.WAITING)

        self.runner.resume(execution["task_id"])
        finished = self.runner.wait_for(execution["task_id"])
        self.assertEqual(finished["status"], ExecutionStatus.COMPLETED)
        self.assertEqual(calls, {"plan": 1, "research": 1, "respond": 1})

    def test_cancel_during_a_step_stops_before_the_next_step(self) -> None:
        entered = threading.Event()
        release = threading.Event()
        calls = {step: 0 for step in STEP_NAMES}

        def make_handler(step: str):
            def handler(context):
                calls[step] += 1
                if step == "plan":
                    entered.set()
                    self.assertTrue(release.wait(timeout=3))
                return valid_handoff(step, context.task_id)
            return handler

        self.runner.close()
        self.runner = DurableAgentRunner(
            self.store,
            {step: make_handler(step) for step in STEP_NAMES},
            recover_on_start=False,
        )
        execution, _ = self.runner.create_execution("cancel me", "cancel-key")
        self.assertTrue(entered.wait(timeout=2))
        self.runner.cancel(execution["task_id"])
        release.set()
        cancelled = self.runner.wait_for(execution["task_id"])
        self.assertEqual(cancelled["status"], ExecutionStatus.CANCELLED)
        self.assertEqual(
            cancelled["checkpoints"]["plan"]["status"], "cancelled"
        )
        self.assertNotIn("output", cancelled["checkpoints"]["plan"])
        self.assertEqual(calls, {"plan": 1, "research": 0, "respond": 0})

    def test_timed_out_step_retries_with_same_idempotency_key(self) -> None:
        first_call_started = threading.Event()
        release_first_call = threading.Event()
        calls = {step: 0 for step in STEP_NAMES}
        keys: list[str] = []

        def make_handler(step: str):
            def handler(context):
                calls[step] += 1
                if step == "plan":
                    keys.append(context.idempotency_key)
                    if calls[step] == 1:
                        first_call_started.set()
                        release_first_call.wait(timeout=2)
                return valid_handoff(step, context.task_id)
            return handler

        self.runner.close()
        self.runner = DurableAgentRunner(
            self.store,
            {step: make_handler(step) for step in STEP_NAMES},
            max_workers=2,
            recover_on_start=False,
            step_timeout=0.05,
            retry_budget=1,
        )
        execution, _ = self.runner.create_execution("retry timeout", "timeout-key")
        self.assertTrue(first_call_started.wait(timeout=1))
        try:
            completed = self.runner.wait_for(execution["task_id"], timeout=2)
        finally:
            release_first_call.set()

        self.assertEqual(completed["status"], ExecutionStatus.COMPLETED)
        self.assertEqual(calls["plan"], 2)
        self.assertEqual(keys, [f"{execution['task_id']}:plan"] * 2)
        self.assertEqual(
            completed["checkpoints"]["plan"]["status"], "completed"
        )

    def test_exhausted_timeout_budget_fails_without_checkpointing_output(self) -> None:
        entered = threading.Event()
        release = threading.Event()
        calls = {"plan": 0, "research": 0, "respond": 0}

        def make_handler(step: str):
            def handler(context):
                calls[step] += 1
                if step == "plan":
                    entered.set()
                    release.wait(timeout=2)
                return valid_handoff(step, context.task_id)
            return handler

        self.runner.close()
        self.runner = DurableAgentRunner(
            self.store,
            {step: make_handler(step) for step in STEP_NAMES},
            max_workers=2,
            recover_on_start=False,
            step_timeout=0.05,
            retry_budget=1,
        )
        execution, _ = self.runner.create_execution("fail timeout", "timeout-fail")
        self.assertTrue(entered.wait(timeout=1))
        try:
            failed = self.runner.wait_for(execution["task_id"], timeout=2)
        finally:
            release.set()

        self.assertEqual(failed["status"], ExecutionStatus.FAILED)
        self.assertEqual(calls, {"plan": 2, "research": 0, "respond": 0})
        self.assertEqual(failed["checkpoints"]["plan"]["status"], "failed")
        self.assertNotIn("output", failed["checkpoints"]["plan"])
        self.assertIn("TimeoutError", failed["errors"][0]["message"])

    def test_malformed_handoff_fails_execution_before_next_role_runs(self) -> None:
        calls = {"research": 0, "respond": 0}
        malformed_calls = 0

        def malformed_plan(context):
            nonlocal malformed_calls
            malformed_calls += 1
            return {
                "schema_version": "1.0",
                "from_role": "planner",
                "to_role": "validator",
                "task_id": context.task_id,
                "status": "completed",
                "payload": {
                    "goal": "invalid route",
                    "research_questions": ["question"],
                },
            }

        def later_step(step):
            def handler(context):
                calls[step] += 1
                return valid_handoff(step, context.task_id)
            return handler

        self.runner.close()
        self.runner = DurableAgentRunner(
            self.store,
            {
                "plan": malformed_plan,
                "research": later_step("research"),
                "respond": later_step("respond"),
            },
            recover_on_start=False,
        )
        execution, _ = self.runner.create_execution("reject bad handoff", "bad-handoff")
        failed = self.runner.wait_for(execution["task_id"])

        self.assertEqual(failed["status"], ExecutionStatus.FAILED)
        self.assertIn("to_role must be 'researcher'", failed["errors"][0]["message"])
        self.assertEqual(failed["checkpoints"]["plan"]["status"], "failed")
        self.assertNotIn("output", failed["checkpoints"]["plan"])
        self.assertEqual(malformed_calls, 1)
        self.assertEqual(calls, {"research": 0, "respond": 0})


class ExecutionAPITests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        self.runner = DurableAgentRunner(
            ExecutionStore(root / "api.sqlite3", root / "history")
        )
        self.server = create_server(self.runner, port=0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_address[1]}"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.runner.close()
        self.temp_dir.cleanup()

    def request(self, path: str, method: str = "GET", body=None, headers=None):
        data = None if body is None else json.dumps(body).encode("utf-8")
        request = Request(
            self.base_url + path,
            data=data,
            method=method,
            headers={"Content-Type": "application/json", **(headers or {})},
        )
        try:
            with urlopen(request, timeout=3) as response:
                return response.status, json.loads(response.read())
        except HTTPError as error:
            with error:
                return error.code, json.loads(error.read())

    def test_create_status_and_history_endpoints(self) -> None:
        status, created = self.request(
            "/executions",
            "POST",
            {"input_text": "status api"},
            {"Idempotency-Key": "http-key"},
        )
        self.assertEqual(status, 202)
        task_id = created["task_id"]
        for _ in range(100):
            status, state = self.request(f"/executions/{task_id}")
            if state["status"] == ExecutionStatus.COMPLETED:
                break
            time.sleep(0.01)
        self.assertEqual(status, 200)
        self.assertEqual(state["status"], ExecutionStatus.COMPLETED)
        history_status, history = self.request(f"/executions/{task_id}/history")
        self.assertEqual(history_status, 200)
        self.assertTrue(history["events"])

    def test_invalid_input_and_unknown_execution_return_errors(self) -> None:
        status, body = self.request("/executions", "POST", {"input_text": " "})
        self.assertEqual(status, 400)
        self.assertIn("error", body)
        status, body = self.request("/executions/not-a-task")
        self.assertEqual(status, 404)
        self.assertIn("error", body)


if __name__ == "__main__":
    unittest.main()
