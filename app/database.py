from databases import Database
from sqlalchemy import MetaData
import os

def get_env_or_fail(key: str) -> str:
    environment = os.environ.get("ENVIRONMENT", "production")
    prefix = "STAGING_" if environment == "staging" else ""
    
    value = os.environ.get(f"{prefix}{key}")
    if value is None:
        raise ValueError(f"Variável de ambiente {prefix}{key} não configurada")
    return value

# Obter variáveis do GitHub Actions
DB_USERNAME = get_env_or_fail("DB_USERNAME")
DB_PASSWORD = get_env_or_fail("DB_PASSWORD")
DB_HOST = get_env_or_fail("DB_HOST")
DB_PORT = get_env_or_fail("DB_PORT")
DB_NAME = get_env_or_fail("DB_NAME")

metadata = MetaData()

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
database = Database(DATABASE_URL)

def get_database():
    return database
