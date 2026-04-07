from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
  DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./movies.db")
  model_config = ConfigDict(env_file=".env")

settings = Settings()