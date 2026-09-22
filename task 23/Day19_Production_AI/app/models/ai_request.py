from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class AIRequest(Base):
    __tablename__ = "ai_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    conversation_id: Mapped[str] = mapped_column(ForeignKey("conversations.id"))
    model: Mapped[str] = mapped_column(String(100), default="mock-gpt")
    status: Mapped[str] = mapped_column(String(30))
    input_tokens: Mapped[int] = mapped_column(Integer, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, default=0)
    retrieval_time: Mapped[float] = mapped_column(Float, default=0)
    llm_time: Mapped[float] = mapped_column(Float, default=0)
    latency: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    conversation = relationship("Conversation", back_populates="ai_requests")
