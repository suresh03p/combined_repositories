import re
from typing import Any, Dict, Iterable, List


def normalize_text(value: str) -> str:
    if value is None:
        return ""
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def exact_match(expected: str, actual: str) -> bool:
    return normalize_text(expected) == normalize_text(actual)


def semantic_match(expected: str, actual: str) -> bool:
    expected_norm = normalize_text(expected)
    actual_norm = normalize_text(actual)
    if expected_norm == actual_norm:
        return True

    expected_terms = set(expected_norm.split())
    actual_terms = set(actual_norm.split())
    overlap = len(expected_terms.intersection(actual_terms))
    coverage = overlap / max(len(expected_terms), 1)
    return coverage >= 0.5 or expected_norm in actual_norm or actual_norm in expected_norm


def relevance_score(question: str, answer: str) -> float:
    question_tokens = set(normalize_text(question).split())
    answer_tokens = set(normalize_text(answer).split())
    if not question_tokens:
        return 0.0
    overlap = question_tokens.intersection(answer_tokens)
    return round(len(overlap) / len(question_tokens), 2)


def groundedness_score(context: str, answer: str) -> float:
    if not context or not answer:
        return 0.0
    context_tokens = set(normalize_text(context).split())
    answer_tokens = set(normalize_text(answer).split())
    overlap = context_tokens.intersection(answer_tokens)
    if not context_tokens:
        return 0.0
    return round(len(overlap) / len(context_tokens), 2)


def calculate_average(values: Iterable[float]) -> float:
    items = list(values)
    if not items:
        return 0.0
    return round(sum(items) / len(items), 4)


def score_response(question: str, expected: str, actual: str, context: str = "") -> Dict[str, Any]:
    return {
        "exact_match": exact_match(expected, actual),
        "semantic_match": semantic_match(expected, actual),
        "relevance": relevance_score(question, actual),
        "groundedness": groundedness_score(context, actual),
        "quality": calculate_average([
            1.0 if exact_match(expected, actual) else 0.0,
            1.0 if semantic_match(expected, actual) else 0.0,
            relevance_score(question, actual),
            groundedness_score(context, actual),
        ]),
    }


def evaluate_dataset(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    details = []
    for row in rows:
        result = score_response(
            question=row.get("question", ""),
            expected=row.get("expected_answer", ""),
            actual=row.get("actual_answer", ""),
            context=row.get("context", ""),
        )
        details.append({
            "id": row.get("id", "unknown"),
            "question": row.get("question", ""),
            "result": result,
        })

    scores = [item["result"]["quality"] for item in details]
    return {
        "total": len(details),
        "average_quality": calculate_average(scores),
        "results": details,
    }
