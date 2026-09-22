"""ChromaDB storage for document chunks and their embeddings."""

from pathlib import Path

import chromadb

from src.embeddings import embed_query, embed_texts

COLLECTION_NAME = "company_knowledge"
DEFAULT_PATH = Path(__file__).resolve().parents[1] / ".chroma"


def get_collection(path=DEFAULT_PATH):
    client = chromadb.PersistentClient(path=str(path))
    return client.get_or_create_collection(COLLECTION_NAME)


def add_records(collection, records):
    if not records:
        return
    embeddings = embed_texts([record["document"] for record in records])
    collection.upsert(
        ids=[record["id"] for record in records],
        documents=[record["document"] for record in records],
        embeddings=embeddings,
        metadatas=[record["metadata"] for record in records],
    )


def search(collection, question, top_k=3):
    result = collection.query(query_embeddings=[embed_query(question)], n_results=top_k)
    matches = []
    for index, document in enumerate(result["documents"][0]):
        matches.append(
            {
                "document": document,
                "metadata": result["metadatas"][0][index],
                "distance": result["distances"][0][index],
            }
        )
    return matches
