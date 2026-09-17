from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_VERSION: str = ""
    APP_NAME: str = ""
    DESCRIPTION: str = ""

    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/currency_db"
    )
    DATABASE_URL_SYNC: str = (
        "postgresql+psycopg2://postgres:postgres@localhost:5432/currency_db"
    )

    SECRET_KEY: str = "change-me-in-production-supersecretkey"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1
    ALGORITHM: str = "HS256"


settings = Settings()
