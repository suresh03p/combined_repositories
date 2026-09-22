"""Conversation history kept separate from document retrieval."""

from datetime import datetime, timezone


class ConversationMemory:
    def __init__(self):
        self._conversations: dict[str, list[dict]] = {}

    def add(self, conversation_id: str, role: str, content: str) -> dict:
        message = {"role": role, "content": content,
                   "timestamp": datetime.now(timezone.utc).isoformat()}
        self._conversations.setdefault(conversation_id, []).append(message)
        return message

    def get(self, conversation_id: str) -> list[dict]:
        return list(self._conversations.get(conversation_id, []))