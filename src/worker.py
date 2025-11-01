import asyncio
from typing import Any

from src.logger import logger
from src.queue import (
    EXCHANGE_NAME,
    ROUTING_KEY_STATUS,
    ROUTING_KEY_TASK,
    send_message,
)
from src.services.status.processor import StatusProcessor
from src.services.task.executors import get_task_executor

message_buffer: dict[str, dict[str, Any]] = {}
buffer_lock = asyncio.Lock()


async def process_pair(task_message: dict[str, Any], status_message: dict[str, Any]):
    status = StatusProcessor(status_message)
    task = get_task_executor(task_message)

    if status.is_appropriate and status.request_id == task.request_id:
        await task.execute()
        message_out = await status.process(task.is_done, task.result)
        await send_message(EXCHANGE_NAME, ROUTING_KEY_STATUS, message_out.model_dump())
        logger.info(f"{message_out}")
        logger.info(f"OUT: request_id={message_out.request_id}, request_status={message_out.request_status}")


def is_status_message(msg: dict[str, Any]) -> bool:
    return "request_status" in msg


def is_task_message(msg: dict[str, Any]) -> bool:
    return "request_type" in msg


async def handle_message(message: dict[str, Any], routing_key: str):
    if routing_key in (ROUTING_KEY_TASK, ROUTING_KEY_STATUS):
        logger.info(f" IN: request_id={message['request_id']}, routing_key={routing_key}")

    request_id = message.get("request_id")
    if not request_id:
        return

    async with buffer_lock:
        if request_id not in message_buffer:
            message_buffer[request_id] = {}

        if routing_key == ROUTING_KEY_TASK:
            message_buffer[request_id]["task"] = message
        elif routing_key == ROUTING_KEY_STATUS:
            message_buffer[request_id]["status"] = message

        entry = message_buffer[request_id]
        if "task" in entry and "status" in entry:
            task_message = entry["task"]
            status_message = entry["status"]

            if is_status_message(task_message) and is_task_message(status_message):
                task_message, status_message = status_message, task_message

            del message_buffer[request_id]

            asyncio.create_task(process_pair(task_message, status_message))
