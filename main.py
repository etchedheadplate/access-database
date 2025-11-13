import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.access.routes import router as access_router
from src.api.auth.routes import router as auth_router
from src.api.database.routes import router as database_router
from src.api.health.routes import router as health_router
from src.config import Settings
from src.logger import logger
from src.queue import (
    RabbitMQConnection,
    RabbitMQConsumer,
    RabbitMQProducer,
)
from src.worker import handle_message

settings = Settings()  # type: ignore[call-arg]
rabbit_connection = RabbitMQConnection()
producer = RabbitMQProducer(rabbit_connection)
consumer = RabbitMQConsumer(rabbit_connection)
exchange = settings.EXCHANGE_NAME
task_routing_key = settings.ROUTING_KEY_TASK
status_routing_key = settings.ROUTING_KEY_STATUS_VALIDATED


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_connection.connect()
    logger.info("Connected to RabbitMQ")

    asyncio.create_task(consumer.consume(exchange, task_routing_key, lambda msg: handle_message(msg, task_routing_key)))
    asyncio.create_task(
        consumer.consume(exchange, status_routing_key, lambda msg: handle_message(msg, status_routing_key))
    )

    yield

    await rabbit_connection.close()
    logger.info("Disconnected from RabbitMQ")


app = FastAPI(lifespan=lifespan)

app.include_router(health_router, tags=["Health"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(database_router, prefix="/database", tags=["Database"])
app.include_router(access_router, prefix="/access", tags=["Access"])
