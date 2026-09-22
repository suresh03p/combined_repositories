# Day 23 AI Agent

A small FastAPI agent with explicit planning, tool execution, limits, in-memory conversation memory, and structured logging.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then send `POST /api/agent` with JSON such as `{"message":"What is 2 + 3?"}`.
