# Multi-Agent Enterprise Research Pipeline

A dependency-free Python demo that routes a business question through research, retrieval, analysis, validation, and writing agents. The example corpus is local and intentionally small; replace the tool handlers in `src/tools/registry.py` to connect real search, document, or model services.

## Run

```powershell
C:/Users/Admin/AppData/Local/Python/pythoncore-3.14-64/python.exe -m src
C:/Users/Admin/AppData/Local/Python/pythoncore-3.14-64/python.exe -m unittest discover -s tests -v
```

Pass a different question as the first command-line argument. `Supervisor.run` also accepts a `failure_plan` mapping for deterministic failure simulation, for example:

```python
Supervisor().run("Compare retention trends", {"rag": ["timeout", "missing_context"]})
```

Supported simulated faults are `research_failure`, `rag_failure`, `timeout`, `invalid_response`, and `missing_context`. A list applies faults per attempt; after those entries are consumed, the agent runs normally. The supervisor retries once by default, skips unavailable research, delegates unavailable retrieval to the researcher, and stops when a required downstream stage cannot safely continue.

Each agent's shared-state reads and writes are explicitly restricted in `src/memory/shared_state.py`; state values are copied at the boundary so agents cannot mutate another agent's data by reference.