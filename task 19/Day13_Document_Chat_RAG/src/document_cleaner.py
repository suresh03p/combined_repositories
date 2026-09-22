"""Normalize extracted document text before chunking."""

import re
from html import unescape


def clean_text(text: str, headers: list[str] | None = None, footers: list[str] | None = None) -> str:
    text = unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    removed = set(headers or []) | set(footers or [])
    lines = [line for line in lines if line and line not in removed]
    return "\n\n".join(lines)


def compare_text(original: str, headers: list[str] | None = None, footers: list[str] | None = None) -> dict[str, str]:
    return {"original_text": original, "cleaned_text": clean_text(original, headers, footers)}