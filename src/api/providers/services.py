from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.database.repo.track import TrackRepository

from src.api.providers.dummies import get_session_factory
from src.database.repo import (
    ParticipantRepository,
    ResultParticipantRepository,
    TryFestivalRepository,
)
from src.service.result_calc import RelsultCalcService


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


def get_track_repository(
    session: AsyncSession = Depends(yield_db_session),
) -> TrackRepository:
    yield TrackRepository(session=session)


def get_try_festival_repository(
    session: AsyncSession = Depends(yield_db_session),
) -> TryFestivalRepository:
    yield TryFestivalRepository(session=session)


def get_result_calc_service(
    participant_repo: ParticipantRepository = Depends(get_participant_repository),
    result_participant_repo: ResultParticipantRepository = Depends(
        get_result_participant_repository
    ),
    try_festival_repo: TryFestivalRepository = Depends(get_try_festival_repository),
) -> RelsultCalcService:
    yield RelsultCalcService(
        participant_repo=participant_repo,
        result_participant_repo=result_participant_repo,
        try_festival_repo=try_festival_repo,
    )
