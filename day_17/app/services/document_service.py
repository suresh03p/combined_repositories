import hashlib
import html
import re
from datetime import datetime, timezone
from pathlib import Path
from app.core.config import UPLOAD_DIR
from app.core.logging import get_logger
from app.database.vector_store import Chunk, add_chunks, count_for_document, delete_document
from app.services.embedding_service import cached_embed, document_hash

logger = get_logger(__name__)
_documents: dict[str, dict] = {}
_next_id = 1

def create_document(file_name: str, file_type: str, content: bytes) -> dict:
    global _next_id
    document_id = f"DOC-{_next_id:03d}"
    _next_id += 1
    digest = document_hash(content)
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    (UPLOAD_DIR / f"{document_id}_{file_name}").write_bytes(content)
    record = {"document_id": document_id, "file_name": file_name, "file_type": file_type, "status": "uploaded", "upload_date": datetime.now(timezone.utc), "chunk_count": 0, "document_hash": digest, "error": None}
    _documents[document_id] = record
    return record

def get_document(document_id: str) -> dict | None:
    return _documents.get(document_id)

def list_documents() -> list[dict]:
    return list(_documents.values())

def process_document(document_id: str) -> None:
    record = _documents[document_id]
    record["status"] = "processing"
    logger.info("Document %s processing started", document_id)
    try:
        path = next(UPLOAD_DIR.glob(f"{document_id}_*"))
        content = path.read_bytes()
        extension = Path(record["file_name"]).suffix.lower()
        if extension == ".pdf":
            text = "PDF text extraction requires pypdf; upload TXT or HTML for the offline demo."
        elif extension in {".html", ".htm"}:
            text = re.sub(r"<[^>]+>", " ", html.unescape(content.decode("utf-8", errors="ignore")))
        else:
            text = content.decode("utf-8", errors="ignore")
        words = text.split()
        chunks = [" ".join(words[index:index + 180]) for index in range(0, len(words), 180)] or ["No extractable text found."]
        vector_chunks = []
        for index, chunk_text in enumerate(chunks, 1):
            vector, _ = cached_embed(chunk_text)
            vector_chunks.append(Chunk(f"{document_id}-CH-{index:03d}", document_id, record["file_name"], chunk_text, vector, index if extension == ".pdf" else None))
        add_chunks(vector_chunks)
        record["chunk_count"] = count_for_document(document_id)
        record["status"] = "completed"
        logger.info("Document %s processing completed with %s chunks", document_id, record["chunk_count"])
    except Exception as exc:
        record["status"] = "failed"
        record["error"] = str(exc)
        logger.exception("Document %s processing failed", document_id)

def delete_document_record(document_id: str) -> bool:
    record = _documents.pop(document_id, None)
    if not record:
        return False
    delete_document(document_id)
    for path in UPLOAD_DIR.glob(f"{document_id}_*"):
        path.unlink(missing_ok=True)
    return True
