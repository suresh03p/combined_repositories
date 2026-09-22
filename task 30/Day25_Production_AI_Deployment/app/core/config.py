from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    app_name: str = "production-ai-api"
    app_port: int = 8000
    database_url: str = ""
    redis_url: str = ""
    llm_api_key: str = ""
    embedding_model: str = "local-hash"
    vector_db_path: str = "./data/vectors.json"
    log_level: str = "INFO"
    max_request_size: int = Field(default=1_048_576, ge=1)
    request_timeout: float = Field(default=30.0, gt=0)
    auth_username: str = "admin"
    auth_password: str = "change-me"
    jwt_secret: str = "change-this-in-production"

    @property
    def ai_configured(self) -> bool:
        return bool(self.llm_api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()
