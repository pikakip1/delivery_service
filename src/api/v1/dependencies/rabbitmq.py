from aio_pika import connect_robust, Channel, ExchangeType
from typing import Optional
from src.core.config import settings

rabbit_channel: Optional[Channel] = None


async def init_rabbit() -> None:
    global rabbit_channel
    connection = await connect_robust(str(settings.rabbitmq.RABBITMQ_URL))
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)

    exchange = await channel.declare_exchange(
        "shipments", ExchangeType.DIRECT, durable=True
    )
    queue = await channel.declare_queue(
        "shipments.register",
        durable=True,
    )
    await queue.bind(exchange, routing_key="register")

    rabbit_channel = channel


async def close_rabbit() -> None:
    global rabbit_channel
    if rabbit_channel:
        await rabbit_channel.close()
        rabbit_channel = None


def get_rabbit_channel() -> Channel:
    if not rabbit_channel:
        raise RuntimeError("RabbitMQ channel is not initialized")
    return rabbit_channel
