from fastapi import APIRouter, Depends, HTTPException
from app.auth.models import User
from app.auth.security import get_current_user
from app.main import CONVERSATIONS
router = APIRouter(prefix="/api/v1/conversations", tags=["conversations"])
@router.get("/{conversation_id}")
def get_conversation(conversation_id: str, user: User = Depends(get_current_user)):
    conversation = CONVERSATIONS.get(conversation_id)
    if not conversation or conversation["tenant_id"] != user.tenant_id or conversation["owner_id"] != user.id:
        raise HTTPException(404, "Conversation not found")
    return conversation
