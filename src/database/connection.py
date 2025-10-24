from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy_utils import create_database, database_exists  # type: ignore

from src.database.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from src.database.models import Base, User
from src.logger import logger

SYNC_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SYNC_DATABASE_URL)


def create_db():
    if not database_exists(engine.url):
        create_database(engine.url)
        logger.info(f"Database {DB_NAME} created.")
    else:
        logger.info(f"Database {DB_NAME} exists.")


ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async_engine = create_async_engine(ASYNC_DATABASE_URL)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
