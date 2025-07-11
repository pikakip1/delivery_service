import json
import aio_pika
from src.schemas.parcel import ParcelCreate, ParcelOut
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
    
    async def add_parcel(
        self,
        session_id: str,
        parcel: ParcelCreate,
        channel: aio_pika.Channel
    ):
        new_parcel = Parcel(
            name=parcel.name,
            weight=parcel.weight,
            type_parcel=parcel.type_parcel,
            cost=0, 
        )
        
        self.session.add(new_parcel)
        await self.session.commit()
        
        payload = {
            "parcel_id": str(new_parcel.id),
            "weight_kg": new_parcel.weight,
            "contents_usd": parcel.cost,
            "session_id": session_id,
        }
        
        exchange = await channel.declare_exchange("shipments", aio_pika.ExchangeType.DIRECT, durable=True)
        await exchange.publish(
            aio_pika.Message(body=json.dumps(payload).encode()),
            routing_key="register",
    )
        

    async def list_parcel(
        self,
    ) -> list[ParcelOut]:
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
                    cost=parcel.cost,
                )
            )
         
        return mapped_percels
    