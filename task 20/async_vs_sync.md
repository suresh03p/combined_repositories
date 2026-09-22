# Synchronous vs Asynchronous Processing

## Synchronous

```text
Upload -> Extract -> Chunk -> Embed -> Store -> Response
```

The request remains open until all work completes. It is simple and useful for small files, but large documents consume request workers, increase timeout risk, and make the interface feel slow.

## Asynchronous

```text
Upload -> Create job -> Return job ID -> Background processing -> Extract -> Chunk -> Embed -> Store
```

The API returns quickly with a document ID and status. The client polls `/documents/{document_id}/status` or subscribes to job events. This improves upload experience and isolates long work, but requires durable job state, retries, idempotency, monitoring, and failure handling. The demo uses FastAPI `BackgroundTasks`; production workloads should use a durable worker queue.
