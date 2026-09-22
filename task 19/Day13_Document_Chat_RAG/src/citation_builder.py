"""Build citations only from retrieved evidence."""


def citation_structure(result: dict) -> dict:
    return {"source": result["source"], "page": result["page"], "section": result["section"]}


def build_citations(results: list[dict]) -> list[dict]:
    seen = set()
    citations = []
    for result in results:
        key = (result["source"], result["page"], result["section"])
        if key not in seen:
            seen.add(key)
            citations.append(citation_structure(result))
    return citations


def format_sources(citations: list[dict]) -> str:
    return "\n".join(f"[{number}] {item['source']} - Page {item['page']} - {item['section']}"
                     for number, item in enumerate(citations, start=1))