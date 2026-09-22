from collections import defaultdict, deque
from time import monotonic
from fastapi import HTTPException

_requests: dict[str, deque[float]] = defaultdict(deque)

def check_rate_limit(key: str, limit: int = 10, window_seconds: int = 60) -> None:
    now = monotonic()
    timestamps = _requests[key]
    while timestamps and now - timestamps[0] >= window_seconds:
        timestamps.popleft()
    if len(timestamps) >= limit:
        raise HTTPException(429, "AI request rate limit exceeded")
    timestamps.append(now)

def reset_rate_limits() -> None:
    _requests.clear()
