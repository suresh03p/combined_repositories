"""Serialization helpers for reports and records."""

from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any


class DataSerializer:
    """Persist data in JSON and pickle formats."""

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir

    def save_json(self, data: Any, path: Path) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def save_pickle(self, data: Any, path: Path) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        with path.open("wb") as handle:
            pickle.dump(data, handle)
