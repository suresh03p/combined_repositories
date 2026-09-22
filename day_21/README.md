# Day 20 Secure AI Assistant

A deliberately small FastAPI teaching project demonstrating layered AI application security.

## Run

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the API.

## Test

```powershell
pytest -q
```

The application uses an in-memory store for learning. Set `JWT_SECRET` in a real deployment; never use the development fallback in production.
