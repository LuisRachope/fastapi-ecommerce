from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações globais da aplicação"""

    # API
    API_TITLE: str = "E-commerce API"
    API_VERSION: str = "0.1.0"
    API_DESCRIPTION: str = "API de E-commerce "
    DOCS_URL: str = "/ui"
    REDOC_URL: str | None = None

    # Ambiente
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite:///./ecommerce.db"

    # CORS
    ALLOWED_ORIGINS: list[str] = ["http://localhost:8080"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
