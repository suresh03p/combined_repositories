def retrieve(query: str) -> list[dict[str, str]]:
    if "leave" in query.casefold():
        return [{"content": "Employees receive 18 annual leave days.", "source": "leave_policy.pdf"}]
    return []
