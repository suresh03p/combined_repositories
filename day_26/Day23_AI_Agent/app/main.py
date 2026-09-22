from fastapi import FastAPI

from app.api.agent import router

app = FastAPI(title="Day 23 AI Agent", version="1.0.0")
app.include_router(router, prefix="/api")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
