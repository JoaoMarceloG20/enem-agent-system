
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # PostgreSQL
    postgres_user: str = os.getenv("POSTGRES_USER")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD")
    postgres_db: str = os.getenv("POSTGRES_DB")
    postgres_host: str = os.getenv("POSTGRES_HOST")
    postgres_port: int = int(os.getenv("POSTGRES_PORT"))

    # Qdrant
    qdrant_host: str = os.getenv("QDRANT_HOST")
    qdrant_port: int = int(os.getenv("QDRANT_PORT"))

    # Redis
    redis_host: str = os.getenv("REDIS_HOST")
    redis_port: int = int(os.getenv("REDIS_PORT"))

    # Gemini API Key
    gemini_api_key: str = os.getenv("GEMINI_API_KEY")

    class Config:
        env_file = ".env"

settings = Settings()
