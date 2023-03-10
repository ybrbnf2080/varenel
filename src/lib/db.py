from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker


def create_url(user: str, password: str, host: str, port: int, db: str) -> str:
    """Create database url."""
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"


def create_engine(url: str) -> AsyncEngine:
    """Create async database engine from url."""
    return create_async_engine(url=url, future=True)


def create_session_factory(engine: AsyncEngine) -> sessionmaker:
    """Create database session factory."""
    return sessionmaker(bind=engine, future=True, class_=AsyncSession)  # type: ignore


def create_session(session_factory: sessionmaker) -> AsyncSession:
    """Create database session from session factory."""
    return session_factory(future=True)  # type: ignore


def session_factory_from_url(
    user: str,
    password: str,
    host: str,
    port: int,
    db: str,
) -> sessionmaker:
    """Create database session factory from url."""
    url = create_url(user=user, password=password, host=host, port=port, db=db)
    engine = create_engine(url=url)
    return create_session_factory(engine=engine)
