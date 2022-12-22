import logging
from functools import partial

import aiohttp
from aiogram import Bot
from fastapi import FastAPI


logger = logging.getLogger(__name__)


async def on_startup(aiohttp_session: aiohttp.ClientSession) -> None:
    await aiohttp_session.__aenter__()
    logger.info("Application startup")


async def on_shutdown(aiohttp_session: aiohttp.ClientSession) -> None:
    await aiohttp_session.close()
    logger.info("Application shutdown")


def setup_events(app: FastAPI, aiohttp_session: aiohttp.ClientSession) -> None:
    app.add_event_handler(
        event_type="startup",
        func=partial(on_startup, aiohttp_session=aiohttp_session),
    )
    app.add_event_handler(
        event_type="shutdown",
        func=partial(on_shutdown, aiohttp_session=aiohttp_session),
    )
