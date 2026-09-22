"""Unified loader for PDF, HTML, and TXT files."""

from pathlib import Path
from .html_loader import load_html
from .pdf_loader import load_pdf


def load_document(file_path: str | Path) -> list[dict]:
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return load_pdf(path)
    if suffix in {".html", ".htm"}:
        return load_html(path)
    if suffix == ".txt":
        return [{"document_id": path.stem, "source": path.name, "page": 1,
                 "text": path.read_text(encoding="utf-8"), "file_type": "txt"}]
    raise ValueError("Unsupported file type.")


def load_documents(directory: str | Path) -> list[dict]:
    records = []
    for path in sorted(Path(directory).iterdir()):
        if path.is_file() and path.suffix.lower() in {".pdf", ".html", ".htm", ".txt"}:
            records.extend(load_document(path))
    return records