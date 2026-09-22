"""Archive and restore log data."""

from __future__ import annotations

import zipfile
from pathlib import Path


class ArchiveManager:
    """Compress logs and backup reports."""

    def __init__(self, archive_dir: Path) -> None:
        self.archive_dir = archive_dir

    def compress_logs(self, files: list[Path]) -> Path:
        archive_path = self.archive_dir / "logs_archive.zip"
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in files:
                archive.write(path, arcname=path.name)
        return archive_path

    def restore(self, archive_path: Path, destination: Path) -> None:
        with zipfile.ZipFile(archive_path, "r") as archive:
            archive.extractall(destination)
