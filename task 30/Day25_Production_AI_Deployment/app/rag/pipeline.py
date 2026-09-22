from app.services.ai_service import AIService


class RagPipeline:
    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    async def query(self, question: str, documents: list[str]) -> str:
        context = "\n".join(documents[:20])
        prompt = f"Context:\n{context}\n\nQuestion: {question}" if context else question
        return await self.ai_service.answer(prompt)
