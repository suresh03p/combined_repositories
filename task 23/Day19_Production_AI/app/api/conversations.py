from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.conversation import ConversationResponse, MessageResponse
from app.services.conversation_service import history

router = APIRouter(prefix="/api/v1", tags=["conversations"])


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(conversation_id: str, db: Session = Depends(get_db)) -> ConversationResponse:
    messages = history(db, conversation_id)
    return ConversationResponse(
        conversation_id=conversation_id,
        messages=[MessageResponse(role=item.role, content=item.content) for item in messages],
    )
