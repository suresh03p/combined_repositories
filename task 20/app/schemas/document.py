from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict

DocumentStatus = Literal["uploaded", "processing", "completed", "failed"]

class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    document_id: str
    file_name: str
    file_type: str
    status: DocumentStatus
    upload_date: datetime
    chunk_count: int = 0
    document_hash: str

class UploadResponse(BaseModel):
    document_id: str
    status: DocumentStatus
    message: str

class StatusResponse(BaseModel):
    document_id: str
    status: DocumentStatus
    error: str | None = None
