from databases import Database
from sqlalchemy import MetaData
from app.config import settings
import os

metadata = MetaData()

def get_database_url():
    if settings.DATABASE_TYPE == "postgres":
        return f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    else:
        # Ensures that the data directory exists
        os.makedirs("data", exist_ok=True)
        return f"sqlite:///data/{settings.SQLITE_DB_NAME}"

DATABASE_URL = get_database_url()
database = Database(DATABASE_URL)

def get_database():
    return database
