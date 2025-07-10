import logging
import aio_pika
from fastapi import APIRouter, Depends
from src.api.v1.dependencies.rabbitmq import get_rabbit_channel
from src.schemas.parcel import ParcelCreate, ParcelOut
from src.api.v1.dependencies.repository import get_repository
from src.repository.parcel import ParcelRepo
from src.utils.session import get_session_id


router = APIRouter(prefix="/parcel", tags=["parcel"])


@router.post("/", name="parcels:post", summary="Добавить посылку")
async def add_parcel(
    parcel: ParcelCreate,
    session_id: str = Depends(get_session_id),
    parcel_repo: ParcelRepo = Depends(get_repository(ParcelRepo)),
    channel: aio_pika.Channel = Depends(get_rabbit_channel),
) -> None:
    await parcel_repo.add_parcel(session_id=session_id, parcel=parcel, channel=channel)


@router.get("/", name="parcels:get", summary="Получить список посылок")
async def list_parcels(
    parcel_repo: ParcelRepo = Depends(get_repository(ParcelRepo)),
) -> list[ParcelOut]:
    parcels = await parcel_repo.list_parcel()
    return parcels
