"""Character-window chunking with explicit overlap."""
from __future__ import annotations


def fixed_chunks(text: str, size: int = 512, overlap: int = 50) -> list[str]:
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("size must be positive and overlap must be smaller than size")
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start:start + size].strip()
        if chunk:
            chunks.append(chunk)
        if start + size >= len(text):
            break
        start += size - overlap
    return chunks


def compare_settings(text: str) -> list[dict]:
    return [{"chunk_size": size, "overlap": overlap, "number_of_chunks": len(fixed_chunks(text, size, overlap))}
            for size, overlap in ((256, 0), (256, 50), (512, 50), (1024, 100))]
