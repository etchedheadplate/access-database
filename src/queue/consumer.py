import json
from collections.abc import Awaitable, Callable
from typing import Any

import aio_pika

from src.logger import logger

from .config import SERVICE_NAME
from .connection import RabbitMQConnection


class RabbitMQConsumer:
    def __init__(self, connection: RabbitMQConnection):
        self.connection = connection
        self.service_name = SERVICE_NAME

    async def consume(self, exchange_name: str, routing_key: str, callback: Callable[[Any], Awaitable[None]]):
        if not self.connection.channel:
            await self.connection.connect()

        if self.connection.channel is None:
            raise RuntimeError("Channel was not initialized after connection")

        exchange = await self.connection.channel.declare_exchange(
            exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
        )

        queue_name = f"{exchange_name}_{self.service_name}"
        queue = await self.connection.channel.declare_queue(queue_name, durable=True)
        await queue.bind(exchange, routing_key)

        await queue.bind(exchange, routing_key)

        logger.info(f"SUB: exchange={exchange_name}, queue={queue}, topic={routing_key}")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    payload = json.loads(message.body)
                    await callback(payload)
