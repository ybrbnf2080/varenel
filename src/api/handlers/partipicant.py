import logging
from dataclasses import asdict
from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from src.api.providers import get_participant_repository
from src.api.schemas import errors
from src.database.repo import ParticipantRepository
from src.lib import enums, models


participants_router = APIRouter(
    prefix="/participants",
    tags=["Participant"],
)

logger = logging.getLogger(__name__)


@participants_router.get(
    path="/",
    response_model=List[models.Participant],
    summary="Get participants",
    description="Get all participants",
)
async def get_participants(
    offset_type: enums.OffsetType,
    offset_id: int = 0,
    limit: int = 10,
    participant_service: ParticipantRepository = Depends(get_participant_repository),
) -> List[models.Participant]:
    """Get all participants"""

    return await participant_service.get_all(
        offset_type=offset_type,
        offset_id=offset_id,
        limit=limit,
    )


@participants_router.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": models.Participant},
        status.HTTP_409_CONFLICT: {"model": errors.AlreadyExistsError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": errors.UnprocessableEntityError
        },
    },
    summary="Create participant",
    description="Add new participant to database",
)
async def create_participant(
    request: models.Participant,
    participant_service: ParticipantRepository = Depends(get_participant_repository),
) -> models.Participant:
    """Create participant"""
    new_participant = await participant_service.create(request=request)
    return new_participant


@participants_router.get(
    path="/{participant_id}",
    responses={
        status.HTTP_200_OK: {"model": models.Participant},
        status.HTTP_404_NOT_FOUND: {"model": errors.NotFoundError},
    },
    summary="Get participant",
    description="Get participant by ID",
)
async def get_participant(
    participant_id: int,
    participant_service: ParticipantRepository = Depends(get_participant_repository),
) -> models.Participant:
    """Get participant by ID"""

    participant = await participant_service.get(participant_id=participant_id)
    return participant


# @participants_router.delete(
#     path="/{participant_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     responses={
#         status.HTTP_204_NO_CONTENT: {"model": None},
#         status.HTTP_404_NOT_FOUND: {"model": errors.NotFoundError},
#     },
#     summary="Delete participant",
#     description="Delete participant by ID",
# )
# async def delete_participant(
#     participant_id: int,
#     participant_service: ParticipantRepository = Depends(get_participant_repository),
# ) -> None:
#     """Delete participant by ID"""
#     await participant_service.delete(participant_id=participant_id)
