from collections.abc import Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import db_helper
from src.repository.base import BaseRepository


def get_repository(
    repo_type: type[BaseRepository],
) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repo(
        session: AsyncSession = Depends(db_helper.session_getter),
    ) -> BaseRepository:
        return repo_type(session=session)  # type: ignore

    return _get_repo
