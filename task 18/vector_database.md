# Vector Databases

## Traditional databases

MySQL and PostgreSQL organize structured records into rows, columns, and tables. A table might contain `Employee_ID`, `Name`, `Department`, and `Salary`. SQL is excellent when we know the field and condition we want:

```sql
SELECT name FROM employees WHERE department = 'HR';
```

A keyword query such as `WHERE text LIKE '%leave%'` looks for matching characters. It may miss a document that says `vacation` or `time away` instead of `leave`.

## Vector databases

A vector database stores an ID, a document or chunk, an embedding, and metadata. It creates an index that makes it efficient to find vectors near a query vector.

```text
Document -> embedding -> vector database
Question -> embedding -> nearest stored chunks
```

The search is semantic rather than an exact spelling check. A question such as `How can I take vacation?` can be close to a chunk saying `Employees may request leave through the HR portal`, because the embedding model has learned related language patterns.

## ChromaDB

ChromaDB is a developer-friendly vector database that runs locally and exposes collections. This project uses a persistent collection called `company_knowledge`. Each chunk is stored with metadata such as:

```python
{"source": "leave_policy.txt", "chunk": 1}
```

Metadata lets us show where an answer came from, filter by source, and inspect retrieval quality. The database stores vectors, but the embedding model creates those vectors. ChromaDB does not magically know the meaning of raw text without an embedding function or supplied embeddings.

## Retrieval

A retriever embeds the question, asks the vector database for the nearest chunks, and returns the top K results. Chroma reports a distance; smaller distance means closer for the configured metric. Cosine similarity reports a score where larger generally means more similar. They express related ideas with opposite score directions, so do not compare the numbers directly.

## What it does not guarantee

Semantic search is not proof that a result is correct. It can retrieve a plausible but irrelevant chunk, especially when documents are short, ambiguous, or from a different domain. That is why this project includes ten test questions and an accuracy report. A production system may combine keyword and vector search, filter metadata, rerank candidates, and evaluate answers as well as retrieval.
