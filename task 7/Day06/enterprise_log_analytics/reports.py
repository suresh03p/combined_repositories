"""Generate report files for analytics output."""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


class ReportGenerator:
    """Write analytics reports to files."""

    def __init__(self, report_dir: Path) -> None:
        self.report_dir = report_dir

    def write_hourly_report(self, data: Counter[str]) -> Path:
        return self._write_report("hourly_report.txt", data)

    def write_daily_summary(self, data: Counter[str]) -> Path:
        return self._write_report("daily_summary.txt", data)

    def write_top_errors(self, data: Counter[str]) -> Path:
        return self._write_report("top_errors.txt", data)

    def write_user_activity(self, data: defaultdict[str, int]) -> Path:
        return self._write_report("user_activity.txt", data)

    def write_security_incidents(self, data: list[dict[str, Any]]) -> Path:
        self.report_dir.mkdir(parents=True, exist_ok=True)
        path = self.report_dir / "security_incidents.txt"
        path.write_text("\n".join(str(item) for item in data), encoding="utf-8")
        return path

    def _write_report(self, file_name: str, data: Any) -> Path:
        self.report_dir.mkdir(parents=True, exist_ok=True)
        path = self.report_dir / file_name
        path.write_text(str(dict(data)), encoding="utf-8")
        return path
