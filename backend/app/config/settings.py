from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str = "MargDarshak API"
    VERSION: str = "0.1.0"
    DEBUG: bool = True

    # Postgres
    POSTGRES_USER: str = "margdarshak"
    POSTGRES_PASSWORD: str = "margdarshak_secret"
    POSTGRES_DB: str = "margdarshak_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"

    @property
    def async_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # Qdrant
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333

    # LLM
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings():
    return Settings()
