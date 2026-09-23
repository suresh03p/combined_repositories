"""Extract pages while retaining layout-adjacent metadata."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pymupdf

from ingestion.document_loader import load_document


def _heading(text: str) -> str | None:
    first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
    if not first_line:
        return None
    return first_line if len(first_line) <= 120 else None


def _tables(path: str, page_number: int) -> list[list[list[str]]]:
    try:
        import pdfplumber

        with pdfplumber.open(path) as pdf:
            tables = pdf.pages[page_number - 1].extract_tables()
            return tables or []
    except Exception:
        return []


def parse_page(path: str | Path, page_number: int) -> dict[str, Any]:
    """Parse one 1-based page and preserve its original number."""
    document = load_document(path)
    if page_number < 1 or page_number > document["page_count"]:
        raise IndexError(f"Page {page_number} is outside 1..{document['page_count']}")
    with pymupdf.open(document["path"]) as pdf:
        page = pdf[page_number - 1]
        text = page.get_text("text").strip()
        blocks = []
        for block in page.get_text("blocks"):
            block_text = block[4].strip()
            if block_text:
                blocks.append({"text": block_text, "position": list(block[:4])})
        images = [{"width": image[2], "height": image[3]} for image in page.get_images(full=True)]
    return {
        "document_id": document["document_id"],
        "page_number": page_number,
        "text": text,
        "images": images,
        "tables": _tables(document["path"], page_number),
        "section": _heading(text),
        "heading": _heading(text),
        "paragraphs": blocks,
    }


def parse_document(path: str | Path) -> list[dict[str, Any]]:
    """Parse every page in source order."""
    document = load_document(path)
    return [parse_page(path, page_number) for page_number in range(1, document["page_count"] + 1)]


def write_pages(path: str | Path, output_dir: str | Path = "data/processed/pages") -> list[Path]:
    """Write one JSON file per page for downstream chunking and retrieval."""
    import json

    pages = parse_document(path)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    written = []
    for page in pages:
        output = destination / f"{page['document_id']}_page_{page['page_number']:04d}.json"
        output.write_text(json.dumps(page, indent=2), encoding="utf-8")
        written.append(output)
    return written