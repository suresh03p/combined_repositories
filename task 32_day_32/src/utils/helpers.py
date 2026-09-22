from __future__ import annotations

import json
from pathlib import Path


def ensure_directory(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)


def write_json(path: str, payload: dict) -> None:
    ensure_directory(str(Path(path).parent))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def read_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
