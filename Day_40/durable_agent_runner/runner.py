import json
from concurrent.futures import Future, ThreadPoolExecutor
from threading import Lock
from typing import Any, Callable
from uuid import uuid4

from .models import ExecutionStatus, StepContext
from .store import ExecutionNotFound, ExecutionStore, IdempotencyConflict


STEP_NAMES = ("plan", "research", "respond")
StepHandler = Callable[[StepContext], Any]


def _plan(context: StepContext) -> dict[str, Any]:
    return {
        "goal": context.input_text.strip(),
        "next_steps": ["research", "respond"],
        "idempotency_key": context.idempotency_key,
    }


def _research(context: StepContext) -> dict[str, Any]:
    return {
        "notes": [f"Demo research completed for: {context.input_text.strip()}"],
        "idempotency_key": context.idempotency_key,
    }


def _respond(context: StepContext) -> dict[str, Any]:
    research = context.previous_outputs["research"]
    return {
        "answer": research["notes"][0],
        "conversation_id": context.conversation_id,
        "idempotency_key": context.idempotency_key,
    }


class DurableAgentRunner:
    """Execute a sequential workflow and persist each completed step."""

    def __init__(
        self,
        store: ExecutionStore,
        step_handlers: dict[str, StepHandler] | None = None,
        max_workers: int = 4,
        recover_on_start: bool = True,
    ) -> None:
        self.store = store
        self.step_handlers = (
            step_handlers
            if step_handlers is not None
            else {"plan": _plan, "research": _research, "respond": _respond}
        )
        if tuple(self.step_handlers) != STEP_NAMES:
            raise ValueError(f"Step handlers must be ordered as {STEP_NAMES}.")
        self._executor = ThreadPoolExecutor(
            max_workers=max_workers, thread_name_prefix="durable-agent"
        )
        self._lock = Lock()
        self._scheduled: dict[str, Future[None]] = {}
        if recover_on_start:
            self.store.export_all_histories()
            self.recover()

    def create_execution(
        self,
        input_text: str,
        idempotency_key: str | None = None,
        conversation_id: str | None = None,
    ) -> tuple[dict[str, Any], bool]:
        if not input_text.strip():
            raise ValueError("input_text must not be empty.")
        if conversation_id is not None and not conversation_id.strip():
            raise ValueError("conversation_id must not be empty.")
        key = idempotency_key if idempotency_key is not None else str(uuid4())
        if not key.strip() or len(key) > 200:
            raise ValueError("idempotency_key must be non-empty and at most 200 characters.")
        execution, created = self.store.create(
            input_text.strip(), key, conversation_id, STEP_NAMES[0]
        )
        if execution["status"] == ExecutionStatus.QUEUED:
            self._schedule(execution["task_id"])
        return execution, created

    def recover(self) -> list[str]:
        recovered = self.store.recover_interrupted(STEP_NAMES[0])
        for task_id in recovered:
            self._schedule(task_id)
        return recovered

    def _schedule(self, task_id: str) -> None:
        with self._lock:
            existing = self._scheduled.get(task_id)
            if existing is not None and not existing.done():
                return
            future = self._executor.submit(self._run, task_id)
            self._scheduled[task_id] = future

    def _run(self, task_id: str) -> None:
        for step in STEP_NAMES:
            execution = self.store.get(task_id)
            if execution["status"] in (
                ExecutionStatus.CANCELLED,
                ExecutionStatus.COMPLETED,
                ExecutionStatus.FAILED,
            ):
                return
            if execution["status"] == ExecutionStatus.WAITING:
                return
            if execution["pause_requested"]:
                self.store.finish(task_id, ExecutionStatus.WAITING)
                return
            checkpoint = execution["checkpoints"].get(step, {})
            if checkpoint.get("status") == "completed":
                continue

            idempotency_key = checkpoint.get(
                "idempotency_key", f"{task_id}:{step}"
            )
            execution = self.store.set_step_running(
                task_id, step, idempotency_key
            )
            if execution["cancel_requested"]:
                self.store.finish(task_id, ExecutionStatus.CANCELLED)
                return
            if execution["pause_requested"]:
                self.store.finish(task_id, ExecutionStatus.WAITING)
                return

            previous_outputs = {
                name: details["output"]
                for name, details in execution["checkpoints"].items()
                if details.get("status") == "completed"
            }
            context = StepContext(
                task_id=task_id,
                conversation_id=execution["conversation_id"],
                input_text=execution["input_text"],
                previous_outputs=previous_outputs,
                idempotency_key=idempotency_key,
            )
            try:
                output = self.step_handlers[step](context)
                json.dumps(output, allow_nan=False)
            except Exception as error:
                self.store.fail(task_id, step, error)
                return

            execution = self.store.complete_step(
                task_id,
                step,
                output,
                STEP_NAMES[min(STEP_NAMES.index(step) + 1, len(STEP_NAMES) - 1)],
            )
            if execution["status"] == ExecutionStatus.CANCELLED:
                return
            if execution["status"] == ExecutionStatus.WAITING:
                return
            if execution["cancel_requested"]:
                self.store.finish(task_id, ExecutionStatus.CANCELLED)
                return

        self.store.finish(task_id, ExecutionStatus.COMPLETED)

    def resume(self, task_id: str) -> dict[str, Any]:
        execution = self.store.queue_resume(task_id, STEP_NAMES[0])
        self._schedule(task_id)
        return execution

    def pause(self, task_id: str) -> dict[str, Any]:
        return self.store.request_pause(task_id)

    def cancel(self, task_id: str) -> dict[str, Any]:
        execution = self.store.request_cancel(task_id)
        if execution["status"] == ExecutionStatus.CANCELLED:
            return self.store.finish(task_id, ExecutionStatus.CANCELLED)
        return execution

    def get_execution(self, task_id: str) -> dict[str, Any]:
        return self.store.get(task_id)

    def list_executions(self, limit: int = 100) -> list[dict[str, Any]]:
        return self.store.list(limit)

    def get_history(self, task_id: str) -> dict[str, Any]:
        return {
            "execution": self.store.get(task_id),
            "events": self.store.events(task_id),
        }

    def wait_for(self, task_id: str, timeout: float = 5.0) -> dict[str, Any]:
        with self._lock:
            future = self._scheduled.get(task_id)
        if future is not None:
            future.result(timeout=timeout)
        return self.store.get(task_id)

    def close(self, wait: bool = True) -> None:
        self._executor.shutdown(wait=wait, cancel_futures=False)


__all__ = [
    "DurableAgentRunner",
    "ExecutionNotFound",
    "IdempotencyConflict",
    "STEP_NAMES",
    "StepContext",
]
