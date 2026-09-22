from fastapi import HTTPException
from app.auth.models import User

def assert_document_access(user: User, document: dict) -> None:
    if document.get("tenant_id") != user.tenant_id:
        raise HTTPException(403, "Document belongs to another tenant")
    if document.get("access_level") == "private" and document.get("owner_id") != user.id:
        raise HTTPException(403, "Private document is not owned by this user")

def filter_documents(user: User, documents: list[dict]) -> list[dict]:
    return [document for document in documents if document.get("tenant_id") == user.tenant_id and (document.get("access_level") != "private" or document.get("owner_id") == user.id)]
