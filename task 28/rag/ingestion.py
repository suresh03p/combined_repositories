"""Extract page-level records from PDFs (and text files for the offline demo)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable


def extract_document(path: str | Path) -> list[dict]:
    path = Path(path)
    if path.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("Install pypdf to read PDF files") from exc
        return [{"document": path.name, "page": i, "text": page.extract_text() or ""}
                for i, page in enumerate(PdfReader(str(path)).pages, start=1)]
    text = path.read_text(encoding="utf-8")
    return [{"document": path.name, "page": 1, "text": text}]


def ingest_directory(directory: str | Path) -> list[dict]:
    root = Path(directory)
    records: list[dict] = []
    for path in sorted(root.iterdir()):
        if path.suffix.lower() in {".pdf", ".txt", ".md"}:
            records.extend(extract_document(path))
    return records


def save_jsonl(records: Iterable[dict], output: str | Path) -> None:
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="documents")
    parser.add_argument("--output", default="data/pages.jsonl")
    args = parser.parse_args()
    pages = ingest_directory(args.input_dir)
    save_jsonl(pages, args.output)
    print(f"Extracted {len(pages)} pages")
