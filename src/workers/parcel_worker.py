import asyncio
import json
from typing import Optional

from aio_pika import IncomingMessage, Channel
from redis.asyncio import Redis

from src.api.v1.dependencies.rabbitmq import (
    close_rabbit,
    get_rabbit_channel,
    init_rabbit,
)
from src.api.v1.dependencies.redis import close_redis_pool, get_redis, init_redis_pool
from src.services.redis import RedisRepo, get_redis_repo
from src.core.db import db_helper

from src.models.parcel import Parcel
from src.utils.parcel import calculate_shipping_cost, get_dollar_rate


redis_client: Optional[Redis] = None
redis_repo: Optional[RedisRepo] = None
rabbit_channel: Optional[Channel] = None


async def init_resources():
    global redis_client, redis_repo, rabbit_channel

    await init_redis_pool()
    redis_client = await get_redis()
    redis_repo = get_redis_repo()

    await init_rabbit()
    rabbit_channel = get_rabbit_channel()


async def handle_message(message: IncomingMessage):
    async with message.process():
        data = json.loads(message.body)
        pid = data["parcel_id"]
        weight = data["weight_kg"]
        contents_usd = data["contents_usd"]
        session_id = data.get("session_id")

        rate = await get_dollar_rate(
            redis=redis_client,
            redis_repo=redis_repo,
            session_id=session_id,
        )

        cost = calculate_shipping_cost(
            weight=weight,
            cost=contents_usd,
            dollar_rate=rate,
        )

        async with db_helper.session_factory() as session:
            parcel = await session.get(Parcel, pid)
            if parcel:
                parcel.cost = cost
                await session.commit()


async def main():
    try:
        await init_resources()
        queue = await rabbit_channel.declare_queue("shipments.register", durable=True)

        await queue.consume(handle_message)
        await asyncio.Future()
    finally:
        await close_rabbit()
        await close_redis_pool()


if __name__ == "__main__":
    asyncio.run(main())
