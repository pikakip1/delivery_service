from fastapi import HTTPException
from redis.asyncio import Redis
from src.core.config import settings

redis: Redis | None = None

async def init_redis_pool() -> None:
    global redis
    redis = Redis.from_url(
        settings.redis.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
        max_connections=20,
    )

async def close_redis_pool() -> None:
    if redis:
        await redis.close()
        
        
async def get_redis() -> Redis:
    if not redis:
        raise HTTPException(500, "Redis pool is not initialized")
    return redis