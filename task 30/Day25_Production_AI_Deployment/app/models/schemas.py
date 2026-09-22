from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=200)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10_000)


class ChatResponse(BaseModel):
    answer: str
    request_id: str


class RagRequest(BaseModel):
    question: str = Field(min_length=1, max_length=10_000)
    documents: list[str] = Field(default_factory=list, max_length=20)


class JobResponse(BaseModel):
    job_id: str
    status: str
    result: str | None = None
