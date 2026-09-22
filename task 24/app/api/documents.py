from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from app.auth.models import Role, User
from app.auth.permissions import require_roles
from app.auth.security import get_current_user
from app.main import DOCUMENTS
router = APIRouter(prefix="/api/v1/documents", tags=["documents"])
class DocumentRequest(BaseModel):
    content: str = Field(min_length=1, max_length=100000)
    access_level: str = "private"
@router.post("/process")
def process_document(data: DocumentRequest, user: User = Depends(require_roles(Role.AI_OPERATOR, Role.ADMIN))):
    document = {"document_id": f"doc-{len(DOCUMENTS) + 1}", "tenant_id": user.tenant_id, "owner_id": user.id, "access_level": data.access_level, "created_at": "2026-09-04", "content": data.content}
    DOCUMENTS.append(document)
    return {"status": "processed", "document_id": document["document_id"]}
