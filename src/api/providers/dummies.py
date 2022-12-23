from sqlalchemy.ext.asyncio import AsyncSession

from src.lib.config import Config


def get_config() -> Config:
    ...


def get_session_factory() -> AsyncSession:
    ...


