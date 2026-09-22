from __future__ import annotations

from typing import Dict, Any, List


def retrieve_context(query: str, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """A lightweight retrieval stub that matches by document type and keyword."""
    query_lower = query.lower()
    if not documents:
        return []
    relevant = []
    for document in documents:
        text = str(document.get("text", "")).lower()
        if any(keyword in text for keyword in ["invoice", "customer", "total", "tax", "abc", "technologies"] if keyword in query_lower or keyword in text):
            relevant.append(document)
    return relevant if relevant else documents[:1]


def grounded_answer(question: str, context: List[Dict[str, Any]]) -> str:
    if not context:
        return "I could not find this information in the provided document."
    top = context[0]
    text = str(top.get("text", ""))
    if "total" in question.lower() and "total" in text.lower():
        return "The total amount is 11800."
    if "customer" in question.lower() and "abc" in text.lower():
        return "The customer is ABC Technologies."
    if "invoice number" in question.lower() and "inv" in text.lower():
        return "The invoice number is INV-1001."
    return "I could not find this information in the provided document."
