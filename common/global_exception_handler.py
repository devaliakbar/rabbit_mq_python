from fastapi import Request
from fastapi.exceptions import RequestValidationError
from src.api.configuration.cors_allow_json_response import CORSAllowJsonResponse
from src.common.app_logger import AppLogger
from src.common.app_exception import AppBaseException
from src.domain.model.error_response import ErrorResponse


class GlobalExceptionHandler:
    def __init__(self, log: AppLogger):
        self.log = log

    async def handle_exception(
        self, request: Request, exc: Exception
    ) -> CORSAllowJsonResponse:
        if isinstance(exc, AppBaseException):
            return await self.handle_base_exception(request, exc)

        if isinstance(exc, RequestValidationError):
            return await self.validation_exception_handler(request, exc)

        self.log.error(
            f"Unexpected error occurred while processing request '{request.url} {exc}'"
        )
        return CORSAllowJsonResponse(
            status_code=500,
            content=ErrorResponse(
                error="Internal Server Error", err_code=None
            ).model_dump(),
        )

    async def handle_base_exception(
        self, request: Request, exc: AppBaseException
    ) -> CORSAllowJsonResponse:
        self.log.error(
            f"{exc.status_code} Error occurred while processing request '{request.url}': {exc.message}"
        )
        return CORSAllowJsonResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                error=exc.message, err_code=exc.err_code
            ).model_dump(),
        )

    async def validation_exception_handler(
        self, request: Request, exc: RequestValidationError
    ) -> CORSAllowJsonResponse:
        error_details = ", ".join(
            [f"{err['loc'][-1]}: {err['msg']}" for err in exc.errors()]
        )
        self.log.error(
            f"Validation error occurred while processing request '{request.url}': {error_details}"
        )
        return CORSAllowJsonResponse(
            status_code=400,
            content=ErrorResponse(error=f"{error_details}", err_code=None).model_dump(),
        )
