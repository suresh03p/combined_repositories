"""Conservative text normalization for extracted documents."""
from __future__ import annotations

import re


def clean_text(text: str, headers: tuple[str, ...] = (), footers: tuple[str, ...] = ()) -> str:
    lines = []
    for raw in text.replace("\r\n", "\n").splitlines():
        line = re.sub(r"\s+", " ", raw).strip()
        if not line or line in headers or line in footers:
            continue
        lines.append(line)
    cleaned = " ".join(lines)
    # Join common PDF line-break hyphenation, but retain meaningful hyphens.
    cleaned = re.sub(r"(?<=\w)-\s+(?=\w)", "", cleaned)
    return re.sub(r" {2,}", " ", cleaned).strip()


def clean_pages(pages: list[dict], headers: tuple[str, ...] = (), footers: tuple[str, ...] = ()) -> list[dict]:
    return [{**page, "text": clean_text(page["text"], headers, footers)} for page in pages]


if __name__ == "__main__":
    print(clean_text("Employee\nLeave   Policy\n\nPage 4"))
