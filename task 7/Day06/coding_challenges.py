"""Advanced coding challenges covering validation, parsing, serialization, and queueing."""

from __future__ import annotations

import json
import re
from collections import Counter, deque
from pathlib import Path
from typing import Any


class EmailValidator:
    """Validate email addresses from the challenge."""

    pattern = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.pattern.fullmatch(value.strip()))


class PasswordStrengthChecker:
    """Check password complexity."""

    @staticmethod
    def is_strong(password: str) -> bool:
        return bool(re.fullmatch(r"(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}", password))


class GSTNumberValidator:
    """Validate GST registrations."""

    pattern = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return bool(cls.pattern.fullmatch(value.strip().upper()))


class LogFileAnalyzer:
    """Analyze a simple log file."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def analyze(self) -> Counter[str]:
        counts = Counter()
        if not self.path.exists():
            return counts
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if "ERROR" in line:
                counts["ERROR"] += 1
            elif "WARN" in line:
                counts["WARN"] += 1
            else:
                counts["INFO"] += 1
        return counts


class BusinessDayCalculator:
    """Calculate business days between two dates."""

    @staticmethod
    def count(start: str, end: str) -> int:
        from datetime import date, timedelta

        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
        total = 0
        current = start_date
        while current <= end_date:
            if current.weekday() < 5:
                total += 1
            current += timedelta(days=1)
        return total


class WordFrequencyCounter:
    """Count word frequency in text."""

    @staticmethod
    def count(text: str) -> Counter[str]:
        return Counter(re.findall(r"\b\w+\b", text.lower()))


class EmployeeSerializer:
    """Serialize an employee record to JSON."""

    @staticmethod
    def serialize(employee: dict[str, Any], path: Path) -> None:
        path.write_text(json.dumps(employee, indent=2), encoding="utf-8")


class QueueSimulation:
    """Simple queue simulation using deque."""

    def __init__(self) -> None:
        self.queue: deque[str] = deque()

    def enqueue(self, item: str) -> None:
        self.queue.append(item)

    def dequeue(self) -> str | None:
        return self.queue.popleft() if self.queue else None


class SecurityLogParser:
    """Parse security log strings."""

    @staticmethod
    def parse(line: str) -> dict[str, str]:
        match = re.match(r"^(?P<timestamp>\S+) (?P<level>\S+) (?P<message>.+)$", line)
        return match.groupdict() if match else {}


class ArchiveManager:
    """Create an archive using zipfile."""

    @staticmethod
    def create_archive(files: list[Path], archive_path: Path) -> None:
        import zipfile

        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for file_path in files:
                archive.write(file_path, arcname=file_path.name)


def demo() -> dict[str, Any]:
    """Show sample outputs for the coding challenges."""
    return {
        "email": EmailValidator.is_valid("user@example.com"),
        "password": PasswordStrengthChecker.is_strong("Abc@1234"),
        "gst": GSTNumberValidator.is_valid("22AAAAA0000A1Z5"),
        "word_count": dict(WordFrequencyCounter.count("python python is great")),
        "business_days": BusinessDayCalculator.count("2026-08-01", "2026-08-07"),
    }


if __name__ == "__main__":
    print(demo())
