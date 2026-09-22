class AIServiceError(Exception):
    """Safe application error for model, retrieval, cache, or worker failures."""


class ResourceNotFoundError(Exception):
    """Raised when a requested resource does not exist."""
