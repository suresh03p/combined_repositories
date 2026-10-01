# Parallel Multi-Agent Research Engine

A small Python 3.11+ project demonstrating concurrent agent execution, result aggregation, validation, conflict detection, retry/fallback, and JSON tracing. It uses only the Python standard library. Demo values and citations are synthetic fixtures, not real research.

## Sequential and parallel execution

Sequential execution waits for each independent task before starting the next:

```text
Agent A -> Agent B -> Agent C -> aggregate
```

Parallel execution lets a supervisor launch independent work together, then aggregates after every task has completed:

```text
                 +-> Research (tasks 1, 2, 3) --+
Supervisor ------+-> RAG ------------------------+--> Aggregator --> Validator
                 +-> Document ------------------+
                 +-> Analytics -----------------+
```

Sequential execution is appropriate when later tasks depend on earlier outputs. This demo's research, retrieval, document, and analytics tasks are independent, so `asyncio.gather()` schedules them concurrently. `async` declares coroutine functions; `await` yields while an operation is pending; `asyncio.wait_for()` enforces per-attempt timeouts; exceptions are caught per agent so one failure does not cancel sibling work.

## Run

From the project root:

```powershell
python main.py
python -m unittest discover -s tests -v
```

The demo deliberately reports revenue as `20` from Research Agent 1 and `25` from RAG. The aggregator keeps both attributed values and emits `CONFLICT DETECTED`; the validator marks the aggregate as requiring review. It does not choose a winner.

## Project map

- `src/agents/demo_agents.py`: Research Agents 1-3, RAG, Document, and Analytics workers.
- `src/orchestration/supervisor.py`: concurrent execution, retries, timeout, fallback, controlled failure, and tracing.
- `src/orchestration/aggregator.py`: unified claims and contradiction detection.
- `src/agents/validator.py`: source, evidence, calculation, contradiction, and citation checks.
- `outputs/multi_agent_trace.json`: generated execution trace with agent, start/end, status, tool calls, result, and error.

The default policy allows one retry after the initial attempt, then invokes a configured fallback if available. Exhausted failures are recorded as failed results so the full run can still aggregate and validate the other agents.