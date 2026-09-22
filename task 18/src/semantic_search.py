"""Search the shared company knowledge collection."""

from src.vector_store import get_collection, search


def search_company_knowledge(question, top_k=3):
    return search(get_collection(), question, top_k=top_k)


if __name__ == "__main__":
    question = input("Question: ")
    for number, result in enumerate(search_company_knowledge(question), start=1):
        print(f"\nResult {number}")
        print(f"Source: {result['metadata']['source']}")
        print(f"Distance: {result['distance']:.4f}")
        print(f"Content: {result['document']}")
