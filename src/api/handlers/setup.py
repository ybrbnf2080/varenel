from fastapi import FastAPI

from .partipicant import participants_router
from .result_participant import result_participants_router
from .try_festival import try_festivals_router


def setup_routers(app: FastAPI) -> None:
    app.include_router(try_festivals_router, prefix="/api/v1")
    app.include_router(participants_router, prefix="/api/v1")
    app.include_router(result_participants_router, prefix="/api/v1")
