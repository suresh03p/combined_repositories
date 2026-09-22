"""Recursive boundary-aware text splitting."""
from __future__ import annotations

import re


def recursive_chunks(text: str, size: int = 512, overlap: int = 50) -> list[str]:
    if size <= 0 or overlap >= size:
        raise ValueError("size must be positive and overlap smaller than size")
    parts = [part.strip() for part in re.split(r"\n\s*\n|(?<=[.!?])\s+", text) if part.strip()]
    chunks: list[str] = []
    current = ""
    for part in parts:
        candidate = f"{current} {part}".strip()
        if current and len(candidate) > size:
            chunks.append(current)
            tail = current[-overlap:] if overlap else ""
            current = f"{tail} {part}".strip()
        elif len(part) > size:
            if current:
                chunks.append(current)
                current = ""
            for start in range(0, len(part), size - overlap):
                piece = part[start:start + size].strip()
                if piece:
                    chunks.append(piece)
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks
