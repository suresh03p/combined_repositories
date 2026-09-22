"""Small, dependency-free chunking experiments for Day 10."""


def split_into_chunks(text, chunk_size):
    """Split text into word-based chunks with no overlap."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    words = text.split()
    return [" ".join(words[start:start + chunk_size]) for start in range(0, len(words), chunk_size)]


def split_with_overlap(text, chunk_size, overlap):
    """Split text into word-based chunks while repeating an overlap."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be non-negative and smaller than chunk_size")

    words = text.split()
    step = chunk_size - overlap
    return [" ".join(words[start:start + chunk_size]) for start in range(0, len(words), step)]


if __name__ == "__main__":
    sample = " ".join(f"word-{number}" for number in range(1, 501))
    print(f"Original Characters: {len(sample)}")
    for size in (50, 100, 200, 500):
        chunks = split_into_chunks(sample, size)
        print(f"\nChunk size: {size} words")
        print(f"Number of Chunks: {len(chunks)}")
        for number, chunk in enumerate(chunks[:3], start=1):
            print(f"Chunk {number}: {chunk[:120]}...")

    chunks = split_with_overlap(sample, chunk_size=200, overlap=50)
    print(f"\nWith overlap: {len(chunks)} chunks")
    print(f"Chunk 1 ends with: {chunks[0].split()[-1]}")
    print(f"Chunk 2 starts with: {chunks[1].split()[0]}")
