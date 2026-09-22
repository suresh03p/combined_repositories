from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile, status
from app.core.security import require_token
from app.schemas.document import DocumentResponse, StatusResponse, UploadResponse
from app.services.document_service import create_document, delete_document_record, get_document, list_documents, process_document
from app.services.file_validation import validate_upload

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_document(background_tasks: BackgroundTasks, file: UploadFile = File(...), _: str = Depends(require_token)):
    content = await file.read()
    clean_name = validate_upload(file.filename, content, file.content_type)
    record = create_document(clean_name, file.content_type or "application/octet-stream", content)
    background_tasks.add_task(process_document, record["document_id"])
    return UploadResponse(document_id=record["document_id"], status="processing", message="Document uploaded successfully")

@router.get("", response_model=list[DocumentResponse])
def documents(_: str = Depends(require_token)):
    return list_documents()

@router.get("/{document_id}", response_model=DocumentResponse)
def document(document_id: str, _: str = Depends(require_token)):
    record = get_document(document_id)
    if not record:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")
    return record

@router.get("/{document_id}/status", response_model=StatusResponse)
def document_status(document_id: str, _: str = Depends(require_token)):
    record = get_document(document_id)
    if not record:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")
    return {"document_id": document_id, "status": record["status"], "error": record["error"]}

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_document(document_id: str, _: str = Depends(require_token)):
    if not delete_document_record(document_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")
