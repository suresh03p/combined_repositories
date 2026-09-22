# Day 13 Document Chat RAG

## Project Overview
This project evolves the Day 11 company-policy RAG demo into a document-chat architecture with ingestion, cleaning, metadata, duplicate detection, chunking, retrieval, citations, and conversation memory.

## Problem Statement
A basic demo can retrieve text, but a useful document assistant must accept several file types, preserve provenance, handle failures, and keep conversation context separate from knowledge retrieval.

## RAG Architecture
Documents are validated, extracted, cleaned, chunked by page and section, enriched with metadata, embedded/stored, retrieved, re-ranked, placed into bounded context, and answered with citations. The local reference implementation uses deterministic lexical cosine scoring so it runs without an API key; the `VectorStore` API is ready for Chroma or another embedding backend.

## Supported File Types
PDF, HTML/HTM, and TXT.

## Document Ingestion Process
`document_loader.py` dispatches to the appropriate extractor. HTML removes script, style, navigation, header, footer, and aside elements. PDF records preserve page numbers.

## Chunking Strategy
Text is cleaned and grouped into page, section, paragraph, and bounded word chunks. Each chunk keeps document, page, section, source, and chunk identifiers.

## Embedding Strategy
The production boundary is `VectorStore`; the demo uses token overlap for offline reproducibility. Sentence-transformer embeddings can replace `search` without changing callers.

## Vector Database
`VectorStore` implements `add_documents`, `delete_document`, `search`, and `get_document`. Chroma remains the natural persistent backend from Day 11.

## Retrieval Strategy
Queries are rewritten when they contain follow-up pronouns, then only the standalone query is searched. Results include content, source, page, section, document ID, and score.

## Re-ranking
The reference interface returns scored results; a production deployment should add a cross-encoder re-ranker after initial retrieval.

## Conversation Memory
`ConversationMemory` stores conversation ID, role, content, and UTC timestamp. It is used for query understanding, never as document content.

## Citation System
Citations are generated exclusively from retrieved result metadata and formatted as source, page, and section.

## Error Handling
Unsupported, empty, duplicate, unavailable, and no-answer cases have explicit messages in `error_handling.py`.

## Evaluation Results
Run `pytest -q` and use `rag_answer_evaluation.py` with an ingested corpus. The 20-question dataset measures retrieval, answer, and citation accuracy separately.

## Installation
`python -m pip install -r requirements.txt`

## How to Run
From this directory: `pytest -q`. To use the API, instantiate `DocumentChat`, call `upload(path)`, then `ask(conversation_id, question)`.

## Example Questions
How do I apply for leave? Who approves leave? What is the salary policy? What is the attendance policy?

## Limitations
The offline store is not persistent and lexical scoring is less capable than neural embeddings. PDF extraction depends on readable text rather than OCR.

## Future Improvements
Add Chroma persistence, batch embeddings, cross-encoder re-ranking, OCR, access control, observability, and an HTTP/UI layer.