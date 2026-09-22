import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Sequence


def ensure_directory(path: str) -> None:
    """Create a directory if it does not exist."""
    Path(path).mkdir(parents=True, exist_ok=True)


def deduplicate_records(records: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate records while preserving order."""
    seen = set()
    result: List[Dict[str, Any]] = []
    for record in records:
        key = json.dumps(record, sort_keys=True)
        if key not in seen:
            seen.add(key)
            result.append(record)
    return result


def validate_record(record: Dict[str, Any]) -> bool:
    """Validate that a record is a non-empty dictionary."""
    return isinstance(record, dict) and bool(record)


def write_json(path: str, payload: Any) -> None:
    """Write a JSON payload to disk."""
    ensure_directory(Path(path).parent.as_posix())
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def write_csv(path: str, rows: Sequence[Dict[str, Any]]) -> None:
    """Write records to a CSV file."""
    ensure_directory(Path(path).parent.as_posix())
    if not rows:
        return
    fieldnames = sorted({key for row in rows for key in row.keys()})
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
