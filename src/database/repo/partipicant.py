import logging
from typing import List

import asyncpg
from sqlalchemy import delete, exc, select, update
from src.lib.errors.base import AlreadyExistsError, NotFoundError

from src.database.models.partipicant import (
    ParticipantDatabase,
)
from src.lib.enums import OffsetType
from src.lib.models import Participant
from src.lib.pagination import (
    add_pagination,
    normalize_data,
)

from .base import BaseDBRepo


logger = logging.getLogger(__name__)


class ParticipantRepository(BaseDBRepo):
    async def create(self, dto: Participant) -> Participant:
        """Create new participant."""
        participant = ParticipantDatabase(
            number=dto.number,
            surname=dto.surname,
            name=dto.name,
            patronymic=dto.patronymic,
            birthday=dto.birthday,
            rank=dto.rank,
            city=dto.city,
            team=dto.team,
            group=dto.group,
            couch=dto.couch,
        )
        self._session.add(participant)
        try:
            await self._session.commit()
        except exc.IntegrityError as exception:
            if isinstance(
                exception.orig.__context__, asyncpg.exceptions.UniqueViolationError
            ):
                await self._session.rollback()
                exist_user = await self._session.get(
                    ParticipantDatabase, ident=dto.number
                )
                if (
                    exist_user.name != participant.name
                    or exist_user.surname != participant.surname
                    or exist_user.team != participant.team
                ):
                    logger.warn(
                        f"User is Number {dto.number} already exists: \n"
                        f"  {exist_user.name} {exist_user.surname}, {exist_user.city}"
                        f"  ADD NEW USER TO END LIST!!!!!!"
                    )
                    raise AlreadyExistsError(f"Participant for number {participant.number} already exists.")

                logger.warn(
                    f"User '{dto.number} {dto.name} {dto.surname}' already exists in database"
                )

                return self.orm_to_dto(exist_user)

        await self._session.refresh(participant)

        return self.orm_to_dto(participant)

    async def get(self, participant_id: int) -> Participant:
        """Get participant by order_id."""
        query = select(ParticipantDatabase).where(
            ParticipantDatabase.number == participant_id,
        )

        try:
            result = await self._session.execute(query)
            participant = result.scalar_one_or_none()
        except Exception:
            raise NotFoundError(f"Participant for number {participant_id} not found")

        return self.orm_to_dto(participant)

    async def get_all(
        self, offset_type: OffsetType, offset_id: int = 0, limit: int = 10
    ) -> List[Participant]:
        """Get all participants."""
        query = select(ParticipantDatabase)

        statement = add_pagination(
            query=query,
            model=ParticipantDatabase,
            offset_type=offset_type,
            offset_id=offset_id,
            limit=limit,
        )

        result = await self._session.execute(statement)
        participants: List[ParticipantDatabase] = result.scalars().all()
        return normalize_data(
            [self.orm_to_dto(participant) for participant in participants],
            offset_type=offset_type,
        )

    @staticmethod
    def orm_to_dto(orm_model: ParticipantDatabase) -> Participant:
        return Participant.from_orm(orm_model)
