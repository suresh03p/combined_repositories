"""Retrieval stage plus a safe context-grounded answer formatter."""

from src.semantic_search import search_company_knowledge

NO_ANSWER = "Information not available in the provided company documents."


def build_context(results):
    return "\n\n".join(
        f"[{item['metadata']['source']}, chunk {item['metadata']['chunk']}]\n{item['document']}"
        for item in results
    )


def answer_question(question, top_k=3):
    results = search_company_knowledge(question, top_k=top_k)
    if not results:
        return NO_ANSWER, results
    # This is deliberately extractive: it works without an LLM API key.
    answer = " ".join(result["document"] for result in results[:2])
    return answer, results


if __name__ == "__main__":
    question = input("Question: ")
    answer, results = answer_question(question)
    print("\nRetrieved context:\n" + build_context(results))
    print("\nAnswer:\n" + answer)
