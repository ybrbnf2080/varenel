from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class RequestJsonLogSchema(BaseModel):
    """Request log schema."""

    type: str = Field("request", const=True)
    request_id: str
    request_method: str
    request_path: str
    request_query_params: Dict[str, Any]
    request_referer: Optional[str]
    request_body: str
    remote_ip: str
    remote_port: int


class ResponseJsonLogSchema(BaseModel):
    """Response log scheme."""

    type: str = Field("response", const=True)
    request_id: str
    response_status_code: int
    response_body: str
    response_duration: int


class ExceptionJsonLogSchema(BaseModel):
    """Error log schema."""

    type: str = Field("exception", const=True)
    request_id: str
    error: str
    traceback: Optional[str]
