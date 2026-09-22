# Embeddings From Zero

An embedding converts text into a numerical representation that captures semantic relationships.

```text
"How many leave days do employees get?"
        -> [0.13, -0.42, 0.91, ...]
```

- **Embedding:** the output representation for one text.
- **Vector:** an ordered numeric array.
- **Dimension:** the number of values in that array.
- **Similarity:** a score estimating how close two vectors are.
- **Cosine similarity:** $cos(A,B) = (A . B) / (||A|| ||B||)$; it compares direction rather than raw length.

This project defaults to a deterministic TF-IDF vectorizer for offline experiments. A production deployment can replace it with a domain-tested embedding model while preserving the same `encode(texts)` interface.
