from app.database import check_database
from app.services.cache import cache_health


def health_report() -> dict[str, str]:
    return {
        "api": "healthy",
        "database": "healthy" if check_database() else "unhealthy",
        "redis": "healthy" if cache_health() else "unhealthy",
        "ai_service": "healthy",
    }
