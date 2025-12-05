from abc import ABC
from src.domain.model.error_code import ErrorCodeEnum


class AppBaseException(Exception, ABC):
    def __init__(
        self,
        status_code: int,
        message: str,
        err_code: ErrorCodeEnum | None = None,
    ):
        self.status_code = status_code
        self.message = message
        self.err_code = err_code
        super().__init__()


class BadRequestException(AppBaseException):
    def __init__(
        self, message: str | None = None, err_code: ErrorCodeEnum | None = None
    ):
        super().__init__(400, message or "Bad Request", err_code=err_code)


class UnauthorizedException(AppBaseException):
    def __init__(
        self, message: str | None = None, err_code: ErrorCodeEnum | None = None
    ):
        super().__init__(401, message or "Unauthorized", err_code=err_code)


class ForbiddenException(AppBaseException):
    def __init__(
        self, message: str | None = None, err_code: ErrorCodeEnum | None = None
    ):
        super().__init__(403, message or "Forbidden", err_code=err_code)


class NotFoundException(AppBaseException):
    def __init__(
        self, message: str | None = None, err_code: ErrorCodeEnum | None = None
    ):
        super().__init__(404, message or "Not Found", err_code=err_code)


class InternalServerErrorException(AppBaseException):
    def __init__(
        self, message: str | None = None, err_code: ErrorCodeEnum | None = None
    ):
        super().__init__(500, message or "Internal Server Error", err_code=err_code)
