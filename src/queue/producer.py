import json
from typing import Any

import aio_pika

from src.logger import logger

from .connection import RabbitMQConnection


class RabbitMQProducer:
    def __init__(self, connection: RabbitMQConnection):
        self.connection = connection

    async def send_message(self, exchange_name: str, routing_key: str, message: dict[str, Any]):
        if not self.connection.channel:
            await self.connection.connect()

        if self.connection.channel is None:
            raise RuntimeError("Channel was not initialized after connection")

        exchange = await self.connection.channel.declare_exchange(
            exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
        )

        body = json.dumps(message).encode()

        await exchange.publish(
            aio_pika.Message(body=body, delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
            routing_key=routing_key,
        )

        logger.info(f"OUT: routing_key={routing_key}, exchange={exchange_name}")


async def send_message(exchange_name: str, routing_key: str, message: dict[str, Any]):
    connection = RabbitMQConnection()
    await connection.connect()

    producer = RabbitMQProducer(connection)
    await producer.send_message(exchange_name=exchange_name, routing_key=routing_key, message=message)

    await connection.close()
