# Synchronous vs Asynchronous AI Work

`GET /health` is fast and should complete during the request. Processing a 500-page PDF is different: extract text, chunk it, create embeddings, and write vectors can take seconds or minutes.

- **Synchronous:** the caller waits for the complete result. Use for short work where latency is predictable.
- **Asynchronous I/O:** the server can await network-bound work without blocking its event loop. Use when the work is still part of one request.
- **Background worker:** the API creates a job and returns immediately. A Celery worker consumes a Redis queue and updates job state.

The project exposes `POST /api/v1/documents/process` and `GET /api/v1/jobs/{job_id}`. The Celery task in `app/workers/tasks.py` is the extension point for extraction, chunking, embedding, and vector storage.
