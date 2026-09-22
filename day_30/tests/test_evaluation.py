import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_dataset_exists_and_has_enough_questions():
    dataset_path = ROOT / 'evaluation' / 'dataset.json'
    data = json.loads(dataset_path.read_text(encoding='utf-8'))
    assert len(data) >= 30


def test_golden_dataset_exists():
    dataset_path = ROOT / 'evaluation' / 'golden_dataset.json'
    data = json.loads(dataset_path.read_text(encoding='utf-8'))
    assert len(data) >= 15


def test_scoring_logic_has_exact_match():
    import importlib.util

    spec = importlib.util.spec_from_file_location('scoring', ROOT / 'evaluation' / 'scoring.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.exact_match('7 days', '7 days') is True
    assert module.exact_match('7 days', 'Refunds are allowed for seven days.') is False
