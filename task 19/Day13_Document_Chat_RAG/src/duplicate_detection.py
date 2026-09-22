"""Content fingerprints prevent duplicate ingestion."""

import hashlib
from pathlib import Path


def fingerprint(file_path: str | Path) -> str:
    return hashlib.sha256(Path(file_path).read_bytes()).hexdigest()


class DuplicateDetector:
    def __init__(self):
        self._hashes: dict[str, str] = {}

    def add(self, file_path: str | Path) -> bool:
        path = Path(file_path)
        digest = fingerprint(path)
        if digest in self._hashes:
            return False
        self._hashes[digest] = path.name
        return True

    def contains(self, file_path: str | Path) -> bool:
        return fingerprint(file_path) in self._hashes