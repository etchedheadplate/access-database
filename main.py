from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.auth.routes import auth_router
from src.database.connection import create_db, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
