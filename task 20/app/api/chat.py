from fastapi import APIRouter, Depends
from app.core.security import require_token
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import answer_question

router = APIRouter(tags=["chat"])

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, _: str = Depends(require_token)):
    return answer_question(request.question, request.conversation_id)

@router.get("/conversations/{conversation_id}")
def conversation(conversation_id: str, _: str = Depends(require_token)):
    return {"conversation_id": conversation_id, "messages": []}
