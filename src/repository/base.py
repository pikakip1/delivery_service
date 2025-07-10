from typing import Generic, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.db import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model_cls: type[T]):
        self.session = session
        self.model_cls = model_cls
