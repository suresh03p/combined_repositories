"""Parsers for TXT, CSV, and JSON log files."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


class LogParser:
    """Parse different log formats into a common record structure."""

    def __init__(self, log_dir: Path) -> None:
        self.log_dir = log_dir

    def parse(self, file_path: Path) -> list[dict[str, Any]]:
        suffix = file_path.suffix.lower()
        if suffix == ".txt":
            return self._parse_txt(file_path)
        if suffix == ".csv":
            return self._parse_csv(file_path)
        if suffix == ".json":
            return self._parse_json(file_path)
        raise ValueError(f"Unsupported format: {file_path}")

    def _parse_txt(self, file_path: Path) -> list[dict[str, Any]]:
        records = []
        for line in file_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            timestamp, level, message = line.split(" | ", 2)
            records.append({"timestamp": timestamp, "level": level, "message": message})
        return records

    def _parse_csv(self, file_path: Path) -> list[dict[str, Any]]:
        with file_path.open("r", encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def _parse_json(self, file_path: Path) -> list[dict[str, Any]]:
        with file_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        if isinstance(payload, list):
            return payload
        return [payload]
