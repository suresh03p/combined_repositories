"""Extract readable, metadata-rich text from HTML."""

from pathlib import Path


def load_html(file_path: str | Path) -> list[dict]:
    path = Path(file_path)
    try:
        from bs4 import BeautifulSoup
    except ImportError as exc:
        raise RuntimeError("Install beautifulsoup4 to load HTML documents.") from exc
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
        element.decompose()
    title = soup.title.get_text(" ", strip=True) if soup.title else path.stem
    headings = [node.get_text(" ", strip=True) for node in soup.find_all(["h1", "h2", "h3"])]
    paragraphs = [node.get_text(" ", strip=True) for node in soup.find_all("p")]
    links = [{"text": node.get_text(" ", strip=True), "href": node.get("href", "")} for node in soup.find_all("a")]
    text = "\n\n".join(part for part in [title, *headings, *paragraphs] if part)
    return [{"document_id": path.stem, "source": path.name, "page": 1, "text": text,
             "file_type": "html", "title": title, "headings": headings, "links": links}]