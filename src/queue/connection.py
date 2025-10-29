import aio_pika
from aio_pika.abc import AbstractChannel, AbstractRobustConnection
from dotenv import load_dotenv

from src.logger import logger

from .config import RABBITMQ_HOST, RABBITMQ_PASSWORD, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_VHOST

load_dotenv()


class RabbitMQConnection:
    def __init__(self):
        self.host = RABBITMQ_HOST
        self.port = RABBITMQ_PORT
        self.user = RABBITMQ_USER
        self.password = RABBITMQ_PASSWORD
        self.vhost = RABBITMQ_VHOST
        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractChannel | None = None

    async def connect(self):
        url = f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.vhost}"
        self.connection = await aio_pika.connect_robust(url)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)
        logger.info("Connected to RabbitMQ")

    async def close(self):
        if self.channel and not self.channel.is_closed:
            await self.channel.close()
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
        logger.info("Disconnected from RabbitMQ")
