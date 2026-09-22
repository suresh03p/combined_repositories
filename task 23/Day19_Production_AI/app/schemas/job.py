from pydantic import BaseModel


class JobResponse(BaseModel):
    job_id: str
    status: str
    document_name: str | None = None
    error: str | None = None
