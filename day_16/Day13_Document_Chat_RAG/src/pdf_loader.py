"""PDF extraction with one unified record per page."""

from pathlib import Path


def load_pdf(file_path: str | Path) -> list[dict]:
    path = Path(file_path)
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("Install pypdf to load PDF documents.") from exc
    records = []
    for page_number, page in enumerate(PdfReader(str(path)).pages, start=1):
        records.append({"document_id": path.stem, "source": path.name, "page": page_number,
                        "text": page.extract_text() or "", "file_type": "pdf"})
    return records