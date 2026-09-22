# Day 10: Embeddings From Zero

## How can a computer understand the meaning of a sentence?

A human sees a connection between these sentences:

- I want to book a cab.
- I need a taxi.
- How can I reserve a ride?

A computer begins with characters and words. Embeddings convert text into a list of numbers that places its meaning in a mathematical space:

```text
"I want to book a cab"
          |
      Embedding model
          |
[0.21, -0.43, 0.87, 0.12, ...]
```

The numbers are not a dictionary definition and they are not random. A model learned patterns from many examples. Similar uses of language tend to produce vectors that are close according to a distance measure.

## Simple definitions

1. **Embedding:** A numerical representation of text, an image, or another object that captures useful patterns.
2. **Vector:** An ordered list of numbers, such as `[0.2, -0.4, 0.8]`.
3. **Vector space:** The imagined mathematical space where vectors can be compared by their position and direction.
4. **Dimension:** The number of values in a vector. A vector with 384 numbers has 384 dimensions.
5. **Semantic meaning:** What a piece of language means, not only the exact words it contains.
6. **Semantic similarity:** How close two pieces of text are in meaning.
7. **Similarity search:** Finding stored items whose vectors are closest to a query vector.
8. **Cosine similarity:** A score based on the angle between two vectors. A larger score usually means more similar direction.
9. **Document:** A source of information, such as a policy file or web page.
10. **Chunk:** A smaller piece of a document used for embedding and retrieval.
11. **Metadata:** Extra labels stored with data, such as source filename, page, or chunk number.
12. **Vector database:** A database designed to store vectors and efficiently find nearby vectors.
13. **Retriever:** The component that selects relevant chunks for a question.
14. **Context:** Information supplied to a model so it can answer a question.
15. **RAG:** Retrieval-Augmented Generation: retrieve useful information first, then give it to a language model to help generate an answer.

## The practical flow

```text
Documents -> chunks -> embeddings -> vector database
Question -> question embedding -> nearest chunks -> context -> answer
```

The model in this project is `all-MiniLM-L6-v2`. It produces 384-dimensional vectors. The important lesson is not the number 384; another model may produce 768 or 1536 dimensions. Every vector stored in one collection must use the same embedding model and dimension.

## Cosine similarity without heavy math

Imagine two arrows starting at the same point. Cosine similarity asks whether they point in the same direction. Text with related meaning should point in similar directions. Exact scores depend on the model and the text, so compare scores within the same experiment rather than treating one score as a universal truth.

## Chunking and context

A very large chunk may contain too much unrelated material and may use an AI model's context window inefficiently. A tiny chunk may lose the sentence that explains a rule. Overlap repeats a small boundary so an idea split between chunks can still be retrieved together. Start with a size such as 200 words and an overlap of 50, then evaluate retrieval quality.

## Core explanation

I take documents, split them into smaller pieces, convert those pieces into embeddings, store the embeddings in a vector database, search for pieces most similar to the user's question, and give those pieces to an LLM so it can generate an answer based on the retrieved information. If the context does not contain an answer, the system should say so instead of inventing one.
