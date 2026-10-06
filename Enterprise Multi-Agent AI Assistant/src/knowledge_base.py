"""Local Markdown and text knowledge-base search."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


_STOP_WORDS = {
    "a", "about", "an", "and", "are", "as", "at", "be", "by", "can", "did",
    "do", "for", "from", "how", "i", "in", "is", "it", "of", "on", "or",
    "our", "should", "the", "this", "to", "was", "we", "what", "when",
    "where", "which", "who", "why", "with", "would", "you",
}
_SUPPORTED_SUFFIXES = {".md", ".txt"}


def tokenize(text: str) -> set[str]:
    return {
        word
        for word in re.findall(r"[a-z0-9]+", text.casefold())
        if len(word) > 1 and word not in _STOP_WORDS
    }


@dataclass(frozen=True)
class Passage:
    source: str
    title: str
    section: str | None
    number: int
    text: str
    terms: frozenset[str]


class KnowledgeBase:
    """Search local Markdown and plain-text files with transparent term matching."""

    def __init__(self, directory: str | Path) -> None:
        self.directory = Path(directory).expanduser().resolve()
        if not self.directory.exists():
            raise FileNotFoundError(f"Knowledge directory does not exist: {self.directory}")
        if not self.directory.is_dir():
            raise NotADirectoryError(f"Knowledge path is not a directory: {self.directory}")
        self._passages = self._load_passages()

    def _load_passages(self) -> tuple[Passage, ...]:
        passages: list[Passage] = []
        files = sorted(
            (
                path
                for path in self.directory.rglob("*")
                if path.is_file() and path.suffix.casefold() in _SUPPORTED_SUFFIXES
            ),
            key=lambda path: path.relative_to(self.directory).as_posix().casefold(),
        )
        for path in files:
            relative_path = path.relative_to(self.directory).as_posix()
            content = path.read_text(encoding="utf-8")
            title = path.stem.replace("_", " ").replace("-", " ").strip().title()
            section: str | None = None
            number = 0
            for block in re.split(r"\n\s*\n", content):
                lines = block.strip().splitlines()
                if not lines:
                    continue
                heading = next(
                    (line.lstrip("#").strip() for line in lines if line.lstrip().startswith("#")),
                    None,
                )
                if heading:
                    section = heading
                    if number == 0 and len(lines) == 1:
                        title = heading
                        continue
                text = " ".join(line.strip() for line in lines if not line.lstrip().startswith("#"))
                terms = tokenize(text)
                if text and terms:
                    number += 1
                    passages.append(
                        Passage(
                            source=relative_path,
                            title=title,
                            section=section,
                            number=number,
                            text=text,
                            terms=frozenset(terms),
                        )
                    )
        return tuple(passages)

    def search(self, query: str, limit: int = 5) -> list[dict[str, object]]:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        query_terms = tokenize(query)
        if not query_terms:
            return []

        matches: list[tuple[int, Passage]] = []
        for passage in self._passages:
            score = len(query_terms.intersection(passage.terms))
            if score:
                matches.append((score, passage))
        matches.sort(key=lambda item: (-item[0], item[1].source.casefold(), item[1].number))
        results: list[dict[str, object]] = []
        for score, passage in matches[:limit]:
            results.append(
                {
                    "source": passage.source,
                    "title": passage.title,
                    "section": passage.section,
                    "passage": passage.number,
                    "text": passage.text,
                    "score": score,
                }
            )
        return results

    @property
    def source_count(self) -> int:
        return len({passage.source for passage in self._passages})

