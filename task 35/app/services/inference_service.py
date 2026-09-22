import os
from typing import Dict, Any


class InferenceService:
    def __init__(self, model_version: str | None = None):
        self.model_version = model_version or os.getenv("MODEL_VERSION", "customer-support-v1.0")

    def predict(self, text: str) -> Dict[str, Any]:
        normalized = (text or "").strip()
        if not normalized:
            raise ValueError("Input text cannot be empty.")

        prediction = "account_login_issue" if "login" in normalized.lower() or "log into" in normalized.lower() else "general_support"
        return {
            "model_version": self.model_version,
            "prediction": prediction,
        }
