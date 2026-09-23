from pathlib import Path

from parsing.page_parser import write_pages


for document in sorted(Path("data/raw").glob("*.pdf")):
    outputs = write_pages(document)
    print(f"{document.name}: {len(outputs)} pages")