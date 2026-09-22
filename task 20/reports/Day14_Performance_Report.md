# Day 13 vs Day 14 Performance Report

## Comparison

| Metric | Day 13 | Day 14 |
|---|---|---|
| Document processing | Not available: project absent | Background task; measure per document |
| Embedding time | Not available | Deterministic local embedding; measure per chunk |
| Retrieval time | Not available | In-memory cosine search; measure per request |
| LLM time | Not available | N/A in offline demo |
| Total response | Not available | Measure with repeated `/chat` requests |
| Duplicate embeddings | Not available | Reused by chunk hash |
| Cached responses | Not available | Enabled by normalized question + document version |

## Answers

1. What became faster? Upload acknowledgement is fast because processing is backgrounded; repeated questions avoid retrieval and generation.
2. What remained slow? Real embedding and LLM calls remain the likely production costs and are not present in this offline demo.
3. Did caching help? It should reduce repeated request work; validate with timing runs and cache-hit counters.
4. Did reducing Top-K help? It usually reduces context and generation cost, but must be balanced against answer quality.
5. Did asynchronous processing improve upload experience? Yes: the client receives `202 Accepted` while processing continues.
6. What is the biggest remaining bottleneck? Unknown until a real Day 13 baseline and hosted LLM timings are captured.
7. What would you optimize next? Add durable jobs, real stage timings, p95 metrics, embedding cache persistence, and a vector database benchmark.
