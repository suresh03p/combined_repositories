# Day 35-39: Multi-Agent AI

A small, runnable Day 35 project demonstrating a supervisor coordinating specialized agents through typed shared state. The workflow runs offline with Python's standard library and bundled sample documents.

## Architecture

**Single agent (Day 34):** `User -> Agent -> Planner -> Tools -> RAG -> Answer`. This is compact and works well for bounded requests. As tasks grow, one agent accumulates planning, retrieval, analysis, validation, and writing responsibilities. Its prompt and context grow, intermediate ownership becomes implicit, failures are harder to isolate, and independent work is difficult to parallelize. A multi-agent design can make these boundaries explicit, but adds handoff latency, orchestration complexity, duplicated work, and opportunities for disagreement or failure. More agents do not automatically improve correctness.

**Multi-agent (Day 35):** `User -> Supervisor -> Specialized Agent -> Result -> Supervisor -> ... -> Final Answer`. The supervisor owns routing and status; specialists own bounded tasks; shared state carries results; the supervisor receives each result before choosing the next action. Analysis, validation, and writing are separate stages so their outputs can be inspected.

In this runnable baseline, the exact sequence is `Supervisor -> Research -> Supervisor -> RAG -> Supervisor -> Analysis -> Supervisor -> Validation -> Supervisor -> Writer`. Search and retrieval use separate bundled JSON files and simple keyword overlap. They are deterministic teaching tools, not live web search, embedding-based retrieval, an LLM, or a claim of factual verification.

See [agent_roles.md](agent_roles.md) for each role's responsibilities.

## Project Layout

```text
src/agents/          Specialist and supervisor implementations
src/orchestration/   Shared workflow state
src/tools/           Offline search and text helpers
src/retrieval/       Local knowledge-base retrieval
src/memory/          Reserved for later memory lessons
src/api/             Runnable command-line entry point
data/                Bundled research and knowledge-base documents
tests/               Standard-library workflow tests
outputs/              Generated state JSON
```

## Run

From this directory, with Python 3.10 or newer:

```powershell
python -m src.api.main
```

Pass a question and choose an output path if desired:

```powershell
python -m src.api.main --question "How does shared state help agent communication?" --output outputs/multi_agent_state.json
```

The command prints every agent handoff and the final answer, then writes the shared state to `outputs/multi_agent_state.json`. State includes the conversation ID, request, current agent, task status, agent results, final response, and errors.

## Test

```powershell
python -m unittest discover -s tests -v
```

## Extension Points

Replace `SearchTool` with a real research provider and `LocalRetriever` with an embedding/vector retrieval implementation. Add provider credentials to the environment rather than committing secrets. For parallel agents, introduce explicit concurrency and conflict-resolution rules; the current sequential workflow deliberately keeps ownership and handoffs easy to follow. Add retry limits, timeouts, provenance checks, and stronger claim-level validation before using external tools or production data.
