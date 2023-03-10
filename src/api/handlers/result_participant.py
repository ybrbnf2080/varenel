import logging
from dataclasses import asdict
from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from src.api.providers import (
    get_result_participant_repository,
)
from src.api.providers.services import (
    get_result_calc_service,
)
from src.api.schemas import errors
from src.database.repo import ResultParticipantRepository
from src.lib import enums, models
from src.service.result_calc import RelsultCalcService


result_participants_router = APIRouter(
    prefix="/result_participants",
    tags=["Result Participant"],
)

logger = logging.getLogger(__name__)


@result_participants_router.get(
    path="/",
    response_model=List[models.ResultParticipant],
    summary="Get result_participants",
    description="Get all result_participants",
)
async def get_result_participants(
    offset_type: enums.OffsetType,
    offset_id: int = 0,
    limit: int = 10,
    result_participant_service: ResultParticipantRepository = Depends(
        get_result_participant_repository
    ),
) -> List[models.ResultParticipant]:
    """Get all result_participants"""

    return await result_participant_service.get_all(
        offset_type=offset_type,
        offset_id=offset_id,
        limit=limit,
    )


@result_participants_router.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": models.ResultParticipant},
        status.HTTP_409_CONFLICT: {"model": errors.AlreadyExistsError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": errors.UnprocessableEntityError
        },
    },
    summary="Create result_participant",
    description="Add new result_participant to database",
)
async def create_result_participant(
    request: models.ResultParticipant,
    result_participant_service: ResultParticipantRepository = Depends(
        get_result_participant_repository
    ),
) -> models.ResultParticipant:
    """Create result_participant"""
    new_result_participant = await result_participant_service.create(request)
    return new_result_participant


@result_participants_router.get(
    path="/group/{group}",
    responses={
        status.HTTP_200_OK: {"model": List[models.ResultParticipant]},
        status.HTTP_404_NOT_FOUND: {"model": errors.NotFoundError},
    },
    summary="Get result_participants by group",
    description="Get result_participant by group",
)
async def get_result_participant(
    group: enums.Group,
    result_calc_service: RelsultCalcService = Depends(get_result_calc_service),
) -> List[models.ResultParticipant]:
    """Get result_participant by ID"""

    result_participant = await result_calc_service.get_result_by_group(group=group)
    return result_participant


@result_participants_router.get(
    path="/{result_participant_id}",
    responses={
        status.HTTP_200_OK: {"model": models.ResultParticipant},
        status.HTTP_404_NOT_FOUND: {"model": errors.NotFoundError},
    },
    summary="Get result_participant",
    description="Get result_participant by ID",
)
async def get_result_participant(
    result_participant_id: int,
    result_participant_service: ResultParticipantRepository = Depends(
        get_result_participant_repository
    ),
) -> models.ResultParticipant:
    """Get result_participant by ID"""

    result_participant = await result_participant_service.get(
        result_participant_id=result_participant_id
    )
    return result_participant


# @result_participants_router.delete(
#     path="/{result_participant_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     responses={
#         status.HTTP_204_NO_CONTENT: {"model": None},
#         status.HTTP_404_NOT_FOUND: {"model": errors.NotFoundError},
#     },
#     summary="Delete result_participant",
#     description="Delete result_participant by ID",
# )
# async def delete_result_participant(
#     result_participant_id: int,
#     result_participant_service: ResultParticipantRepository = Depends(get_result_participant_repository),
# ) -> None:
#     """Delete result_participant by ID"""
#     await result_participant_service.delete(try_id=result_participant_id)
# get_result_calc_service
