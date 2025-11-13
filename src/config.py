from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SERVICE_NAME: str

    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str

    JWT_SECRET: str

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_VHOST: str

    EXCHANGE_NAME: str
    ROUTING_KEY_TASK: str
    ROUTING_KEY_STATUS_VALIDATED: str
    ROUTING_KEY_STATUS_DONE: str
    ROUTING_KEY_STATUS_UNPROCESSABLE: str

    model_config = SettingsConfigDict(env_file=".env")
