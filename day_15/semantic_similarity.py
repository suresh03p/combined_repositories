"""Compare sentence meaning with cosine similarity."""

from sklearn.metrics.pairwise import cosine_similarity

from src.embeddings import embed_texts

pairs = [
    ("I need a taxi.", "I want to book a cab."),
    ("I need a taxi.", "Python is a programming language."),
    ("Python is used for programming.", "Python is a programming language."),
    ("The server is running in AWS.", "I want to book a taxi."),
]


if __name__ == "__main__":
    vectors = embed_texts([sentence for pair in pairs for sentence in pair])
    for number, ((first, second), pair_vectors) in enumerate(
        zip(pairs, zip(vectors[::2], vectors[1::2])), start=1
    ):
        score = cosine_similarity([pair_vectors[0]], [pair_vectors[1]])[0][0]
        print(f"Pair {number}")
        print(f"Sentence A: {first}")
        print(f"Sentence B: {second}")
        print(f"Similarity Score: {score:.4f}\n")
