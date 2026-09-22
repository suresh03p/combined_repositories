import asyncio
import time
from typing import Any, Dict, Optional, Tuple

import aiohttp


class APIClient:
    """Simple asynchronous client for fetching JSON responses."""

    def __init__(self, timeout: int, max_retries: int, retry_delay: float) -> None:
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    async def fetch_json(self, url: str) -> Tuple[Optional[Dict[str, Any]], float, bool]:
        for _ in range(self.max_retries):
            try:
                start = time.perf_counter()
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=self.timeout) as response:
                        response.raise_for_status()
                        payload = await response.json()
                elapsed = time.perf_counter() - start
                return payload, elapsed, True
            except Exception:  # pragma: no cover
                await asyncio.sleep(self.retry_delay)
        return None, 0.0, False
