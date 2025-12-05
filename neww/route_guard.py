from fastapi import Request
from src.common.app_exception import (
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
)
from src.domain.model.user import User, BasicUser


class RouteGuardMixin:
    def require_profile(self, request: Request) -> User:
        user = request.state.user
        if not user:
            raise NotFoundException(message="Unable to find valid authorized user.")

        if not isinstance(user, User):
            raise UnauthorizedException(message="Unable to find valid user profile.")

        return user

    def require_super_admin_profile(self, request: Request) -> User:
        user = self.require_profile(request)
        if user.is_super_admin is False:
            raise ForbiddenException(
                message="This endpoint is only accessible to super admins."
            )

        return user

    def require_account_without_profile(self, request: Request) -> BasicUser:
        user = request.state.user
        if not user:
            raise NotFoundException(message="Unable to find valid authorized user.")

        if not isinstance(user, BasicUser):
            raise UnauthorizedException(
                message="This endpoint is only accessible to users who have an account but do not yet have a profile."
            )

        if user.email_verified is False:
            raise ForbiddenException(
                message="Please verify your email address, then log in and try again."
            )

        return user
