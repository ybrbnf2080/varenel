class BaseAppError(Exception):
    """Base app error."""

    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class UnauthorizedError(BaseAppError):
    """Unauthorized error. Analog of HTTP 401."""

    pass


class NotFoundError(BaseAppError):
    """Not found error. Analog of HTTP 404."""

    pass


class AlreadyExistsError(BaseAppError):
    """Already exists error. Analog of HTTP 409."""

    pass


class UnprocessableEntityError(BaseAppError):
    """Unprocessable entity error. Analog of HTTP 422."""

    pass


class InternalServerError(BaseAppError):
    """Internal server error. Analog of HTTP 500."""

    pass
