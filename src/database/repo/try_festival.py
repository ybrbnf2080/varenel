from typing import List

import asyncpg
from sqlalchemy import delete, exc, select, update

from src.database.models.try_festival import (
    TryFestivalDatabase,
)
from src.lib.enums import OffsetType
from src.lib.errors.base import NotFoundError
from src.lib.models import TryFestival
from src.lib.pagination import (
    add_pagination,
    normalize_data,
)

from .base import BaseDBRepo


class TryFestivalRepository(BaseDBRepo):
    async def create(self, dto: TryFestival) -> TryFestival:
        """Create new try_festival."""
        try_festival = TryFestivalDatabase(
            participant_number=dto.participant_number,
            track=dto.track,
            result=dto.result,
            time=dto.time,
        )
        try:
            self._session.add(try_festival)
            await self._session.commit()
            await self._session.refresh(try_festival)

        except exc.IntegrityError as exception:
            if isinstance(
                exception.orig.__context__, asyncpg.exceptions.ForeignKeyViolationError
            ):
                raise NotFoundError(
                    message=f"Forgein key error: '{exception.orig.__context__.detail}'"
                )
            raise exception
        return self.orm_to_dto(try_festival)

    async def get(self, try_festival_id: int) -> TryFestival:
        """Get try_festival by order_id."""
        query = select(TryFestivalDatabase).where(
            TryFestivalDatabase.id == try_festival_id,
        )
        result = await self._session.execute(query)
        try_festival = result.scalar_one_or_none()
        if not try_festival:
            raise NotFoundError(f"TryFestival for number {try_festival_id} not found")
        return self.orm_to_dto(try_festival)

    async def get_best_result_from_participant_id(
        self, participant_id: int
    ) -> List[TryFestival]:
        """Get all try_festivals."""
        query = (
            select(TryFestivalDatabase)
            .where(TryFestivalDatabase.participant_number == participant_id)
            .order_by(
                TryFestivalDatabase.track,
                TryFestivalDatabase.time,
                TryFestivalDatabase.result.desc(),
            )
            .distinct(TryFestivalDatabase.track)
        )
        result = await self._session.execute(query)
        try_festivals: List[TryFestivalDatabase] = result.scalars().all()
        return [self.orm_to_dto(try_festival) for try_festival in try_festivals]

    async def get_all(
        self, offset_type: OffsetType, offset_id: int = 0, limit: int = 10
    ) -> List[TryFestival]:
        """Get all try_festivals."""
        query = select(TryFestivalDatabase)

        statement = add_pagination(
            query=query,
            model=TryFestivalDatabase,
            offset_type=offset_type,
            offset_id=offset_id,
            limit=limit,
        )

        result = await self._session.execute(statement)
        try_festivals: List[TryFestivalDatabase] = result.scalars().all()
        return normalize_data(
            [self.orm_to_dto(try_festival) for try_festival in try_festivals],
            offset_type=offset_type,
        )

    async def delete(self, try_id: int) -> None:
        """Delete photo by id. Raise error if photo is not found."""
        statement = (
            delete(TryFestivalDatabase)
            .where(TryFestivalDatabase.id == try_id)
            .returning(TryFestivalDatabase)
        )

        result = await self._session.execute(statement)

        if not result.first():
            raise NotFoundError(f"Try not found")

        await self._session.commit()

    @staticmethod
    def orm_to_dto(orm_model: TryFestivalDatabase) -> TryFestival:
        return TryFestival.from_orm(orm_model)
