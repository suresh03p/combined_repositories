"""Page, section, and paragraph-aware chunking."""

import re

from .document_cleaner import clean_text
from .document_metadata import make_metadata


def chunk_documents(pages: list[dict], chunk_words: int = 120) -> list[dict]:
    chunks = []
    for page in pages:
        text = clean_text(page.get("text", ""))
        section = "General"
        section_number = 0
        words = []
        for paragraph in re.split(r"\n\s*\n", text):
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            if len(paragraph.split()) <= 10 and paragraph.endswith((":", "Policy")):
                section = paragraph.rstrip(":")
                words.extend(section.split())
                continue
            words.extend(paragraph.split())
            while len(words) >= chunk_words:
                section_number += 1
                body, words = words[:chunk_words], words[chunk_words:]
                chunk_id = f"{page['document_id']}-P{page.get('page', 1):02d}-C{section_number:02d}"
                metadata = make_metadata(page["document_id"], page["source"], page["file_type"],
                                         page.get("page", 1), page["source"], "HR", chunk_id)
                metadata["section"] = section
                chunks.append({"chunk_id": chunk_id, "text": " ".join(body), "metadata": metadata})
        if words:
            section_number += 1
            chunk_id = f"{page['document_id']}-P{page.get('page', 1):02d}-C{section_number:02d}"
            metadata = make_metadata(page["document_id"], page["source"], page["file_type"],
                                     page.get("page", 1), page["source"], "HR", chunk_id)
            metadata["section"] = section
            chunks.append({"chunk_id": chunk_id, "text": " ".join(words), "metadata": metadata})
    return chunks