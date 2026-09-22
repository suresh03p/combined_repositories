import re

SENSITIVE_PATTERNS = (r"FAKE_API_KEY_[A-Z0-9]+", r"FAKE_PASSWORD_[A-Z0-9]+", r"Bearer\s+\S+")

def contains_sensitive_data(text: str) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in SENSITIVE_PATTERNS)

def redact_sensitive_data(text: str) -> str:
    for pattern in SENSITIVE_PATTERNS:
        text = re.sub(pattern, "[REDACTED]", text, flags=re.IGNORECASE)
    return text
