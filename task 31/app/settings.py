from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    log_level: str = "INFO"
    redis_url: str = "redis://localhost:6379/0"
    database_url: str = "postgresql://localhost/ai_api"
    llm_api_key: str = ""
    llm_model: str = "configured-model"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
