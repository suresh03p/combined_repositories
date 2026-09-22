"""Load, embed, and persist all company policy chunks in ChromaDB."""

from pathlib import Path

from src.document_loader import load_documents
from src.vector_store import add_records, get_collection


if __name__ == "__main__":
    records = load_documents(Path("data/documents"), chunk_size=200, overlap=50)
    collection = get_collection()
    add_records(collection, records)
    stored = collection.get(include=["documents", "metadatas"])
    print(f"Documents/chunks stored: {collection.count()}")
    print(f"IDs returned: {len(stored['ids'])}")
    for metadata in stored["metadatas"][:5]:
        print(metadata)
