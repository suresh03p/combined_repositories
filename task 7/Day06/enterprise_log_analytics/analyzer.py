"""Analytics utilities for summary and reporting."""

from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime
from typing import Any


class LogAnalyzer:
    """Aggregate log data into reports."""

    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []

    def ingest(self, records: list[dict[str, Any]]) -> None:
        self.records.extend(records)

    def hourly_summary(self) -> Counter[str]:
        counts: Counter[str] = Counter()
        for record in self.records:
            timestamp = record.get("timestamp", "")
            try:
                hour = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime("%H:00")
            except ValueError:
                continue
            counts[hour] += 1
        return counts

    def daily_summary(self) -> Counter[str]:
        counts: Counter[str] = Counter()
        for record in self.records:
            timestamp = record.get("timestamp", "")
            try:
                day = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime("%Y-%m-%d")
            except ValueError:
                continue
            counts[day] += 1
        return counts

    def top_errors(self) -> Counter[str]:
        counts: Counter[str] = Counter()
        for record in self.records:
            error_code = str(record.get("error_code", ""))
            if error_code:
                counts[error_code] += 1
        return counts

    def user_activity(self) -> defaultdict[str, int]:
        counts: defaultdict[str, int] = defaultdict(int)
        for record in self.records:
            user_id = str(record.get("user_id", "unknown"))
            counts[user_id] += 1
        return counts
