from pydantic import BaseModel, Field, ValidationError
import re

class AIResponse(BaseModel):
    answer: str = Field(min_length=1, max_length=10000)
    sources: list[str] = []
    confidence: float = Field(ge=0, le=1)

def validate_ai_output(value: dict) -> AIResponse:
    result = AIResponse.model_validate(value)
    if re.search(r"FAKE_API_KEY|FAKE_PASSWORD|BEGIN PRIVATE", result.answer, re.IGNORECASE):
        raise ValueError("Sensitive information detected in output")
    return result
