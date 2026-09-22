"""Create and inspect a local ChromaDB collection."""

from src.embeddings import embed_texts
from src.vector_store import COLLECTION_NAME, get_collection


if __name__ == "__main__":
    collection = get_collection()
    documents = ["Employees use the HR portal for leave requests.", "Salary is processed monthly."]
    collection.upsert(
        ids=["demo-1", "demo-2"],
        documents=documents,
        embeddings=embed_texts(documents),
        metadatas=[{"source": "demo", "chunk": 1}, {"source": "demo", "chunk": 2}],
    )
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Stored chunks: {collection.count()}")
    print(collection.get(include=["documents", "metadatas"]))
