"""Validate documents and expose stable document-level metadata."""

from __future__ import annotations

import hashlib
import mimetypes
from datetime import datetime
from pathlib import Path
from typing import Any

from pypdf import PdfReader

SUPPORTED_TYPES = {".pdf"}


def validate_document(path: str | Path) -> Path:
    """Return a validated PDF path or raise a useful error."""
    document_path = Path(path)
    if not document_path.is_file():
        raise FileNotFoundError(f"Document does not exist: {document_path}")
    if document_path.suffix.lower() not in SUPPORTED_TYPES:
        raise ValueError(f"Unsupported document type: {document_path.suffix}")
    if document_path.stat().st_size == 0:
        raise ValueError(f"Document is empty: {document_path}")
    try:
        PdfReader(str(document_path))
    except Exception as exc:
        raise ValueError(f"Document is not a readable PDF: {document_path}") from exc
    return document_path


def _document_id(path: Path) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()[:12].upper()
    return f"DOC-{digest}"


def get_document_metadata(path: str | Path) -> dict[str, Any]:
    """Read metadata without discarding the source filename or page count."""
    document_path = validate_document(path)
    reader = PdfReader(str(document_path))
    stat = document_path.stat()
    pdf_metadata = reader.metadata or {}
    creation_date = pdf_metadata.get("/CreationDate")
    if creation_date is not None:
        creation_date = str(creation_date)
    return {
        "document_id": _document_id(document_path),
        "filename": document_path.name,
        "file_type": mimetypes.guess_type(document_path.name)[0] or "application/pdf",
        "file_size": stat.st_size,
        "page_count": len(reader.pages),
        "creation_metadata": creation_date,
        "source_metadata": {str(key): str(value) for key, value in pdf_metadata.items()},
        "ingested_at": datetime.now().astimezone().isoformat(),
    }


def load_document(path: str | Path) -> dict[str, Any]:
    """Load a document and return its identity plus page-level source handles."""
    document_path = validate_document(path)
    metadata = get_document_metadata(document_path)
    return {"path": str(document_path.resolve()), **metadata}