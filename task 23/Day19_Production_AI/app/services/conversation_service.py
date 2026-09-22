from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.message import Message
from app.services.ai_service import generate_answer


def chat(db: Session, conversation_id: str, user_message: str) -> tuple[str, list[str]]:
    conversation = db.get(Conversation, conversation_id)
    if conversation is None:
        conversation = Conversation(id=conversation_id, title=user_message[:200])
        db.add(conversation)
        db.flush()
    db.add(Message(conversation_id=conversation_id, role="user", content=user_message))
    answer, sources = generate_answer(db, conversation_id, user_message)
    db.add(Message(conversation_id=conversation_id, role="assistant", content=answer))
    db.commit()
    return answer, sources


def history(db: Session, conversation_id: str) -> list[Message]:
    return list(db.scalars(
        select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at, Message.id)
    ))
