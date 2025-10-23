from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.database.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

ASYNC_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async_engine = create_async_engine(ASYNC_DATABASE_URL, pool_pre_ping=True)

async_session_maker = async_sessionmaker(bind=async_engine, expire_on_commit=False)
