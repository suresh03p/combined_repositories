"""Metrics and a compact evaluation harness."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class EvaluationQuestion:
    query: str
    expected_document: str
    expected_page: int = 1


def hit(result: dict, item: EvaluationQuestion) -> bool:
    meta = result.get("metadata", {})
    return meta.get("document_name") == item.expected_document and meta.get("page_number") == item.expected_page


def evaluate(search_fn, questions: list[EvaluationQuestion], k: int = 5) -> dict:
    precisions = {n: 0 for n in (1, 3, 5)}
    recalls = {n: 0 for n in (1, 3, 5)}
    reciprocal_ranks = []
    for item in questions:
        results = search_fn(item.query, k=5)
        for n in precisions:
            found = any(hit(result, item) for result in results[:n])
            precisions[n] += int(found) / n
            recalls[n] += int(found)
        rank = next((i + 1 for i, result in enumerate(results) if hit(result, item)), 0)
        reciprocal_ranks.append(1 / rank if rank else 0)
    count = max(len(questions), 1)
    return {**{f"precision@{n}": round(value / count, 4) for n, value in precisions.items()},
            **{f"recall@{n}": round(value / count, 4) for n, value in recalls.items()},
            "mrr": round(sum(reciprocal_ranks) / count, 4)}


def demo_questions() -> list[EvaluationQuestion]:
    return [EvaluationQuestion("How much annual leave can I take?", "leave_policy.txt"),
            EvaluationQuestion("What is the WFH allowance?", "wfh_policy.txt"),
            EvaluationQuestion("How long is probation?", "employee_handbook.txt"),
            EvaluationQuestion("What is the reimbursement limit?", "reimbursement_policy.txt"),
            EvaluationQuestion("When do I record attendance?", "attendance_policy.txt")]
