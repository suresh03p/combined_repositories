from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Production AI Assistant"
    app_env: str = "development"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./production_ai.db"
    redis_url: str = "redis://localhost:6379/0"
    llm_api_key: str = ""
    vector_db_url: str = ""
    cache_ttl: int = 300
    ai_timeout: float = 10.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
