import asyncio
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from src.api.access.routes import router as access_router
from src.api.auth.routes import router as auth_router
from src.api.database.routes import router as database_router
from src.api.health.routes import router as health_router
from src.logger import logger
from src.queue import (
    EXCHANGE_NAME,
    ROUTING_KEY_STATUS,
    ROUTING_KEY_TASK,
    RabbitMQConnection,
    RabbitMQConsumer,
    RabbitMQProducer,
)

rabbit_connection = RabbitMQConnection()
producer = RabbitMQProducer(rabbit_connection)
consumer = RabbitMQConsumer(rabbit_connection)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_connection.connect()

    async def handle_message(msg: dict[str, Any]):
        logger.info(f"Message received: {msg}")

    asyncio.create_task(consumer.consume(EXCHANGE_NAME, ROUTING_KEY_TASK, handle_message))
    asyncio.create_task(consumer.consume(EXCHANGE_NAME, ROUTING_KEY_STATUS, handle_message))

    yield

    await rabbit_connection.close()


app = FastAPI(lifespan=lifespan)

app.include_router(health_router, tags=["Health"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(database_router, prefix="/database", tags=["Database"])
app.include_router(access_router, prefix="/access", tags=["Access"])
