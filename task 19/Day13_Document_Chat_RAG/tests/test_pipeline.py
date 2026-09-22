from pathlib import Path

from src.document_chat import DocumentChat


ROOT = Path(__file__).parents[1]


def build_chat():
    chat = DocumentChat()
    for path in (ROOT / "data/txt").glob("*.txt"):
        chat.upload(path)
    return chat


def test_upload_search_delete_reinsert():
    chat = build_chat()
    result = chat.ask("one", "How do I apply for leave?")
    assert result["retrieved"]
    assert result["sources"][0]["source"] == "leave_policy.txt"
    assert chat.delete_document("leave_policy") > 0
    assert chat.store.get_document("leave_policy") == []
    chat.upload(ROOT / "data/txt/leave_policy.txt")
    assert chat.store.get_document("leave_policy")


def test_duplicate_and_unknown_question():
    chat = build_chat()
    try:
        chat.upload(ROOT / "data/txt/leave_policy.txt")
    except ValueError as exc:
        assert str(exc) == "Document already exists."
    else:
        raise AssertionError("Duplicate was accepted")
    assert "Information not found" in chat.ask("two", "What is the office parking policy?")["answer"]


def test_follow_up_rewrite():
    chat = build_chat()
    chat.ask("three", "What is the leave policy?")
    result = chat.ask("three", "Who approves it?")
    assert "leave policy" in result["standalone_question"]