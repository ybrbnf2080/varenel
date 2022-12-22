from typing import Awaitable, Callable, List

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        api_key: str,
        allowed_paths: List[str],
        production: bool,
    ) -> None:
        super().__init__(app)
        self._api_key = api_key
        self._allowed_paths = allowed_paths
        self._production = production

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        if (
            request.url.path not in self._allowed_paths
            and request.headers.get("X-API-Key") != self._api_key
        ):
            if self._production:
                return PlainTextResponse(status_code=status.HTTP_404_NOT_FOUND)
            else:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "Incorrect X-API-Key"},
                )

        return await call_next(request)
