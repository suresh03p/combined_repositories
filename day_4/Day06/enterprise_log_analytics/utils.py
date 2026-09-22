"""Utility helpers for the analytics package."""

from __future__ import annotations

from pathlib import Path


def ensure_directory(path: Path) -> Path:
    """Ensure the target directory exists."""
    path.mkdir(parents=True, exist_ok=True)
    return path
