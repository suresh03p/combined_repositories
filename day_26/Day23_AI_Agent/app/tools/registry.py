import re

from app.tools.calculator import calculate
from app.tools.date_tool import current_date
from app.tools.document_search import search_documents
from app.tools.errors import UnknownToolError
from app.tools.schemas import Tool


class ToolRegistry:
    def __init__(self, tools: list[Tool]) -> None:
        self._tools = {tool.name: tool for tool in tools}

    @classmethod
    def default(cls) -> "ToolRegistry":
        return cls([
            Tool("calculator", "Evaluate arithmetic", calculate),
            Tool("date", "Return the current UTC date", current_date),
            Tool("document_search", "Search indexed documents", search_documents),
        ])

    def run(self, name: str, message: str) -> str:
        try:
            tool = self._tools[name]
        except KeyError as error:
            raise UnknownToolError(f"Unknown tool: {name}") from error
        argument = message
        if name == "calculator":
            match = re.search(r"[0-9][0-9().+*/ -]*", message)
            argument = match.group(0) if match else message
        return tool.handler(argument.strip())
