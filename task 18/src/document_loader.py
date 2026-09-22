"""Load policy files and turn them into metadata-rich chunks."""

from pathlib import Path

from chunking import split_with_overlap


def load_documents(directory, chunk_size=200, overlap=50):
    records = []
    for path in sorted(Path(directory).glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        chunks = split_with_overlap(text, chunk_size, overlap)
        for number, chunk in enumerate(chunks, start=1):
            records.append(
                {
                    "id": f"{path.stem}-{number}",
                    "document": chunk,
                    "metadata": {"source": path.name, "chunk": number},
                }
            )
    return records
