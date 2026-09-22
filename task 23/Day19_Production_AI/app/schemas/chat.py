from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    conversation_id: str = Field(min_length=1, max_length=80, pattern=r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
    message: str = Field(min_length=1, max_length=4000)

    @field_validator("message")
    @classmethod
    def message_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("message must not be blank")
        return value.strip()


class ChatResponse(BaseModel):
    conversation_id: str
    answer: str
    sources: list[str] = []
    status: str = "success"
