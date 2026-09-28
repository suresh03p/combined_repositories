import re

_STOP_WORDS = {
    "a", "about", "an", "and", "are", "as", "at", "be", "by", "does",
    "for", "from", "how", "i", "in", "into", "is", "it", "of", "on",
    "or", "that", "the", "this", "to", "was", "what", "when", "with",
}


def keywords(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in _STOP_WORDS and len(token) > 1
    }
