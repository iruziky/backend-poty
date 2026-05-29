from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql+asyncpg://poty:poty@db:5432/poty"

    @field_validator("DATABASE_URL")
    @classmethod
    def _ensure_asyncpg(cls, v: str) -> str:
        # Render/Heroku expõem como "postgres://" ou "postgresql://".
        # SQLAlchemy async exige driver explícito.
        if v.startswith("postgres://"):
            v = "postgresql://" + v[len("postgres://") :]
        if v.startswith("postgresql://") and "+asyncpg" not in v:
            v = "postgresql+asyncpg://" + v[len("postgresql://") :]
        return v
    JWT_SECRET: str = "changeme"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_DAYS: int = 7

    OPENROUTER_API_KEY: str = ""
    OPENROUTER_MODEL: str = "openai/gpt-4o-mini"
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    CORS_ORIGINS: str = "*"


settings = Settings()
