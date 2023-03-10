from .base import (
    AlreadyExistsError,
    BaseAppError,
    NotFoundError,
)


class TelegramError(BaseAppError):
    """Telegram"""

    def __init__(self, error: str) -> None:
        super().__init__(f"Telegram_error: \n{error}")
