"""Conservative follow-up question rewriting without sending memory to search."""


def rewrite_query(question: str, history: list[dict]) -> str:
    lowered = question.lower().strip()
    if not any(word in lowered for word in (" it", "that", "they", "them", "this")):
        return question.strip()
    previous = next((item["content"] for item in reversed(history) if item["role"] == "user"), "")
    topic = previous.replace("What is the ", "").replace("what is the ", "").rstrip("?")
    return f"{question.rstrip('?')} according to the {topic}." if topic else question.strip()