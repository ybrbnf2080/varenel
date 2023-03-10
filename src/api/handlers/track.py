import logging
from dataclasses import asdict
from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from src.api.providers import get_track_repository
from src.api.schemas import errors
from src.database.repo import TrackRepository
from src.lib import enums, models


tracks_router = APIRouter(
    prefix="/tracks",
    tags=["Tracks"],
)

logger = logging.getLogger(__name__)


@tracks_router.get(
    path="/",
    response_model=List[models.Track],
    summary="Get tracks",
    description="Get all tracks",
)
async def get_tracks(
    offset_type: enums.OffsetType,
    offset_id: int = 0,
    limit: int = 10,
    track_service: TrackRepository = Depends(get_track_repository),
) -> List[models.Track]:
    """Get all tracks"""

    return await track_service.get_all(
        offset_type=offset_type,
        offset_id=offset_id,
        limit=limit,
    )


@tracks_router.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": models.Track},
        status.HTTP_409_CONFLICT: {"model": errors.AlreadyExistsError},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": errors.UnprocessableEntityError
        },
    },
    summary="Create track",
    description="Add new track to database",
)
async def create_track(
    request: models.Track,
    track_service: TrackRepository = Depends(get_track_repository),
) -> models.Track:
    """Create track"""
    new_track = await track_service.create(request)
    return new_track


@tracks_router.get(
    path="/group/{group}",
    responses={
        status.HTTP_200_OK: {"model": List[models.Track]},
        status.HTTP_404_NOT_FOUND: {"model": errors.NotFoundError},
    },
    summary="Get track",
    description="Get track by ID",
)
async def get_track_by_group(
    group: enums.Group,
    track_service: TrackRepository = Depends(get_track_repository),
) -> List[models.Track]:
    """Get track by ID"""

    track = await track_service.get_all_from_group(group=group)
    return track


@tracks_router.get(
    path="/{track_id}",
    responses={
        status.HTTP_200_OK: {"model": models.Track},
        status.HTTP_404_NOT_FOUND: {"model": errors.NotFoundError},
    },
    summary="Get track",
    description="Get track by ID",
)
async def get_track(
    track_id: int,
    track_service: TrackRepository = Depends(get_track_repository),
) -> models.Track:
    """Get track by ID"""

    track = await track_service.get(track_id=track_id)
    return track


@tracks_router.delete(
    path="/{track_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_404_NOT_FOUND: {"model": errors.NotFoundError},
    },
    summary="Delete track",
    description="Delete track by ID",
)
async def delete_track(
    track_id: int,
    track_service: TrackRepository = Depends(get_track_repository),
) -> None:
    """Delete track by ID"""
    await track_service.delete(number=track_id)
