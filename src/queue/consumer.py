import json
from collections.abc import Awaitable, Callable
from typing import Any

import aio_pika

from src.logger import logger

from .connection import RabbitMQConnection


class RabbitMQConsumer:
    def __init__(self, connection: RabbitMQConnection):
        self.connection = connection

    async def consume(self, exchange_name: str, routing_key: str, callback: Callable[[Any], Awaitable[None]]):
        if not self.connection.channel:
            await self.connection.connect()

        if self.connection.channel is None:
            raise RuntimeError("Channel was not initialized after connection")

        exchange = await self.connection.channel.declare_exchange(
            exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
        )

        queue = await self.connection.channel.declare_queue("", exclusive=True)

        await queue.bind(exchange, routing_key)

        logger.info(f"Subscribed to exchange={exchange_name}, topic={routing_key}")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    payload = json.loads(message.body)
                    await callback(payload)
