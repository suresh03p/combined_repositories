"""Bounded context construction for the answer stage."""


def build_context(results: list[dict], max_results: int = 5) -> str:
    return "\n\n".join(f"[{item['source']} - Page {item['page']} - {item['section']}]\n{item['content']}"
                          for item in results[:max_results])