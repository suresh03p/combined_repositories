from typing import Dict, List


def context_relevance(question: str, retrieved_chunks: List[str]) -> Dict[str, str]:
    if not retrieved_chunks:
        return {"status": "FAIL", "reason": "No retrieved context provided."}

    question_lower = question.lower()
    relevant = []
    for chunk in retrieved_chunks:
        if question_lower in chunk.lower() or any(token in chunk.lower() for token in question_lower.split() if len(token) > 3):
            relevant.append(chunk)

    if relevant:
        return {"status": "PASS", "reason": "Retrieved context appears relevant to the question.", "matches": len(relevant)}
    return {"status": "FAIL", "reason": "Retrieved context appears unrelated to the question.", "matches": 0}
