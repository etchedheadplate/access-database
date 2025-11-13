from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists  # type: ignore

from src.config import Settings
from src.logger import logger

settings = Settings()  # type: ignore[call-arg]

DATABASE_URL = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URL)


def create_db():
    if not database_exists(engine.url):
        create_database(engine.url)
        logger.info(f"Database {settings.DB_NAME} created")
    else:
        logger.info(f"Database {settings.DB_NAME} exists")


if __name__ == "__main__":
    create_db()
