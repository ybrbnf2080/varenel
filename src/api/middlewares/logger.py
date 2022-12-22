import json
import logging
import math
import time
import traceback
import uuid
from typing import Dict

from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from src.lib.logger.scheme import (
    ExceptionJsonLogSchema,
    RequestJsonLogSchema,
    ResponseJsonLogSchema,
)


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self._logger = logging.getLogger(__name__)

    @staticmethod
    async def get_protocol(request: Request) -> str:
        protocol = str(request.scope.get("type", ""))
        http_version = str(request.scope.get("http_version", ""))
        if protocol.lower() == "http" and http_version:
            return f"{protocol.upper()}/{http_version}"
        return ""

    @staticmethod
    async def set_body(request: Request, body: bytes) -> None:
        async def receive() -> Dict[str, str]:
            return {"type": "http.request", "body": body}

        request._receive = receive

    async def get_body(self, request: Request) -> bytes:
        body = await request.body()
        await self.set_body(request, body)
        return body

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
        *args,
        **kwargs,
    ) -> Response:
        """Log request and response in `JSON` format."""
        # Set request id
        request.state.id = str(uuid.uuid4())

        # Create needed variables
        start_time = time.time()

        # Request side
        try:
            raw_request_body = await request.body()
            await self.set_body(request, raw_request_body)
            raw_request_body = await self.get_body(request)
            request_body = raw_request_body.decode()
        except Exception:  # noqa
            request_body = ""

        # Create request log schema
        request_headers: dict = dict(request.headers.items())
        request_json_fields = RequestJsonLogSchema(
            request_id=request.state.id,
            request_referer=request_headers.get("referer", None),
            request_method=request.method,
            request_path=request.url.path,
            request_query_params=dict(request.query_params.multi_items()),
            request_body=request_body,
            remote_ip=request.client[0],
            remote_port=request.client[1],
        ).dict()

        # Log request data
        self._logger.debug(json.dumps(request_json_fields, indent=4))

        # Response side
        try:
            response = await call_next(request)
        except Exception as exc:
            exception_json_response = ExceptionJsonLogSchema(
                request_id=request.state.id,
                error=str(exc),
                traceback=str(
                    traceback.format_exception(type(exc), exc, exc.__traceback__)
                ),
            ).dict()
            self._logger.debug(json.dumps(exception_json_response, indent=4))
            raise exc
        else:
            response_body = b""
            async for chunk in response.body_iterator:  # noqa
                response_body += chunk
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )

        # Create response log schema
        duration: int = math.ceil((time.time() - start_time) * 1000)
        response_json_fields = ResponseJsonLogSchema(
            request_id=request.state.id,
            response_status_code=response.status_code,
            response_body=response_body.decode(),
            response_duration=duration,
        ).dict()

        # Log response data
        self._logger.debug(json.dumps(response_json_fields, indent=4))
        return response
