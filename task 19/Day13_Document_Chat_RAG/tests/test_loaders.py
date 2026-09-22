from pathlib import Path

from src.document_loader import load_document
from src.document_cleaner import clean_text


ROOT = Path(__file__).parents[1]


def test_html_loader_removes_navigation_and_scripts():
    record = load_document(ROOT / "data/html/hr_policy.html")[0]
    assert "ignore" not in record["text"]
    assert "Home" not in record["text"]
    assert "HR provides" in record["text"]


def test_txt_loader_and_cleaner():
    record = load_document(ROOT / "data/txt/leave_policy.txt")[0]
    assert record["file_type"] == "txt"
    assert clean_text("Employee    Leave\n\n\nPolicy") == "Employee Leave\n\nPolicy"