from typing import List

from pydantic_settings import BaseSettings


# самостоятельно подключается к .env
class Settings(BaseSettings):
    BIND_IP: str
    BIND_PORT: int
    DB_URL: str

    JWT_SECRET_SALT: str
    KAFKA_BOOTSTRAP_SERVERS: List[str]
    KAFKA_TOPIC: str

    API_PREFIX: str = "/api"


settings = Settings()
