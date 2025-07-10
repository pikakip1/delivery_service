from aiohttp import ClientSession
from redis.asyncio import Redis

from src.services.redis import RedisRepo

USD_RATE_KEY = "usd_rate"
URL_CBR_DAILY = "https://www.cbr-xml-daily.ru/daily_json.js"


async def get_dollar_rate(
    redis: Redis, redis_repo: RedisRepo, session_id: str
) -> float:
    usd_rate = await redis_repo.read(
        redis_client=redis, prefix=USD_RATE_KEY, session_id=session_id
    )
    if not usd_rate:
        usd_rate = await fetch_usd_rate_from_cbr()
        await redis_repo.create(
            redis_client=redis,
            prefix=USD_RATE_KEY,
            session_id=session_id,
            value=str(usd_rate),
        )
    return float(usd_rate)


async def fetch_usd_rate_from_cbr() -> float:
    async with ClientSession() as session:
        async with session.get(URL_CBR_DAILY) as resp:
            data = await resp.json(content_type=None)
            return float(data["Valute"]["USD"]["Value"])


def calculate_shipping_cost(weight: float, cost: float, dollar_rate: float) -> float:
    return round(int(weight) * 0.5 + (cost * dollar_rate * 0.01), 2)
