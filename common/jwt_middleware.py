from typing import Callable, override
from collections.abc import Sequence, Awaitable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp
from src.common.app_logger import AppLogger
from src.common.app_exception import (
    UnauthorizedException,
)
from src.domain.model.user import User, BasicUser
from src.domain.service.user_service import UserService


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        log: AppLogger,
        user_service: UserService,
        exempt_routes: Sequence[str] | None = None,
    ) -> None:
        super().__init__(app)
        self.log = log
        self.user_service = user_service
        self.exempt_routes = exempt_routes or []

    @override
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        path: str = request.url.path
        if any(path.startswith(exempt_route) for exempt_route in self.exempt_routes):
            return await call_next(request)

        auth_header: str | None = request.headers.get("Authorization")
        if not auth_header:
            raise UnauthorizedException(message="Missing Authorization token")

        if not auth_header.startswith("Bearer "):
            raise UnauthorizedException(message="Invalid Authorization header format")

        token: str = auth_header[7:].strip()

        user: User | BasicUser = await self.user_service.get_user_from_token(
            token=token
        )

        request.state.user = user

        return await call_next(request)
