"""Tool registry and dependency-free demo tool implementations."""

from __future__ import annotations

import ast
import operator
import re
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    handler: Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def execute(self, name: str, **arguments: Any) -> Any:
        try:
            tool = self._tools[name]
        except KeyError as error:
            raise KeyError(f"Unknown tool: {name}") from error
        return tool.handler(**arguments)

    def names(self) -> tuple[str, ...]:
        return tuple(self._tools)


DEFAULT_DOCUMENTS: tuple[dict[str, Any], ...] = (
    {
        "id": "annual_report_2025",
        "title": "Annual Business Review 2025",
        "source": "Annual Business Review 2025",
        "text": (
            "FY2025 revenue grew 12 percent year over year. Customer churn "
            "fell from 8.0 percent in FY2024 to 6.5 percent in FY2025."
        ),
        "facts": [
            "FY2025 revenue grew 12% year over year.",
            "Customer churn fell from 8.0% in FY2024 to 6.5% in FY2025.",
        ],
        "metrics": [
            {"name": "revenue_growth", "period": "FY2025", "value": 12.0, "unit": "%"},
            {"name": "customer_churn", "period": "FY2024", "value": 8.0, "unit": "%"},
            {"name": "customer_churn", "period": "FY2025", "value": 6.5, "unit": "%"},
        ],
    },
    {
        "id": "customer_survey_2025",
        "title": "Customer Exit Survey 2025",
        "source": "Customer Exit Survey 2025",
        "text": (
            "Among customers who left in 2025, 72 percent cited onboarding "
            "friction and 34 percent cited support wait times."
        ),
        "facts": [
            "72% of surveyed customers who left cited onboarding friction.",
            "34% cited support wait times.",
        ],
        "metrics": [
            {"name": "churn_onboarding_friction", "period": "FY2025", "value": 72.0, "unit": "%"},
            {"name": "churn_support_wait", "period": "FY2025", "value": 34.0, "unit": "%"},
        ],
    },
    {
        "id": "onboarding_operations_2025",
        "title": "Onboarding Operations Report 2025",
        "source": "Onboarding Operations Report 2025",
        "text": (
            "Onboarding completion increased from 61 percent in FY2024 to "
            "74 percent in FY2025. Median time to value improved from 21 days "
            "to 15 days."
        ),
        "facts": [
            "Onboarding completion rose from 61% in FY2024 to 74% in FY2025.",
            "Median time to value fell from 21 days to 15 days.",
        ],
        "metrics": [
            {"name": "onboarding_completion", "period": "FY2024", "value": 61.0, "unit": "%"},
            {"name": "onboarding_completion", "period": "FY2025", "value": 74.0, "unit": "%"},
            {"name": "time_to_value", "period": "FY2024", "value": 21.0, "unit": "days"},
            {"name": "time_to_value", "period": "FY2025", "value": 15.0, "unit": "days"},
        ],
    },
)

_STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "did", "do", "for",
    "from", "how", "in", "is", "it", "of", "on", "or", "the", "to", "was",
    "what", "when", "were", "which", "with",
}


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in _STOP_WORDS and len(token) > 1
    }


def _search_documents(documents: tuple[dict[str, Any], ...], query: str) -> list[dict[str, Any]]:
    query_tokens = _tokens(query)
    ranked: list[tuple[int, dict[str, Any]]] = []
    for document in documents:
        document_tokens = _tokens(
            " ".join(
                [document["title"], document["text"], *document.get("facts", [])]
            )
        )
        score = len(query_tokens & document_tokens)
        if score:
            ranked.append((score, document))
    ranked.sort(key=lambda item: (-item[0], item[1]["id"]))
    return [{**document, "score": score} for score, document in ranked]


_BINARY_OPERATORS: dict[type[ast.operator], Callable[[float, float], float]] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}
_UNARY_OPERATORS: dict[type[ast.unaryop], Callable[[float], float]] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _calculate(expression: str) -> float:
    tree = ast.parse(expression, mode="eval")

    def evaluate(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in _BINARY_OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 8:
                raise ValueError("Exponent is too large")
            return float(_BINARY_OPERATORS[type(node.op)](left, right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _UNARY_OPERATORS:
            return float(_UNARY_OPERATORS[type(node.op)](evaluate(node.operand)))
        raise ValueError("Only basic arithmetic expressions are supported")

    return evaluate(tree)


def create_default_tool_registry(
    documents: tuple[dict[str, Any], ...] = DEFAULT_DOCUMENTS,
) -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(
        Tool(
            "RAG Search",
            "Retrieve document passages ranked against a query.",
            lambda query: _search_documents(documents, query),
        )
    )
    registry.register(
        Tool(
            "Calculator",
            "Evaluate a basic numeric arithmetic expression safely.",
            lambda expression: {"expression": expression, "result": _calculate(expression)},
        )
    )
    registry.register(
        Tool(
            "Document Search",
            "Find source documents relevant to a query.",
            lambda query: _search_documents(documents, query),
        )
    )
    registry.register(
        Tool(
            "Document Reader",
            "Read a document by its stable identifier.",
            lambda document_id: next(
                (dict(document) for document in documents if document["id"] == document_id),
                None,
            ),
        )
    )

    def validate(answer: str, citations: list[str], source_ids: list[str]) -> dict[str, Any]:
        issues: list[str] = []
        if not answer.strip():
            issues.append("The result is empty.")
        if not citations:
            issues.append("No citations were provided.")
        unknown = sorted(set(citations) - set(source_ids))
        if unknown:
            issues.append(f"Citations do not match retrieved sources: {', '.join(unknown)}")
        return {"is_valid": not issues, "issues": issues}

    registry.register(
        Tool("Validation Tool", "Check answer content and citation coverage.", validate)
    )
    return registry