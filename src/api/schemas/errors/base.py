from pydantic import BaseModel, Field


class BaseApiError(BaseModel):
    """Base scheme for all API errors."""

    error: str
    detail: str

    class Config:
        schema_extra = {
            "required": ["error", "detail"],
        }


class NotFoundError(BaseApiError):
    """Error for not found resources. Analog of HTTP 404."""

    error: str = Field(default="NotFoundError", const=True)


class AlreadyExistsError(BaseApiError):
    """Error for already exists resources. Analog of HTTP 409."""

    error: str = Field(default="AlreadyExistsError", const=True)


class UnprocessableEntityError(BaseApiError):
    """Error for unprocessable entities. Analog of HTTP 422."""

    error: str = Field(default="UnprocessableEntityError", const=True)


class UnauthorizedError(BaseApiError):
    """Unauthorized error. Analog of HTTP 401."""

    error: str = Field(default="UnauthorizedError", const=True)


class ServerInternalError(BaseApiError):
    """Server internal error. Analog of HTTP 500."""

    error: str = Field("ServerInternalError", const=True)
    detail: str = Field("Server internal error", const=True)
    traceback: str

    class Config:
        schema_extra = {
            "required": ["error", "detail", "traceback"],
        }
