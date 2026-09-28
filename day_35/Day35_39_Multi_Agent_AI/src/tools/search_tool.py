import json
from pathlib import Path
from typing import Any

from src.tools.text import keywords


class SearchTool:
    """Search the bundled, offline research-source sample."""

    def __init__(self, source_path: Path | None = None) -> None:
        project_root = Path(__file__).resolve().parents[2]
        self.source_path = source_path or project_root / "data" / "research_sources.json"

    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        documents = json.loads(self.source_path.read_text(encoding="utf-8"))
        query_terms = keywords(query)
        scored = []
        for document in documents:
            document_terms = keywords(f"{document['title']} {document['content']}")
            score = len(query_terms & document_terms)
            if score:
                scored.append((score, document))
        scored.sort(key=lambda item: (-item[0], item[1]["id"]))
        return [
            {**document, "score": score}
            for score, document in scored[:limit]
        ]
