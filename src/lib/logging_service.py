import asyncio
import html
import logging
import re
from dataclasses import dataclass
from typing import Union

import aiohttp

from src.lib.errors.telegram import TelegramError


logger = logging.getLogger(__name__)


_TAGS_REGEX = re.compile(r"<.*?>")


def _remove_tags(raw_html: str) -> str:
    return re.sub(_TAGS_REGEX, "", raw_html)


class LoggingService:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        log_chat: Union[int, str],
        debug_chat: Union[int, str],
        bot_token: str,
    ) -> None:
        """Initialize Telegram repository."""
        self._session = session
        self._log_chat = log_chat
        self._debug_chat = debug_chat
        self._bot_token = bot_token

    async def _send_message(
        self,
        chat_id: Union[int, str],
        text: str,
        parse_mode: str = "html",
        escape_html: bool = False,
    ) -> None:
        """Send message via Telegram bot."""
        url_placeholder = "https://api.telegram.org/bot{bot_token}/sendMessage"
        url = url_placeholder.format(bot_token=self._bot_token)

        text = _remove_tags(text) if escape_html else text
        text = text[:4096]  # Telegram API limit
        params = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
        }
        response = await self._session.get(url=url, params=params)

        if not response.ok:
            if escape_html:
                json = await response.json()
                if "Too Many Requests" in json.get("description", ""):
                    logger.warning(
                        "Telegram API rate limit exceeded. Response: %s", json
                    )
                    await asyncio.sleep(
                        json.get("parameters", {}).get("retry_after", 5)
                    )

                    return await self._send_message(
                        text=text,
                        chat_id=chat_id,
                        parse_mode=parse_mode,
                        escape_html=True,
                    )
                raise TelegramError(str(json))

            else:
                json = await response.json()
                if "Too Many Requests" in json.get("description", ""):
                    logger.warning(
                        "Telegram API rate limit exceeded. Response: %s", json
                    )
                    await asyncio.sleep(
                        json.get("parameters", {}).get("retry_after", 5)
                    )
                    return await self._send_message(
                        text=text,
                        chat_id=chat_id,
                        parse_mode=parse_mode,
                        escape_html=True,
                    )

                logger.warning("Telegram error: %s", json)
                await self._send_message(
                    text=text, chat_id=chat_id, parse_mode=parse_mode, escape_html=True
                )

    async def log(
        self, text: str, parse_mode: str = "html", escape_html: bool = False
    ) -> None:
        """Send message via Telegram bot to log chat."""
        await self._send_message(
            chat_id=self._log_chat,
            text=text,
            parse_mode=parse_mode,
            escape_html=escape_html,
        )

    async def debug(
        self, text: str, parse_mode: str = "html", escape_html: bool = False
    ) -> None:
        """Send message via Telegram bot to debug chat."""
        await self._send_message(
            chat_id=self._debug_chat,
            text=text,
            parse_mode=parse_mode,
            escape_html=escape_html,
        )

    @staticmethod
    def formating_exception(exc: Exception):
        return (
            f"<b>Error</b>: <code>{exc.__class__.__name__}</code>\n"
            f"<b>Message</b>: <code>{html.escape(str(exc))}</code>\n"
        )
