"""Embedding helpers using a small, widely used sentence-transformer model."""

from functools import lru_cache

MODEL_NAME = "all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_model():
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(MODEL_NAME)


def embed_texts(texts):
    """Return one 384-dimensional embedding for each text."""
    if not texts:
        return []
    return get_model().encode(list(texts), normalize_embeddings=True).tolist()


def embed_query(query):
    return embed_texts([query])[0]


def embedding_dimension():
    return get_model().get_sentence_embedding_dimension()
