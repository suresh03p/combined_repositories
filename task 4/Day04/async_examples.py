import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, Any
import urllib.request as urllib_request

try:
    import aiohttp
except ImportError:
    aiohttp = None


# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------------------------
# Fetch JSON Data from URL
# --------------------------------------------------
async def fetch(url: str, timeout: float = 3.0) -> Dict[str, Any]:
    try:
        if aiohttp is not None:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()

            return {
                "url": url,
                "status": "ok",
                "data": data
            }

        def sync_fetch():
            with urllib_request.urlopen(url, timeout=timeout) as response:
                return json.load(response)

        data = await asyncio.to_thread(sync_fetch)

        return {
            "url": url,
            "status": "ok",
            "data": data
        }

    except Exception as e:
        logger.warning("Fetch failed: %s", e)

        return {
            "url": url,
            "status": "error",
            "error": str(e)
        }


# --------------------------------------------------
# Read File Asynchronously
# --------------------------------------------------
async def read_file(path: str) -> Dict[str, Any]:
    try:
        content = await asyncio.to_thread(
            Path(path).read_text,
            encoding="utf-8"
        )

        return {
            "path": path,
            "status": "ok",
            "content": content
        }

    except Exception as e:
        logger.warning("Read failed: %s", e)

        return {
            "path": path,
          