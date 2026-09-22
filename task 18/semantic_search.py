"""Root-level entry point for semantic search."""

from src.semantic_search import search_company_knowledge


if __name__ == "__main__":
    question = input("Question: ")
    for number, result in enumerate(search_company_knowledge(question), start=1):
        print(f"\nResult {number}")
        print(f"Source: {result['metadata']['source']}")
        print(f"Similarity / Distance: {result['distance']:.4f}")
        print(f"Content: {result['document']}")
