"""Interactive assistant using retrieved company policy context."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from document_store import load_documents, add_records, get_collection
from src.rag_pipeline import answer_question, build_context


if __name__ == "__main__":
    records = load_documents(Path(__file__).resolve().parents[1] / "data/documents")
    add_records(get_collection(), records)
    print("Company knowledge assistant. Type 'quit' to stop.")
    while True:
        question = input("\nYou: ").strip()
        if question.lower() in {"quit", "exit"}:
            break
        answer, results = answer_question(question)
        print("\nSources:\n" + build_context(results))
        print("\nAssistant:\n" + answer)
