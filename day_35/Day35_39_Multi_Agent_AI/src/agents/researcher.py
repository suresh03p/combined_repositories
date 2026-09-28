from typing import Any

from src.tools.search_tool import SearchTool


class ResearchAgent:
    """Find candidate evidence in the configured research source."""

    def __init__(self, search_tool: SearchTool | None = None) -> None:
        self.search_tool = search_tool or SearchTool()

    def run(self, question: str) -> list[dict[str, Any]]:
        return self.search_tool.search(question)
