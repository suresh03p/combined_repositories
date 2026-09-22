from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.auth.models import User
from app.auth.security import get_current_user
from app.core.logging import audit_event
from app.rag.pipeline import secure_retrieve
from app.security.prompt_injection import sanitize_user_prompt
from app.security.rate_limit import check_rate_limit
from app.security.output_validation import validate_ai_output
from app.main import CONVERSATIONS, DOCUMENTS

router = APIRouter(prefix="/api/v1", tags=["ai"])
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)

@router.post("/chat")
def chat(data: ChatRequest, user: User = Depends(get_current_user)):
    check_rate_limit(user.id)
    try:
        sanitize_user_prompt(data.message)
    except ValueError as exc:
        audit_event("/api/v1/chat", "blocked", user.id, user.tenant_id, "PROMPT_INJECTION")
        raise HTTPException(400, str(exc))
    matches = secure_retrieve(user, data.message, DOCUMENTS)
    response = validate_ai_output({"answer": f"Safe assistant response for: {data.message}", "sources": [d["document_id"] for d in matches], "confidence": 0.91})
    conversation_id = f"conv-{uuid4().hex[:8]}"
    CONVERSATIONS[conversation_id] = {"id": conversation_id, "tenant_id": user.tenant_id, "owner_id": user.id, "messages": [data.message]}
    audit_event("/api/v1/chat", "success", user.id, user.tenant_id)
    return {"conversation_id": conversation_id, **response.model_dump()}
