# RAG Performance Bottlenecks

1. Large documents increase parsing time, memory use, and job duration.
2. Poor chunk sizing creates too many chunks or loses useful context.
3. Duplicate uploads repeat embedding API calls and increase cost.
4. Embedding model latency and rate limits slow ingestion.
5. Vector indexes without the right metric or parameters slow retrieval.
6. Searching too many candidates increases database latency.
7. Large Top-K values create oversized prompts.
8. Re-ranking every candidate adds CPU or model latency.
9. Large prompts increase LLM time and token cost.
10. LLM queueing, rate limits, and output length dominate generation time.
11. Synchronous uploads make users wait through the full ingestion pipeline.
12. API worker saturation, serialization, and file buffering add request latency.
13. Database connections, disk I/O, and unindexed metadata queries create contention.
14. Network distance and repeated remote calls increase tail latency.

## Stage mapping

- Ingestion: parsing, cleaning, chunking, embedding, storage.
- Retrieval: query embedding, vector search, filtering, re-ranking.
- Generation: prompt construction, LLM queueing, token generation.
- API: upload buffering, worker capacity, serialization, timeouts.
- Database: index quality, connection pool, disk and metadata scans.
- Network: upload size, provider latency, retries, and regional placement.

The useful diagnostic is a timed trace for each stage, plus p50/p95 latency and failure rate. Optimization should target the largest measured contributor first.
