import logging
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


# WORKER_LOG_DEFAULT_FORMAT = (
    # тут докидываем имя процесса - там будет имя и номер воркера
#     "[%(asctime)s.%(msecs)03d] [%(processName)s] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
# )


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8001


# class GunicornConfig(BaseModel):
#     host: str = "0.0.0.0"
#     port: int = 8000
#     workers: int = 1
#     timeout: int = 900


class LoggingConfig(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT
    log_date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    users: str = "/users"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


# class TaskiqConfig(BaseModel):
#     url: AmqpDsn = "amqp://guest:guest@localhost:5672//"
#     log_format: str = WORKER_LOG_DEFAULT_FORMAT


class DatabaseConfig(BaseModel):
    name: str
    password: str
    host: str
    port: int
    user: str
    
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
    
    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    model_config = SettingsConfigDict(env_file=".env")


class RedisConfig(BaseModel):
    host: str = "redis"
    port: int = 6379
    db: int = 0
    password: str | None = None

    @property
    def REDIS_URL(self) -> str:
        # auth = self.password if self.password else ""
        return f"redis://{self.host}:{self.port}/{self.db}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    run: RunConfig = RunConfig()
    # gunicorn: GunicornConfig = GunicornConfig()
    logging: LoggingConfig = LoggingConfig()
    api: ApiPrefix = ApiPrefix()
    # taskiq: TaskiqConfig = TaskiqConfig()
    db: DatabaseConfig
    redis: RedisConfig
    session_secret_key: str = "SECRET_KEY"


settings = Settings()
