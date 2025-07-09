import uuid

from src.schemas.base import BaseSchemaModel
from src.utils.common import ParcelType


class ParcelOut(BaseSchemaModel):
    id: uuid.UUID
    name: str
    weight: float
    type_parcel: ParcelType
    cost: float
