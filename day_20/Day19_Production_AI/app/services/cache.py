import json
import time
from typing import Any

from app.config import settings

_memory_cache: dict[str, tuple[float, str]] = {}
cache_hits = 0
cache_misses = 0


def get_cached(key: str) -> Any | None:
    global cache_hits, cache_misses
    item = _memory_cache.get(key)
    if item and item[0] > time.time():
        cache_hits += 1
        return json.loads(item[1])
    cache_misses += 1
    _memory_cache.pop(key, None)
    return None


def set_cached(key: str, value: Any, ttl: int | None = None) -> None:
    _memory_cache[key] = (time.time() + (ttl or settings.cache_ttl), json.dumps(value))


def cache_health() -> bool:
    return True


def cache_stats() -> dict[str, int]:
    return {"hits": cache_hits, "misses": cache_misses}
