from src.schemas.parcel import ParcelOut
from src.models.parcel import Parcel
from src.repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy as sa

class ParcelRepo(BaseRepository[Parcel]):
    def __init__(
        self,
        session: AsyncSession,
) -> None:
        super().__init__(session=session, model_cls=Parcel)

    async def list_parcel(self) -> list[ParcelOut]:
        stmt = sa.select(self.model_cls)
        result_stmt = await self.session.execute(stmt)
        parcels = result_stmt.scalars()
        mapped_percels = []
        
        for parcel in parcels:
            mapped_percels.append(
                ParcelOut(
                    id=parcel.id,
                    name=parcel.name,
                    weight=parcel.weight,
                    type_parcel=parcel.type_parcel,
                    cost=parcel.cost
                )
            )
         
        return mapped_percels
    