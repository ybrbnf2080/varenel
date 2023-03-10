import logging
from dataclasses import asdict
from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from src.api.providers import get_try_festival_repository
from src.api.schemas import errors
from src.database.repo import TryFestivalRepository
from src.lib import enums, models


try_festivals_router = APIRouter(
    prefix="/try_festivals",
    tags=["Try festival"],
)

logger = logging.getLogger(__name__)


@try_festivals_router.get(
    path="/",
    response_model=List[models.TryFestival],
    summary="Get try_festivals",
    description="Get all try_festivals",
)
async def get_try_festivals(
    offset_type: enums.OffsetType,
    offset_id: int = 0,
    limit: int = 10,
    try_festival_service: TryFestivalRepository = Depends(get_try_festival_repository),
) -> List[models.TryFestival]:
    """Get all try_festivals"""

    return await try_festival_service.get_all(
        offset_type=offset_type,
        offset_id=offset_id,
        limit=limit,
    )


@try_festivals_router.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": models.TryFestival},
        status.HTTP_409_CONFLICT: {"model": errors.AlreadyExistsError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": errors.UnprocessableEntityError
        },
    },
    summary="Create try_festival",
    description="Add new try_festival to database",
)
async def create_try_festival(
    request: models.TryFestival,
    try_festival_service: TryFestivalRepository = Depends(get_try_festival_repository),
) -> models.TryFestival:
    """Create try_festival"""
    new_try_festival = await try_festival_service.create(request)
    return new_try_festival


@try_festivals_router.get(
    path="/{try_festival_id}",
    responses={
        status.HTTP_200_OK: {"model": models.TryFestival},
        status.HTTP_404_NOT_FOUND: {"model": errors.NotFoundError},
    },
    summary="Get try_festival",
    description="Get try_festival by ID",
)
async def get_try_festival(
    try_festival_id: int,
    try_festival_service: TryFestivalRepository = Depends(get_try_festival_repository),
) -> models.TryFestival:
    """Get try_festival by ID"""

    try_festival = await try_festival_service.get(try_festival_id=try_festival_id)
    return try_festival


@try_festivals_router.delete(
    path="/{try_festival_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_404_NOT_FOUND: {"model": errors.NotFoundError},
    },
    summary="Delete try_festival",
    description="Delete try_festival by ID",
)
async def delete_try_festival(
    try_festival_id: int,
    try_festival_service: TryFestivalRepository = Depends(get_try_festival_repository),
) -> None:
    """Delete try_festival by ID"""
    await try_festival_service.delete(try_id=try_festival_id)
