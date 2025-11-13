from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, drop_database  # type: ignore

from src.config import Settings
from src.logger import logger

settings = Settings()  # type: ignore[call-arg]

DATABASE_URL = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URL)


def drop_db():
    if database_exists(engine.url):
        drop_database(engine.url)
        logger.info(f"Database {settings.DB_NAME} dropped")
    else:
        logger.info(f"Database {settings.DB_NAME} doesn't exist")


if __name__ == "__main__":
    drop_db()
