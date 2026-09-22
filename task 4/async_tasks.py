import asyncio
from typing import Any, Dict, List, Optional, Sequence, Tuple

from api_client import APIClient
from logger import setup_logger


async def collect_data(urls: Sequence[str], timeout: int, max_retries: int, retry_delay: float) -> List[Dict[str, Any]]:
    logger = setup_logger()
    client = APIClient(timeout=timeout, max_retries=max_retries, retry_delay=retry_delay)
    tasks = [fetch_single_resource(client, url, logger) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    payloads: List[Any] = []
    for result in results:
        if isinstance(result, tuple):
            payload, elapsed, success = result
            if success:
                payloads.append(payload)
            else:
                logger.warning("Request failed for one of the endpoints")
        else:
            logger.exception("Unexpected exception while collecting data: %s", result)
    return payloads


async def fetch_single_resource(client: APIClient, url: str, logger: Any) -> Tuple[Any, float, bool]:
    payload, elapsed, success = await client.fetch_json(url)
    if success:
        logger.info("Fetched %s in %.3f seconds", url, elapsed)
    else:
        logger.error("Failed to fetch %s", url)
    return payload, elapsed, success
