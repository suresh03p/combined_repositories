from __future__ import annotations

import json
import os
import sqlite3
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any, Iterator
from uuid import uuid4

from .models import ExecutionStatus


class IdempotencyConflict(ValueError):
    """An idempotency key was reused for a different request."""


class ExecutionNotFound(LookupError):
    """The requested execution does not exist."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class ExecutionStore:
    """SQLite-backed execution state and append-only execution history."""

    def __init__(self, database_path: str | Path, history_dir: str | Path) -> None:
        self.database_path = Path(database_path)
        self.history_dir = Path(history_dir)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self._history_export_lock = Lock()
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path, timeout=30)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 30000")
        return connection

    @contextmanager
    def _connection(self) -> Iterator[sqlite3.Connection]:
        connection = self._connect()
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self._connection() as connection:
            connection.execute("PRAGMA journal_mode = WAL")
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS executions (
                    task_id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL,
                    input_text TEXT NOT NULL,
                    status TEXT NOT NULL CHECK (
                        status IN ('queued', 'running', 'waiting', 'completed', 'failed', 'cancelled')
                    ),
                    current_step TEXT NOT NULL,
                    checkpoints TEXT NOT NULL DEFAULT '{}',
                    errors TEXT NOT NULL DEFAULT '[]',
                    idempotency_key TEXT NOT NULL UNIQUE,
                    cancel_requested INTEGER NOT NULL DEFAULT 0,
                    pause_requested INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS execution_events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL REFERENCES executions(task_id),
                    event TEXT NOT NULL,
                    status TEXT NOT NULL,
                    step TEXT,
                    detail TEXT,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS execution_events_task_id
                    ON execution_events(task_id, event_id);
                """
            )

    @staticmethod
    def _decode(row: sqlite3.Row) -> dict[str, Any]:
        execution = dict(row)
        execution["checkpoints"] = json.loads(execution["checkpoints"])
        execution["errors"] = json.loads(execution["errors"])
        execution["cancel_requested"] = bool(execution["cancel_requested"])
        execution["pause_requested"] = bool(execution["pause_requested"])
        return execution

    @staticmethod
    def _event(
        connection: sqlite3.Connection,
        task_id: str,
        event: str,
        status: str,
        step: str | None = None,
        detail: str | None = None,
    ) -> None:
        connection.execute(
            """
            INSERT INTO execution_events (task_id, event, status, step, detail, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (task_id, event, status, step, detail, utc_now()),
        )

    def _require(self, connection: sqlite3.Connection, task_id: str) -> sqlite3.Row:
        row = connection.execute(
            "SELECT * FROM executions WHERE task_id = ?", (task_id,)
        ).fetchone()
        if row is None:
            raise ExecutionNotFound(task_id)
        return row

    def create(
        self,
        input_text: str,
        idempotency_key: str,
        conversation_id: str | None = None,
        first_step: str = "plan",
    ) -> tuple[dict[str, Any], bool]:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            existing = connection.execute(
                "SELECT * FROM executions WHERE idempotency_key = ?",
                (idempotency_key,),
            ).fetchone()
            if existing is not None:
                if (
                    existing["input_text"] != input_text
                    or (
                        conversation_id is not None
                        and existing["conversation_id"] != conversation_id
                    )
                ):
                    raise IdempotencyConflict(
                        "The idempotency key already belongs to a different request."
                    )
                execution = self._decode(existing)
                created = False
            else:
                now = utc_now()
                task_id = str(uuid4())
                actual_conversation_id = conversation_id or str(uuid4())
                connection.execute(
                    """
                    INSERT INTO executions (
                        task_id, conversation_id, input_text, status, current_step,
                        idempotency_key, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        task_id,
                        actual_conversation_id,
                        input_text,
                        ExecutionStatus.QUEUED,
                        first_step,
                        idempotency_key,
                        now,
                        now,
                    ),
                )
                self._event(
                    connection, task_id, "execution_queued",
                    ExecutionStatus.QUEUED, first_step,
                )
                execution = self._decode(self._require(connection, task_id))
                created = True
        if created:
            self.export_history(execution["task_id"])
        return execution, created

    def get(self, task_id: str) -> dict[str, Any]:
        with self._connection() as connection:
            return self._decode(self._require(connection, task_id))

    def list(self, limit: int = 100) -> list[dict[str, Any]]:
        with self._connection() as connection:
            rows = connection.execute(
                "SELECT * FROM executions ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [self._decode(row) for row in rows]

    def events(self, task_id: str) -> list[dict[str, Any]]:
        with self._connection() as connection:
            self._require(connection, task_id)
            rows = connection.execute(
                """
                SELECT event, status, step, detail, created_at
                FROM execution_events WHERE task_id = ? ORDER BY event_id
                """,
                (task_id,),
            ).fetchall()
            return [dict(row) for row in rows]

    def export_history(self, task_id: str) -> Path:
        with self._history_export_lock:
            with self._connection() as connection:
                connection.execute("BEGIN")
                execution = self._decode(self._require(connection, task_id))
                event_rows = connection.execute(
                    """
                    SELECT event, status, step, detail, created_at
                    FROM execution_events WHERE task_id = ? ORDER BY event_id
                    """,
                    (task_id,),
                ).fetchall()
                record = {
                    "execution": execution,
                    "events": [dict(row) for row in event_rows],
                }
            destination = self.history_dir / f"{task_id}.json"
            temporary_path: str | None = None
            try:
                with tempfile.NamedTemporaryFile(
                    mode="w",
                    encoding="utf-8",
                    dir=self.history_dir,
                    prefix=f".{task_id}.",
                    suffix=".tmp",
                    delete=False,
                ) as temporary_file:
                    temporary_path = temporary_file.name
                    json.dump(record, temporary_file, indent=2, ensure_ascii=False)
                    temporary_file.write("\n")
                    temporary_file.flush()
                    os.fsync(temporary_file.fileno())
                os.replace(temporary_path, destination)
            except OSError:
                if temporary_path is not None:
                    try:
                        os.unlink(temporary_path)
                    except OSError:
                        pass
                raise
        return destination

    def export_all_histories(self) -> None:
        with self._connection() as connection:
            task_ids = [
                row["task_id"]
                for row in connection.execute(
                    "SELECT task_id FROM executions"
                ).fetchall()
            ]
        for task_id in task_ids:
            self.export_history(task_id)

    def recover_interrupted(self, first_step: str) -> list[str]:
        """Requeue interrupted work; completed checkpoints are retained."""
        recovered: list[str] = []
        updated: list[str] = []
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            rows = connection.execute(
                "SELECT * FROM executions WHERE status IN (?, ?)",
                (ExecutionStatus.QUEUED, ExecutionStatus.RUNNING),
            ).fetchall()
            for row in rows:
                execution = self._decode(row)
                checkpoints = execution["checkpoints"]
                for step, checkpoint in checkpoints.items():
                    if checkpoint["status"] == "running":
                        checkpoints[step] = {
                            "status": "pending",
                            "idempotency_key": checkpoint["idempotency_key"],
                        }
                next_step = next(
                    (
                        step
                        for step in ("plan", "research", "respond")
                        if checkpoints.get(step, {}).get("status") != "completed"
                    ),
                    first_step,
                )
                if execution["cancel_requested"]:
                    status = ExecutionStatus.CANCELLED
                elif execution["pause_requested"]:
                    status = ExecutionStatus.WAITING
                else:
                    status = ExecutionStatus.QUEUED
                now = utc_now()
                connection.execute(
                    """
                    UPDATE executions
                    SET status = ?, current_step = ?, checkpoints = ?,
                        cancel_requested = 0, pause_requested = 0, updated_at = ?
                    WHERE task_id = ?
                    """,
                    (
                        status,
                        next_step,
                        json.dumps(checkpoints),
                        now,
                        execution["task_id"],
                    ),
                )
                self._event(
                    connection,
                    execution["task_id"],
                    "execution_recovered",
                    status,
                    next_step,
                    "Restart recovery retained completed checkpoints.",
                )
                if status == ExecutionStatus.CANCELLED:
                    self._event(
                        connection,
                        execution["task_id"],
                        "execution_cancelled",
                        status,
                        next_step,
                        "Cancellation was pending when the process stopped.",
                    )
                if status == ExecutionStatus.QUEUED:
                    recovered.append(execution["task_id"])
                updated.append(execution["task_id"])
        for task_id in updated:
            self.export_history(task_id)
        return recovered

    def set_step_running(
        self, task_id: str, step: str, idempotency_key: str
    ) -> dict[str, Any]:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = self._require(connection, task_id)
            execution = self._decode(row)
            if execution["cancel_requested"] or execution["pause_requested"]:
                return execution
            checkpoints = execution["checkpoints"]
            checkpoints[step] = {
                "status": "running",
                "idempotency_key": idempotency_key,
            }
            now = utc_now()
            connection.execute(
                """
                UPDATE executions SET status = ?, current_step = ?, checkpoints = ?,
                    updated_at = ? WHERE task_id = ?
                """,
                (
                    ExecutionStatus.RUNNING,
                    step,
                    json.dumps(checkpoints),
                    now,
                    task_id,
                ),
            )
            self._event(connection, task_id, "step_started", ExecutionStatus.RUNNING, step)
        self.export_history(task_id)
        return self.get(task_id)

    def complete_step(
        self, task_id: str, step: str, output: Any, next_step: str
    ) -> dict[str, Any]:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = self._require(connection, task_id)
            execution = self._decode(row)
            checkpoints = execution["checkpoints"]
            idempotency_key = checkpoints[step]["idempotency_key"]
            cancelled = execution["cancel_requested"]
            waiting = execution["pause_requested"] and not cancelled
            status = (
                ExecutionStatus.CANCELLED
                if cancelled
                else ExecutionStatus.WAITING if waiting else ExecutionStatus.RUNNING
            )
            if cancelled:
                checkpoints[step] = {
                    "status": "cancelled",
                    "idempotency_key": idempotency_key,
                }
            else:
                checkpoints[step] = {
                    "status": "completed",
                    "idempotency_key": idempotency_key,
                    "output": output,
                    "completed_at": utc_now(),
                }
            now = utc_now()
            connection.execute(
                """
                UPDATE executions
                SET status = ?, current_step = ?, checkpoints = ?,
                    cancel_requested = 0, pause_requested = 0, updated_at = ?
                WHERE task_id = ?
                """,
                (
                    status,
                    step if cancelled else next_step,
                    json.dumps(checkpoints),
                    now,
                    task_id,
                ),
            )
            if cancelled:
                self._event(
                    connection, task_id, "execution_cancelled", status, step
                )
            elif waiting:
                self._event(
                    connection,
                    task_id,
                    "step_checkpointed",
                    status,
                    step,
                    f"Completed step '{step}'.",
                )
                self._event(
                    connection, task_id, "execution_waiting", status, next_step
                )
            else:
                self._event(
                    connection,
                    task_id,
                    "step_checkpointed",
                    status,
                    step,
                    f"Completed step '{step}'.",
                )
        self.export_history(task_id)
        return self.get(task_id)

    def finish(self, task_id: str, status: ExecutionStatus) -> dict[str, Any]:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = self._require(connection, task_id)
            current = self._decode(row)
            if current["status"] in (
                ExecutionStatus.CANCELLED,
                ExecutionStatus.COMPLETED,
            ):
                return current
            now = utc_now()
            connection.execute(
                """
                UPDATE executions
                SET status = ?, cancel_requested = 0, pause_requested = 0, updated_at = ?
                WHERE task_id = ?
                """,
                (status, now, task_id),
            )
            self._event(connection, task_id, f"execution_{status.value}", status)
        self.export_history(task_id)
        return self.get(task_id)

    def fail(self, task_id: str, step: str, error: Exception) -> dict[str, Any]:
        message = f"{type(error).__name__}: {error}"
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = self._require(connection, task_id)
            execution = self._decode(row)
            if execution["cancel_requested"]:
                checkpoints = execution["checkpoints"]
                previous = checkpoints.get(step, {})
                checkpoints[step] = {
                    "status": "cancelled",
                    "idempotency_key": previous.get(
                        "idempotency_key", f"{task_id}:{step}"
                    ),
                }
                now = utc_now()
                connection.execute(
                    """
                    UPDATE executions
                    SET status = ?, cancel_requested = 0, pause_requested = 0,
                        checkpoints = ?, updated_at = ?
                    WHERE task_id = ?
                    """,
                    (
                        ExecutionStatus.CANCELLED,
                        json.dumps(checkpoints),
                        now,
                        task_id,
                    ),
                )
                self._event(
                    connection,
                    task_id,
                    "execution_cancelled",
                    ExecutionStatus.CANCELLED,
                    step,
                )
                cancelled = True
            else:
                cancelled = False
            if not cancelled:
                errors = execution["errors"]
                errors.append({"step": step, "message": message, "created_at": utc_now()})
                checkpoints = execution["checkpoints"]
                previous = checkpoints.get(step, {})
                checkpoints[step] = {
                    "status": "failed",
                    "idempotency_key": previous.get(
                        "idempotency_key", f"{task_id}:{step}"
                    ),
                    "error": message,
                }
                now = utc_now()
                connection.execute(
                    """
                    UPDATE executions
                    SET status = ?, errors = ?, checkpoints = ?, updated_at = ?
                    WHERE task_id = ?
                    """,
                    (
                        ExecutionStatus.FAILED,
                        json.dumps(errors),
                        json.dumps(checkpoints),
                        now,
                        task_id,
                    ),
                )
                self._event(
                    connection, task_id, "execution_failed", ExecutionStatus.FAILED,
                    step, message,
                )
        self.export_history(task_id)
        return self.get(task_id)

    def queue_resume(self, task_id: str, first_step: str) -> dict[str, Any]:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = self._require(connection, task_id)
            execution = self._decode(row)
            if execution["status"] in (
                ExecutionStatus.COMPLETED,
                ExecutionStatus.CANCELLED,
            ):
                raise ValueError(
                    f"An execution with status '{execution['status']}' cannot be resumed."
                )
            if execution["status"] == ExecutionStatus.RUNNING:
                raise ValueError("A running execution cannot be resumed.")
            checkpoints = execution["checkpoints"]
            for step, checkpoint in checkpoints.items():
                if checkpoint["status"] == "failed":
                    checkpoints[step] = {
                        "status": "pending",
                        "idempotency_key": checkpoint["idempotency_key"],
                    }
            next_step = next(
                (
                    step
                    for step in ("plan", "research", "respond")
                    if checkpoints.get(step, {}).get("status") != "completed"
                ),
                first_step,
            )
            now = utc_now()
            connection.execute(
                """
                UPDATE executions
                SET status = ?, current_step = ?, checkpoints = ?,
                    cancel_requested = 0, pause_requested = 0, updated_at = ?
                WHERE task_id = ?
                """,
                (
                    ExecutionStatus.QUEUED,
                    next_step,
                    json.dumps(checkpoints),
                    now,
                    task_id,
                ),
            )
            self._event(
                connection, task_id, "execution_resumed",
                ExecutionStatus.QUEUED, next_step,
            )
        self.export_history(task_id)
        return self.get(task_id)

    def request_pause(self, task_id: str) -> dict[str, Any]:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            execution = self._decode(self._require(connection, task_id))
            if execution["status"] in (
                ExecutionStatus.COMPLETED,
                ExecutionStatus.FAILED,
                ExecutionStatus.CANCELLED,
            ):
                raise ValueError(
                    f"An execution with status '{execution['status']}' cannot be paused."
                )
            if execution["status"] == ExecutionStatus.WAITING:
                return execution
            status = (
                ExecutionStatus.WAITING
                if execution["status"] == ExecutionStatus.QUEUED
                else ExecutionStatus.RUNNING
            )
            now = utc_now()
            connection.execute(
                """
                UPDATE executions SET status = ?, pause_requested = 1, updated_at = ?
                WHERE task_id = ?
                """,
                (status, now, task_id),
            )
            self._event(connection, task_id, "pause_requested", status, execution["current_step"])
        self.export_history(task_id)
        return self.get(task_id)

    def request_cancel(self, task_id: str) -> dict[str, Any]:
        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            execution = self._decode(self._require(connection, task_id))
            if execution["status"] in (
                ExecutionStatus.COMPLETED,
                ExecutionStatus.CANCELLED,
            ):
                raise ValueError(
                    f"An execution with status '{execution['status']}' cannot be cancelled."
                )
            status = (
                ExecutionStatus.CANCELLED
                if execution["status"] in (
                    ExecutionStatus.QUEUED,
                    ExecutionStatus.WAITING,
                    ExecutionStatus.FAILED,
                )
                else ExecutionStatus.RUNNING
            )
            cancel_requested = status != ExecutionStatus.CANCELLED
            now = utc_now()
            connection.execute(
                """
                UPDATE executions
                SET status = ?, cancel_requested = ?, updated_at = ?
                WHERE task_id = ?
                """,
                (status, int(cancel_requested), now, task_id),
            )
            self._event(
                connection, task_id, "cancel_requested", status, execution["current_step"]
            )
            if status == ExecutionStatus.CANCELLED:
                self._event(
                    connection, task_id, "execution_cancelled", status,
                    execution["current_step"],
                )
        self.export_history(task_id)
        return self.get(task_id)
