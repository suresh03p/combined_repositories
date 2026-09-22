"""Security monitoring for suspicious access patterns."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any


class SecurityMonitor:
    """Detect suspicious activity in log records."""

    def __init__(self) -> None:
        self.failed_logins: Counter[str] = Counter()
        self.ip_attempts: defaultdict[str, int] = defaultdict(int)

    def detect(self, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        incidents = []
        for record in records:
            event_type = str(record.get("event_type", ""))
            user_id = str(record.get("user_id", ""))
            ip_address = str(record.get("ip", ""))
            if event_type == "login_failed":
                self.failed_logins[user_id] += 1
                self.ip_attempts[ip_address] += 1
            if self.failed_logins[user_id] >= 3:
                incidents.append({"type": "brute_force", "user_id": user_id})
            if self.ip_attempts[ip_address] >= 5:
                incidents.append({"type": "suspicious_ip", "ip": ip_address})
            if record.get("token") == "invalid":
                incidents.append({"type": "invalid_token", "user_id": user_id})
            if record.get("status") == "401":
                incidents.append({"type": "unauthorized_access", "user_id": user_id})
        return incidents
