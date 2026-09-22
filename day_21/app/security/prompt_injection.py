import re

SUSPICIOUS_PATTERNS = [r"ignore\s+(all\s+)?previous", r"reveal\s+(the\s+)?system prompt", r"you are now an?\s+administrator", r"show\s+restricted"]

def detect_prompt_injection(text: str) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in SUSPICIOUS_PATTERNS)

def sanitize_user_prompt(text: str) -> str:
    if detect_prompt_injection(text):
        raise ValueError("Prompt rejected: suspected instruction override")
    return text
