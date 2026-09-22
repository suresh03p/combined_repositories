# Production RAG Architecture

## Basic RAG

```text
Question -> Vector Search -> LLM -> Answer
```

The basic flow embeds a question, retrieves nearest chunks, and asks an LLM to answer. It is useful as a proof of concept but assumes documents are already clean, indexed, and trustworthy.

## Production RAG

```text
Document -> Ingestion -> Validation -> Text Extraction -> Cleaning -> Chunking
-> Metadata -> Embeddings -> Vector Database -> Retrieval -> Re-ranking
-> Context Construction -> LLM -> Answer -> Sources
```

1. **Document:** The user or an administrator supplies a PDF, HTML, or TXT source.
2. **Ingestion:** The system accepts the file, assigns an identity, and starts processing.
3. **Validation:** It checks file type, size, permissions, readability, and whether the document is a duplicate.
4. **Text Extraction:** Format-specific parsers turn bytes into text while preserving PDF pages and HTML structure.
5. **Cleaning:** Repeated whitespace, headers, footers, broken lines, empty content, and HTML artifacts are removed.
6. **Chunking:** Content is divided into coherent page/section/paragraph chunks sized for retrieval and the model context window.
7. **Metadata:** Each chunk receives document ID, source, file type, page, section, category, upload date, and chunk ID.
8. **Embeddings:** Chunks become vectors in a shared semantic space; batching and model versioning matter in production.
9. **Vector Database:** Vectors, text, and metadata are persisted and indexed for similarity and metadata filtering.
10. **Retrieval:** A standalone user query finds candidate chunks, optionally filtered by tenant, category, or document.
11. **Re-ranking:** A stronger model reorders the smaller candidate set to improve relevance.
12. **Context Construction:** The system deduplicates, orders, truncates, and labels evidence before sending it to the LLM.
13. **LLM:** The model answers from the supplied context and follows a no-invention instruction.
14. **Answer:** The user receives a concise response or an explicit not-found message when evidence is insufficient.
15. **Sources:** Citations are created only from retrieved metadata so users can inspect the evidence.

## Key Difference
Basic RAG focuses on nearest-neighbor lookup and generation. Production RAG treats documents, provenance, failure cases, lifecycle management, evaluation, security, and operations as first-class parts of the system.