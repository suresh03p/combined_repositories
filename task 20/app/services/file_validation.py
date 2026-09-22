import re
from pathlib import Path
from fastapi import HTTPException, UploadFile, status
from app.core.config import ALLOWED_EXTENSIONS, MAX_UPLOAD_SIZE


def safe_filename(filename: str | None) -> str:
    name = Path(filename or "upload.txt").name
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    if not name or name in {".", ".."}:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid filename")
    return name


def validate_upload(filename: str | None, content: bytes, content_type: str | None) -> str:
    clean = safe_filename(filename)
    extension = Path(clean).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Only PDF, HTML, and TXT files are allowed")
    if not content:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Uploaded file is empty")
    if len(content) > MAX_UPLOAD_SIZE:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Uploaded file exceeds the size limit")
    allowed_mimes = {".pdf": {"application/pdf"}, ".html": {"text/html"}, ".htm": {"text/html"}, ".txt": {"text/plain", "application/octet-stream"}}
    if content_type and content_type not in allowed_mimes[extension]:
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "MIME type does not match the file extension")
    return clean
