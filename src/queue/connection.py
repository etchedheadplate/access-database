import aio_pika
from aio_pika.abc import AbstractChannel, AbstractRobustConnection

from src.config import Settings


class RabbitMQConnection:
    def __init__(self):
        settings = Settings()  # type: ignore[call-arg]
        self.host = settings.RABBITMQ_HOST
        self.port = settings.RABBITMQ_PORT
        self.user = settings.RABBITMQ_USER
        self.password = settings.RABBITMQ_PASSWORD
        self.vhost = settings.RABBITMQ_VHOST
        self.url = f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/{self.vhost}"
        self.__connection: AbstractRobustConnection | None = None
        self.__channel: AbstractChannel | None = None

    async def connect(self):
        self.__connection = await aio_pika.connect_robust(self.url)
        self.__channel = await self.__connection.channel()
        await self.__channel.set_qos(prefetch_count=1)

    async def close(self):
        if self.__channel and not self.__channel.is_closed:
            await self.__channel.close()
        if self.__connection and not self.__connection.is_closed:
            await self.__connection.close()
