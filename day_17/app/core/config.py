import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = Path(os.getenv("DATA_DIR", BASE_DIR / "data"))
UPLOAD_DIR = DATA_DIR / "uploads"
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10")) * 1024 * 1024
API_TOKEN = os.getenv("RAG_API_TOKEN", "change-me")
ALLOWED_EXTENSIONS = {".pdf", ".html", ".htm", ".txt"}
