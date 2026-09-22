"""Complete local document-chat flow with deterministic grounded answers."""

from pathlib import Path

from .citation_builder import build_citations, format_sources
from .conversation_memory import ConversationMemory
from .context_builder import build_context
from .document_loader import load_document
from .duplicate_detection import DuplicateDetector
from .production_chunking import chunk_documents
from .query_rewriter import rewrite_query
from .source_retriever import retrieve
from .vector_store import VectorStore


class DocumentChat:
    def __init__(self):
        self.store = VectorStore()
        self.memory = ConversationMemory()
        self.duplicates = DuplicateDetector()

    def upload(self, file_path: str | Path) -> int:
        path = Path(file_path)
        if path.suffix.lower() not in {".pdf", ".html", ".htm", ".txt"}:
            raise ValueError("Unsupported file type.")
        if not self.duplicates.add(path):
            raise ValueError("Document already exists.")
        pages = load_document(path)
        if not any(page.get("text", "").strip() for page in pages):
            raise ValueError("Document contains no readable text.")
        chunks = chunk_documents(pages)
        self.store.add_documents(chunks)
        return len(chunks)

    def delete_document(self, document_id: str) -> int:
        removed = self.store.delete_document(document_id)
        if removed:
            self.duplicates._hashes = {
                digest: name for digest, name in self.duplicates._hashes.items()
                if Path(name).stem != document_id
            }
        return removed

    def ask(self, conversation_id: str, question: str) -> dict:
        history = self.memory.get(conversation_id)
        standalone = rewrite_query(question, history)
        results = retrieve(self.store, standalone)
        self.memory.add(conversation_id, "user", question)
        if not results:
            answer = "Information not found in the uploaded documents."
            sources = []
        else:
            answer = results[0]["content"]
            sources = build_citations(results)
            answer += "\n\nSources:\n" + format_sources(sources)
        self.memory.add(conversation_id, "assistant", answer)
        return {"question": question, "standalone_question": standalone, "answer": answer,
                "retrieved": results, "sources": sources}