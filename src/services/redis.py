import uuid
from functools import lru_cache

from redis.asyncio import Redis

from src.core.config import settings


class RedisRepo:
    async def create(
        self,
        redis_client: Redis,
        prefix: str,
        session_id: str,
        value: str,
        expires_time: int | None = settings.redis.expire,
    ) -> None:
        session_key = f"{prefix}:{session_id}"
        await redis_client.set(
            session_key,
            value=value,
            ex=expires_time,
        )

    async def read(
        self, redis_client: Redis, prefix: str, session_id: str
    ) -> str | None:
        session_key = f"{prefix}:{session_id}"
        return await redis_client.get(
            session_key,
        )

    async def exists(
        self,
        redis_client: Redis,
        prefix: str,
        session_id: uuid.UUID,
    ) -> bool:
        session_key = f"{prefix}:{session_id}"
        return bool(await redis_client.exists(session_key))


@lru_cache
def get_redis_repo() -> RedisRepo:
    return RedisRepo()
