import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.job import Job
from app.schemas.job import JobResponse

router = APIRouter(prefix="/api/v1", tags=["documents"])


@router.post("/documents/process", response_model=JobResponse, status_code=202)
def process_document(document_name: str = "document.pdf", db: Session = Depends(get_db)) -> JobResponse:
    job = Job(job_id=f"JOB-{uuid.uuid4().hex[:12]}", document_name=document_name, status="queued")
    db.add(job)
    db.commit()
    return JobResponse(job_id=job.job_id, status=job.status, document_name=job.document_name)
