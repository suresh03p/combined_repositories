"""Root-level entry point for the first retrieval-augmented pipeline."""

from src.rag_pipeline import answer_question, build_context


if __name__ == "__main__":
    question = input("Question: ")
    answer, results = answer_question(question)
    print("\nContext:\n" + build_context(results))
    print("\nAnswer:\n" + answer)
