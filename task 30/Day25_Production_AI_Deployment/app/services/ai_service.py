import asyncio


class AIService:
    def __init__(self, api_key: str, timeout: float):
        self.api_key = api_key
        self.timeout = timeout

    async def answer(self, prompt: str) -> str:
        await asyncio.sleep(0)
        if not self.api_key:
            return f"Local AI fallback: {prompt}"
        return f"Configured LLM placeholder response for: {prompt}"
