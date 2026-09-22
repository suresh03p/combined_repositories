def validate_message(message: str, max_length: int = 4_000) -> str:
    value = message.strip()
    if not value:
        raise ValueError("Message cannot be empty")
    if len(value) > max_length:
        raise ValueError("Message is too long")
    return value
