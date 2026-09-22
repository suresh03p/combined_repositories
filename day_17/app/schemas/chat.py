from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    conversation_id: str = Field(min_length=1, max_length=100)
    question: str = Field(min_length=1, max_length=2000)

class Source(BaseModel):
    document: str
    page: int | None = None
    chunk_id: str

class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    cached: bool = False
