from typing import List

import asyncpg
from sqlalchemy import delete, exc, select, update

from src.database.models.result_participant import (
    ResultParticipantDatabase,
)
from src.lib.enums import OffsetType
from src.lib.errors.base import (
    AlreadyExistsError,
    NotFoundError,
)
from src.lib.models import ResultParticipant
from src.lib.pagination import (
    add_pagination,
    normalize_data,
)

from .base import BaseDBRepo


class ResultParticipantRepository(BaseDBRepo):
    async def create(self, dto: ResultParticipant) -> ResultParticipant:
        """Create new result_participant."""
        result_participant = ResultParticipantDatabase(
            participant_number=dto.participant_number,
            point=dto.point,
        )
        self._session.add(result_participant)
        try:
            await self._session.commit()
            await self._session.refresh(result_participant)
        except exc.IntegrityError as exception:
            if isinstance(
                exception.orig.__context__, asyncpg.exceptions.ForeignKeyViolationError
            ):
                raise NotFoundError(
                    message=f"Forgein key error: '{exception.orig.__context__.detail}'"
                )
            raise exception

        return self.orm_to_dto(result_participant)

    async def get(self, result_participant_id: int) -> ResultParticipant:
        """Get result_participant by order_id."""
        query = select(ResultParticipantDatabase).where(
            ResultParticipantDatabase.id == result_participant_id,
        )

        try:
            result = await self._session.execute(query)
            result_participant = result.scalar_one_or_none()
        except exc.IntegrityError:
            raise NotFoundError(
                f"Participant for number {result_participant_id} not found"
            )

        return self.orm_to_dto(result_participant)

    async def get_all(
        self, offset_type: OffsetType, offset_id: int = 0, limit: int = 10
    ) -> List[ResultParticipant]:
        """Get all result_participant."""
        query = select(ResultParticipantDatabase)

        statement = add_pagination(
            query=query,
            model=ResultParticipantDatabase,
            offset_type=offset_type,
            offset_id=offset_id,
            limit=limit,
        )

        result = await self._session.execute(statement)
        result_participant: List[ResultParticipantDatabase] = result.scalars().all()
        return normalize_data(
            [
                self.orm_to_dto(result_participant)
                for result_participant in result_participant
            ],
            offset_type=offset_type,
        )

    @staticmethod
    def orm_to_dto(orm_model: ResultParticipantDatabase) -> ResultParticipant:
        return ResultParticipant.from_orm(orm_model)
