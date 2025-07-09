from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from src.schemas.parcel import ParcelOut
from src.api.v1.dependencies.redis import get_redis
from src.api.v1.dependencies.repository import get_repository
from src.repository.parcel import ParcelRepo
from src.utils.session import get_session_id


router = APIRouter(prefix="/parcel", tags=["course"])

@router.get("/", name="parcels:get", summary='Получить список посылок')
async def list_parcels(
    session_id: str = Depends(get_session_id),
    course_repo: ParcelRepo = Depends(get_repository(ParcelRepo)),
    redis: Redis = Depends(get_redis),
) -> list[ParcelOut]:
    parcels = await course_repo.list_parcel()
    return parcels