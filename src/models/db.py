import uuid
from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so
import uuid6
from sqlalchemy.orm import DeclarativeBase

from src.core.config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        sa.UUID(as_uuid=True),
        primary_key=True,
        default=uuid6.uuid7,
    )
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )
    is_deleted: so.Mapped[bool] = so.mapped_column(
        sa.BOOLEAN, default=False, server_default=sa.text("false")
    )

    metadata = sa.MetaData(
        naming_convention=settings.db.naming_convention,
    )
