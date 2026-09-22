import logging

from redis.asyncio import Redis

logger = logging.getLogger(__name__)


class RedisService:
    def __init__(self, url: str):
        self.url = url
        self.client: Redis | None = Redis.from_url(url) if url else None

    async def ping(self) -> bool:
        if not self.client:
            return True
        try:
            return bool(await self.client.ping())
        except Exception:
            logger.exception("Redis health check failed")
            return False

    async def close(self) -> None:
        if self.client:
            await self.client.aclose()
