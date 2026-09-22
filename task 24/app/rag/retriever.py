def retrieve(query: str, documents: list[dict]) -> list[dict]:
    words = set(query.lower().split())
    return [document for document in documents if words.intersection(document["content"].lower().split())]
