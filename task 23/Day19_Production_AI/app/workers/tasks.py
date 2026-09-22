from app.workers.celery_app import celery_app


@celery_app.task
def process_document(job_id: str, document_name: str) -> dict[str, str]:
    # Replace this task body with extraction, chunking, embedding, and indexing.
    return {"job_id": job_id, "status": "completed", "document_name": document_name}
