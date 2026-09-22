import time
from app.database.vector_store import search
from app.core.logging import get_logger

logger = get_logger(__name__)

def retrieve(question: str, top_k: int = 3):
    started = time.perf_counter()
    logger.info("Retrieval started")
    results = search(question, top_k)
    logger.info("Retrieval completed in %.3f seconds", time.perf_counter() - started)
    return results
