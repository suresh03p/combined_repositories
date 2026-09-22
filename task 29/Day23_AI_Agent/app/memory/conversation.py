from dataclasses import dataclass

from app.memory.storage import InMemoryStorage


@dataclass(frozen=True)
class Message:
    role: str
    content: str


class ConversationMemory:
    def __init__(self) -> None:
        self.storage = InMemoryStorage[list[Message]]()

    def add(self, conversation_id: str, role: str, content: str) -> None:
        messages = self.storage.get(conversation_id) or []
        self.storage.set(conversation_id, [*messages, Message(role, content)])

    def get(self, conversation_id: str) -> list[Message]:
        return self.storage.get(conversation_id) or []
