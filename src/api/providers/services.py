from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.api.providers.dummies import get_session_factory
from src.database.repo import (
    ParticipantRepository,
    ResultParticipantRepository,
    TryFestivalRepository,
)


async def yield_db_session(
    session_factory: sessionmaker = Depends(get_session_factory),
) -> AsyncSession:
    async with session_factory() as session:
        yield session


def get_participant_repository(
    session: AsyncSession = Depends(yield_db_session),
) -> ParticipantRepository:
    yield ParticipantRepository(session=session)


def get_result_participant_repository(
    session: AsyncSession = Depends(yield_db_session),
) -> ResultParticipantRepository:
    yield ResultParticipantRepository(session=session)


def get_try_festival_repository(
    session: AsyncSession = Depends(yield_db_session),
) -> TryFestivalRepository:
    yield TryFestivalRepository(session=session)
