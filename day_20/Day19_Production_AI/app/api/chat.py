from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.conversation_service import chat

router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def create_chat(request: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    answer, sources = chat(db, request.conversation_id, request.message)
    return ChatResponse(conversation_id=request.conversation_id, answer=answer, sources=sources)
