import hashlib
import math
import re
from collections import Counter

_cache: dict[str, list[float]] = {}

def document_hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()

def embed(text: str) -> list[float]:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    counts = Counter(tokens)
    vector = [0.0] * 64
    for token, count in counts.items():
        digest = hashlib.sha256(token.encode()).digest()
        index = int.from_bytes(digest[:2], "big") % len(vector)
        vector[index] += count
    magnitude = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / magnitude for value in vector]

def cached_embed(text: str) -> tuple[list[float], bool]:
    key = hashlib.sha256(text.encode()).hexdigest()
    if key in _cache:
        return _cache[key], True
    vector = embed(text)
    _cache[key] = vector
    return vector, False

def cosine_similarity(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))
