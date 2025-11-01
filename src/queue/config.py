import os

from dotenv import load_dotenv

load_dotenv()

SERVICE_NAME = os.getenv("SERVICE_NAME", "Database")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", 5672))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/")

EXCHANGE_NAME = os.getenv("EXCHANGE_NAME", "access")
ROUTING_KEY_TASK = os.getenv("ROUTING_KEY_TASK", "request.task")
ROUTING_KEY_STATUS = os.getenv("ROUTING_KEY_STATUS", "request.status")
