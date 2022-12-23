import logging

import aiohttp
from fastapi import FastAPI

from src.api import errors, handlers, middlewares, providers
from src.lib.config import parse_config
from src.lib.db import session_factory_from_url
from src.lib.logger import setup_logging
from src.lib.logging_service import LoggingService


logger = logging.getLogger(__name__)


def fastapi() -> FastAPI:
    return FastAPI(
        title="Photo reviews API",
        description="Photo reviews API",
        version="0.0.1",
    )


def api() -> FastAPI:
    # Setup logger
    setup_logging()

    # Parse config
    config = parse_config()
    logger.debug("Config: %s", config)

    # Create FastAPI app
    app = fastapi()
    app.openapi_url = None if config.application.production else "/openapi.json"
    app.docs_url = None if config.application.production else "/docs"
    app.redoc_url = None if config.application.production else "/redoc"

    # Setup routers
    handlers.setup_routers(app=app)

    # Setup middleware
    session_factory = session_factory_from_url(
        user=config.postgres.user,
        password=config.postgres.password,
        host=config.postgres.host,
        port=config.postgres.port,
        db=config.postgres.db,
    )

    aiohttp_session = aiohttp.ClientSession()
    errors.setup_error_handlers(
        app=app,
        logging_service=LoggingService(
            session=aiohttp_session,
            log_chat=config.telegram.log_chat,
            debug_chat=config.telegram.debug_chat,
            bot_token=config.telegram.bot_token,
        ),
    )

    middlewares.setup_middlewares(
        app=app,
        api_key=config.application.api_key,
        allowed_paths=[
            "/docs",
            "/docs/",
            "/redoc",
            "/redoc/",
            "/favicon.ico",
            "/openapi.json",
        ],
        production=config.application.production,
    )
    app.dependency_overrides[providers.get_session_factory] = lambda: session_factory
    app.dependency_overrides[providers.get_config] = lambda: config

    # Setup events
    providers.setup_events(
        app=app,
        aiohttp_session=aiohttp_session,
    )

    return app
