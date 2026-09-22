# Day 14 Performance Baseline

## Environment

No Day 13 project was present in the workspace, so a Day 13 baseline could not be measured. The current service is an offline demonstration with deterministic local embeddings and no network LLM.

| Operation | Time | Measurement status |
|---|---:|---|
| Document upload | pending | Measure with an actual request and file |
| Text extraction | pending | PDF parser not installed in offline demo |
| Chunking | pending | Run `performance_monitor.py` around ingestion |
| Embedding | pending | Local deterministic implementation |
| Vector storage | pending | In-memory store |
| Retrieval | pending | Measure with `/chat` |
| LLM response | N/A | Offline extractive answer; no external LLM |
| Total response | pending | Measure end-to-end |

## Method

Record at least five runs with the same document and question. Report average, minimum, and maximum. Keep document size, chunk size, top-K, embedding model, vector database, and LLM model constant.

## Largest operation

There is no defensible measured winner until the Day 13 system is available and the timings above are captured. In a typical hosted RAG system, embedding generation and LLM generation are the leading candidates; measure rather than assume.
