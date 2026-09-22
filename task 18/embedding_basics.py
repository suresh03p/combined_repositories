"""See text become numerical vectors."""

from src.embeddings import MODEL_NAME, embed_texts, embedding_dimension

sentences = [
    "I want to book a cab",
    "I need a taxi",
    "Python is a programming language",
    "The weather is very cold today",
]


if __name__ == "__main__":
    for text, vector in zip(sentences, embed_texts(sentences)):
        print("Text:\n" + text)
        print("\nEmbedding:\n" + str(vector))
        print(f"\nDimension: {len(vector)}")
        print(f"Model: {MODEL_NAME}\n")
    print(f"Embedding length from model: {embedding_dimension()}")
