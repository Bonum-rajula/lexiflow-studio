# src/core/config.py
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Load .env file

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    api_base_url: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

# Singleton instance
settings = Settings()