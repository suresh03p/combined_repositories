from app.schemas.chat import ChatResponse, Source
from app.services.retrieval_service import retrieve
from app.services import cache_service


def answer_question(question: str, conversation_id: str) -> ChatResponse:
    cached = cache_service.get(question, "current")
    if cached:
        return cached.model_copy(update={"cached": True})
    results = retrieve(question, top_k=3)
    if not results:
        response = ChatResponse(answer="I could not find relevant information in the uploaded documents.", sources=[])
    else:
        sources = [Source(document=item.file_name, page=item.page, chunk_id=item.chunk_id) for item, _ in results]
        best = results[0][0]
        response = ChatResponse(answer=f"Based on {best.file_name}: {best.text[:600]}", sources=sources)
    cache_service.put(question, "current", response)
    return response
