import os
import time
import uuid
from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator


app = FastAPI(title="Inference API", version=os.getenv("MODEL_VERSION", "customer-support-v1.0"))


class InferenceRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("text cannot be empty")
        return cleaned


class InferenceResponse(BaseModel):
    request_id: str
    model_version: str
    prediction: str
    status: Literal["success", "error"] = "success"


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "inference-api"}


@app.get("/ready")
def readiness_check():
    return {"status": "ready", "service": "inference-api"}


@app.post("/inference", response_model=InferenceResponse)
def infer(request: InferenceRequest):
    request_id = str(uuid.uuid4())
    start = time.time()

    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    if len(request.text) > 2000:
        raise HTTPException(status_code=413, detail="Input exceeds maximum allowed length.")

    try:
        prediction = "account_login_issue" if "log into" in request.text.lower() or "login" in request.text.lower() else "general_support"
        duration = time.time() - start
        return {
            "request_id": request_id,
            "model_version": os.getenv("MODEL_VERSION", "customer-support-v1.0"),
            "prediction": prediction,
            "status": "success",
        }
    except Exception:
        raise HTTPException(status_code=500, detail="Inference failed. Please try again later.")
