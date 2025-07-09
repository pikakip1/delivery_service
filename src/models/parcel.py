import sqlalchemy as sa
import sqlalchemy.orm as so

from src.models.db import Base
from src.utils.common import ParcelType


class Parcel(Base):
    __tablename__ = 'parcels'

    name: so.Mapped[str] = so.mapped_column(sa.String(100), nullable=False, index=True)
    weight: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    type_parcel: so.Mapped[ParcelType] = so.mapped_column(sa.Enum(ParcelType), nullable=False)
    cost: so.Mapped[float] = so.mapped_column(sa.Float, nullable=False)
    
    

