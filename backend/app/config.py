from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: str = "development"
    app_name: str = "PrimeHomes Lead Bot"
    debug: bool = True

    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/primehomes"

    ai_provider: str = "google"
    ai_model: str = ""
    ai_api_key: str = ""
    ai_temperature: float = 0.2
    ai_max_tokens: int = 1000

    n8n_base_url: str = "http://localhost:5678"
    n8n_webhook_url: str = "http://localhost:5678/webhook/primehomes/chat"
    n8n_webhook_secret: str = ""

    frontend_url: str = "http://localhost:5173"
    cors_origins: List[str] = ["http://localhost:5173"]

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Sales portal user (MVP single-user auth)
    sales_user_email: str = "sales@primehomes.ng"
    sales_user_password: str = "changeme123"
    sales_user_name: str = "Sales Manager"

    # Google Sheets (optional)
    google_sheets_credentials: str = ""
    google_sheets_id: str = ""

    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
