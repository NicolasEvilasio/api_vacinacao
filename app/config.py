"""
Application settings.

This module contains the global application settings.
It is responsible for:
- Configuring logging
- Defining global constants
- Configuring rate limiting
- Managing environment variables

Centralizes all settings that can be reused in
different parts of the application.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address
import logging
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # Configuração do banco de dados
    DATABASE_TYPE: str = os.getenv("DATABASE_TYPE", "sqlite")  # "sqlite" ou "postgres"
    
    # Configurações PostgreSQL
    DB_USERNAME: str = os.getenv("DB_USERNAME", "")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "")
    DB_PORT: int = int(os.getenv("DB_PORT", "5432"))
    DB_NAME: str = os.getenv("DB_NAME", "")
    
    # Configuração SQLite
    SQLITE_DB_NAME: str = os.getenv("SQLITE_DB_NAME", "database.db")

    # Configuração de URLs
    PRODUCTION_URL: str = os.getenv("PRODUCTION_URL", "")

    class Config:
        env_file = ".env"

settings = Settings()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rate Limiter
limiter = Limiter(key_func=get_remote_address) 