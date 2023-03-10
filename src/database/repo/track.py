import logging
from typing import List

import asyncpg
from sqlalchemy import delete, exc, select, update

from src.database.models.track import TrackDatabase
from src.lib import enums
from src.lib.enums import OffsetType
from src.lib.errors.base import (
    AlreadyExistsError,
    NotFoundError,
)
from src.lib.models import Track
from src.lib.pagination import (
    add_pagination,
    normalize_data,
)

from .base import BaseDBRepo


logger = logging.getLogger(__name__)


class TrackRepository(BaseDBRepo):
    async def create(self, dto: Track) -> Track:
        """Create new track."""
        track = TrackDatabase(
            number=dto.number,
            color=dto.color,
            group=dto.group,
        )
        self._session.add(track)
        try:
            await self._session.commit()
        except exc.IntegrityError as exception:
            raise AlreadyExistsError(f"track for number {dto.number}")

        await self._session.refresh(track)

        return self.orm_to_dto(track)

    async def get(self, track_id: int) -> Track:
        """Get track by order_id."""
        query = select(TrackDatabase).where(
            TrackDatabase.number == track_id,
        )

        try:
            result = await self._session.execute(query)
            track = result.scalar_one_or_none()
        except Exception:
            raise NotFoundError(f"Track for number {track_id} not found")

        return self.orm_to_dto(track)

    async def get_all_from_group(self, group: enums.Group) -> List[Track]:
        """Get all tracks."""
        query = select(TrackDatabase).where(TrackDatabase.group == group)

        result = await self._session.execute(query)
        tracks: List[TrackDatabase] = result.scalars().all()
        return [self.orm_to_dto(track) for track in tracks]

    async def get_all(
        self, offset_type: OffsetType, offset_id: int = 0, limit: int = 10
    ) -> List[Track]:
        """Get all tracks."""
        query = select(TrackDatabase)

        statement = add_pagination(
            query=query,
            model=TrackDatabase,
            offset_type=offset_type,
            offset_id=offset_id,
            limit=limit,
        )

        result = await self._session.execute(statement)
        tracks: List[TrackDatabase] = result.scalars().all()
        return normalize_data(
            [self.orm_to_dto(track) for track in tracks],
            offset_type=offset_type,
        )

    async def delete(self, number: int) -> None:
        """Delete track by id. Raise error if track is not found."""
        statement = (
            delete(TrackDatabase)
            .where(TrackDatabase.number == number)
            .returning(TrackDatabase)
        )

        result = await self._session.execute(statement)

        if not result.first():
            raise NotFoundError(f"Track not found")

        await self._session.commit()

    @staticmethod
    def orm_to_dto(orm_model: TrackDatabase) -> Track:
        return Track.from_orm(orm_model)
