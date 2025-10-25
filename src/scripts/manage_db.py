from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database  # type: ignore

from src.database.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from src.logger import logger

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)


def create_db():
    if not database_exists(engine.url):
        create_database(engine.url)
        logger.info(f"Database {DB_NAME} created.")
    else:
        logger.info(f"Database {DB_NAME} exists.")


def drop_db():
    if database_exists(engine.url):
        drop_database(engine.url)
        logger.info(f"Database {DB_NAME} dropped.")
    else:
        logger.info(f"Database {DB_NAME} doesn't exist.")
