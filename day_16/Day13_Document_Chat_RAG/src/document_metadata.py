"""Metadata creation used for filtering and trustworthy citations."""

from datetime import date


def make_metadata(document_id: str, file_name: str, file_type: str, page_number: int,
                  source: str, category: str, chunk_id: str) -> dict:
    return {"document_id": document_id, "file_name": file_name, "file_type": file_type,
            "page_number": page_number, "source": source, "category": category,
            "uploaded_date": date.today().isoformat(), "chunk_id": chunk_id}