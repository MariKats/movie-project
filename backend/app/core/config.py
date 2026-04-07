from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./movies.db"
    OMDB_API_KEY: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


settings = Settings()
