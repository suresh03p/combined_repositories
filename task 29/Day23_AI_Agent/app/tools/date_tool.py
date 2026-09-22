from datetime import datetime, timezone


def current_date(_: str) -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")
