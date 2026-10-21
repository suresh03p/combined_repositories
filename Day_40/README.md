# Day 40: Durable Agent Runner

A runnable Python 3.10+ project demonstrating durable, restartable agent execution. It uses SQLite for persistent task state, checkpoints every agent/tool step, and resumes incomplete work after a process restart. The API and worker use only Python's standard library.

## Run

From this directory:

```powershell
python -m durable_agent_runner
```

The API listens on `http://127.0.0.1:8000`. State is saved to `outputs/executions.sqlite3`; each task's execution history is atomically written to `outputs/execution_history/<task_id>.json`.

Override the bind address or persistence paths:

```powershell
python -m durable_agent_runner --host 127.0.0.1 --port 8000 `
  --database outputs/executions.sqlite3 `
  --history-dir outputs/execution_history
```

## API

- `POST /executions` — queue a workflow. JSON: `{"input_text":"..."}`. An optional `Idempotency-Key` header (or `idempotency_key` body field) makes request retries return the original execution; reusing a key for different input returns `409`.
- `GET /executions` — list recent executions.
- `GET /executions/{task_id}` — read status, conversation ID, current step, checkpoints, and errors.
- `GET /executions/{task_id}/history` — read the execution-history JSON record.
- `POST /executions/{task_id}/pause` — pause at the next step boundary (`waiting`).
- `POST /executions/{task_id}/resume` — resume a waiting or failed execution without repeating completed checkpoints.
- `POST /executions/{task_id}/cancel` — cancel queued/waiting work or request cancellation at the next step boundary.
- `GET /health` — process health.

Execution states are `queued`, `running`, `waiting`, `completed`, `failed`, and `cancelled`.

## Durability and idempotency

SQLite is the source of truth. Each step is marked running before it is called, then its output and the next-step pointer are committed together as a checkpoint. At startup, queued or interrupted running executions are recovered and rescheduled; completed checkpoints are skipped. A step interrupted between starting and persisting its output is retried with the same `<task_id>:<step_name>` idempotency key.

The built-in workflow is a deterministic offline demo (`plan -> research -> respond`), not an LLM. Its role boundaries are:

| Checkpoint | Role | Input | Successful output / next recipient |
| --- | --- | --- | --- |
| `plan` | planner | Execution task ID, user goal, and step idempotency key | Goal and non-empty research questions -> researcher |
| `research` | researcher | Validated planner handoff | One or more claim/evidence findings and limitations -> validator |
| `respond` | validator | Validated researcher handoff | Accepted flag, answer, and issues -> terminal |

Each output is a strict JSON handoff envelope with schema version `1.0`, sender, recipient, execution task ID, status, and role-specific payload. Unknown fields, missing fields, wrong recipients, mismatched task IDs, and invalid payloads are rejected before checkpointing; the execution becomes `failed`, and later roles are not run. A structured `status: "error"` handoff also fails the current execution with its error code and message. The existing checkpoint names are retained for compatibility while role names describe the agent responsibilities.

Each step handler has a 30-second deadline and one retry by default. Configure these per runner with `step_timeout` (finite positive seconds) and `retry_budget` (non-negative number of retries). Retries reuse the same `<task_id>:<step_name>` idempotency key; external tools must honor that key to avoid duplicate side effects. Outputs are JSON-serializable and contract-validated before they can be checkpointed. Invalid output or exhausted retries moves the execution to `failed` without saving that step's output or running later roles. Cancellation is checked at step boundaries and wins atomically over a result that has not yet been checkpointed.

Python cannot forcibly stop a synchronous handler thread. A timed-out call's result is ignored, and its slot remains occupied until it returns; the bounded retry budget and handler slots limit abandoned calls. Cancelling an in-flight call requests cancellation at the runner boundary but cannot undo side effects already started by an external provider. Provider-side timeouts and idempotency are still required for hard cancellation and exactly-once external effects.

The JSON Schema documents are in `schemas/agent-handoff.schema.json` and `schemas/role-contracts.schema.json`. Runtime checks use explicit standard-library validation to keep this demo dependency-free. Execution states are `queued -> running`, may enter `waiting` on pause, and finish as `completed`, `failed`, or `cancelled`. Completed and cancelled executions cannot be resumed; failed executions may be explicitly resumed, which retries the failed step without repeating completed checkpoints.

When integrating external tools, pass the supplied step idempotency key through to the provider/tool and require that tool to deduplicate it. SQLite cannot make an arbitrary external side effect and a local database commit one atomic transaction; provider-side idempotency is necessary to close that crash window.

Run one service process against a database at a time. SQLite persists and recovers work across process restarts, but this demo does not implement multi-process worker claiming or distributed coordination.

The HTTP server is intended for local learning and does not include authentication or TLS. Put it behind an authenticated service boundary before exposing it to an untrusted network.

## Test

```powershell
python -m unittest discover -s tests -v
```

The handoff tests cover valid role routing, strict payload validation, wrong recipients/task IDs, unexpected fields, structured error handoffs, and runner behavior when a malformed handoff is returned.
