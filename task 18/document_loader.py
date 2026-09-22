"""Root-level demonstration of loading and chunking the policy collection."""

from pathlib import Path

from src.document_loader import load_documents


if __name__ == "__main__":
    records = load_documents(Path("data/documents"))
    print(f"Loaded {len(records)} chunks from data/documents")
    for record in records[:3]:
        print(record["id"], record["metadata"])
