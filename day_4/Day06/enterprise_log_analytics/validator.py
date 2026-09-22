"""Validation helpers for log records."""

from __future__ import annotations

import re
from typing import Any


class LogValidator:
    """Validate timestamps, IPs, URLs, IDs, and error codes."""

    TIMESTAMP_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})$")
    IP_PATTERN = re.compile(r"^(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}$")
    URL_PATTERN = re.compile(r"^https?://\S+$", re.IGNORECASE)
    USER_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{3,20}$")
    SESSION_ID_PATTERN = re.compile(r"^[A-Za-z0-9-]{4,30}$")
    ERROR_CODE_PATTERN = re.compile(r"^ERR[-_]?\d{3,5}$", re.IGNORECASE)

    def is_valid(self, record: dict[str, Any]) -> bool:
        timestamp = str(record.get("timestamp", ""))
        ip_address = str(record.get("ip", ""))
        url = str(record.get("url", ""))
        user_id = str(record.get("user_id", ""))
        session_id = str(record.get("session_id", ""))
        error_code = str(record.get("error_code", ""))

        return all([
            self.TIMESTAMP_PATTERN.match(timestamp) is not None,
            self.IP_PATTERN.match(ip_address) is not None,
            self.URL_PATTERN.match(url) is not None,
            self.USER_ID_PATTERN.match(user_id) is not None,
            self.SESSION_ID_PATTERN.match(session_id) is not None,
            self.ERROR_CODE_PATTERN.match(error_code) is not None or error_code == "",
        ])
