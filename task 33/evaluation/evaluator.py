import json
import os
from pathlib import Path
from typing import Any, Dict, List

from scoring import score_response

ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / 'evaluation' / 'dataset.json'


def load_dataset(path: str | Path) -> List[Dict[str, Any]]:
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def mock_ai_app(question: str) -> Dict[str, Any]:
    question_lower = question.lower()
    if 'refund' in question_lower and '7 days' in question_lower:
        return {
            'answer': 'Refunds are available within 7 days.',
            'sources': ['refund_policy.pdf'],
            'context': 'Refunds are available within 7 days.'
        }
    if 'leave' in question_lower or 'vacation' in question_lower:
        return {
            'answer': 'Employees receive 15 days of annual leave.',
            'sources': ['employee_handbook.pdf'],
            'context': 'Employees receive 15 days of annual leave.'
        }
    if 'what is the wi' in question_lower or 'password' in question_lower:
        return {
            'answer': 'I do not have enough information to answer that.',
            'sources': [],
            'context': 'No known office password is listed in the available documents.'
        }
    if 'mars' in question_lower or 'board' in question_lower or 'salary' in question_lower:
        return {
            'answer': 'I do not have enough information to answer that.',
            'sources': [],
            'context': 'No supporting source exists for this claim.'
        }
    return {
        'answer': 'The company headquarters is in Seattle, Washington.',
        'sources': ['company_profile.pdf'],
        'context': 'The company headquarters is in Seattle, Washington.'
    }


def evaluate_dataset(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    evaluated_rows = []
    for row in rows:
        result = mock_ai_app(row['question'])
        evaluation = score_response(
            question=row['question'],
            expected=row['expected_answer'],
            actual=result['answer'],
            context=result['context'],
        )
        evaluated_rows.append({
            'id': row.get('id', 'unknown'),
            'question': row['question'],
            'expected_answer': row['expected_answer'],
            'actual_answer': result['answer'],
            'retrieved_sources': result['sources'],
            'expected_source': row.get('expected_source', 'unknown'),
            'exact_match': evaluation['exact_match'],
            'semantic_match': evaluation['semantic_match'],
            'relevance': evaluation['relevance'],
            'groundedness': evaluation['groundedness'],
            'quality': evaluation['quality'],
        })

    total = len(evaluated_rows)
    passed_exact = sum(1 for row in evaluated_rows if row['exact_match'])
    passed_semantic = sum(1 for row in evaluated_rows if row['semantic_match'])
    relevance_scores = [row['relevance'] for row in evaluated_rows]
    groundedness_scores = [row['groundedness'] for row in evaluated_rows]
    quality_scores = [row['quality'] for row in evaluated_rows]

    summary = {
        'total_tests': total,
        'passed_exact_match': passed_exact,
        'passed_semantic_match': passed_semantic,
        'average_relevance': round(sum(relevance_scores) / total, 4) if total else 0.0,
        'average_groundedness': round(sum(groundedness_scores) / total, 4) if total else 0.0,
        'average_quality': round(sum(quality_scores) / total, 4) if total else 0.0,
        'results': evaluated_rows,
    }
    return summary


def quality_gate(summary: Dict[str, Any], thresholds: Dict[str, float]) -> Dict[str, Any]:
    status = 'PASS'
    for metric, minimum in thresholds.items():
        value = summary.get(metric, 0.0)
        if value < minimum:
            status = 'FAIL'
    return {'status': status, 'thresholds': thresholds, 'summary': summary}


if __name__ == '__main__':
    dataset = load_dataset(DATASET_PATH)
    summary = evaluate_dataset(dataset)
    thresholds = {
        'average_relevance': 0.80,
        'average_groundedness': 0.85,
        'average_quality': 0.80,
    }
    result = quality_gate(summary, thresholds)
    print(json.dumps(result, indent=2))
