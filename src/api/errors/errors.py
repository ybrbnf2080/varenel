import asyncio
import html
import logging
import traceback
from typing import Any, Callable

from fastapi import FastAPI, status
from starlette.requests import Request
from starlette.responses import (
    JSONResponse,
    PlainTextResponse,
    Response,
)

from src.api.schemas import errors as api_errors
from src.lib import errors as app_errors
from src.lib.logging_service import LoggingService


class ApiErrorHandler:
    def __init__(self, logging_service: LoggingService) -> None:
        self._logging_service = logging_service
        self._logger = logging.getLogger(__name__)

    async def handle(self, request: Request, error: Exception) -> JSONResponse:
        """Handle error."""
        if isinstance(error, app_errors.BaseAppError):
            return await self.handle_app_error(request=request, exc=error)
        return await self.handle_all_errors(request=request, exc=error)

    async def handle_all_errors(self, request: Request, exc: Exception) -> JSONResponse:
        """Handle all errors."""
        self._log(request, exc)
        await self._log_to_external_service(request, exc)
        return self._internal_error(exc)

    async def handle_app_error(
        self, request: Request, exc: app_errors.BaseAppError
    ) -> JSONResponse:
        """Handle app errors."""
        self._log(request, exc)
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        constructor = api_errors.BaseApiError

        if isinstance(exc, app_errors.UnauthorizedError):
            status_code = status.HTTP_401_UNAUTHORIZED
            constructor = api_errors.UnauthorizedError

        if isinstance(exc, app_errors.NotFoundError):
            status_code = status.HTTP_404_NOT_FOUND
            constructor = api_errors.NotFoundError

        if isinstance(exc, app_errors.AlreadyExistsError):
            status_code = status.HTTP_409_CONFLICT
            constructor = api_errors.AlreadyExistsError

        if isinstance(exc, app_errors.UnprocessableEntityError):
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            constructor = api_errors.UnprocessableEntityError

        # Process error if unhandled
        if status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            await self._log_to_external_service(request, exc)
            return self._internal_error(exc)

        # Process expected errors
        return JSONResponse(
            status_code=status_code,
            content=constructor(
                detail=exc.message,
            ).dict(),
        )

    def _log(self, request: Request, exc: Exception) -> None:
        """Log error."""
        self._logger.error("RequestID: %s; Error: %s", request.state.id, exc)

    @staticmethod
    def _internal_error(exc: Exception) -> JSONResponse:
        """Return internal server error."""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=api_errors.ServerInternalError(
                traceback="\n".join(
                    traceback.format_exception(type(exc), exc, exc.__traceback__)
                ),
            ).dict(),
        )

    async def _log_to_external_service(self, request: Request, exc: Exception):
        """Send error message to telegram."""
        # Don't send telegram message if it's already `TelegramError`

        message = (
            f"<b>Error</b>: <code>{exc.__class__.__name__}</code>\n"
            f"<b>RequestID</b>: <code>{request.state.id}</code>\n"
            f"<b>Message</b>: <code>{html.escape(str(exc))}</code>\n"
        )
        asyncio.create_task(self._logging_service.log(text=message))


def setup_error_handlers(
    app: FastAPI,
    logging_service: LoggingService,
) -> None:
    """Setup error handlers."""
    api_handler = ApiErrorHandler(
        logging_service=logging_service,
    )

    app.add_exception_handler(
        app_errors.BaseAppError,
        handler=api_handler.handle_app_error,
    )
    app.add_exception_handler(
        Exception,
        handler=api_handler.handle_all_errors,
    )


def factory_exception_code_handler(
    status_code: int,
) -> Callable[[Request, ...], Response]:
    def none_handler(_: Request, *args: Any) -> Response:
        return PlainTextResponse(status_code=status_code)

    return none_handler
