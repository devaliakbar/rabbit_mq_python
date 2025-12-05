from fastapi import APIRouter, Body, Request, UploadFile, File
from src.common.app_exception import BadRequestException
from src.domain.model.auth_token_req import AuthTokenReq
from src.domain.model.auth_token_res import AuthTokenRes
from src.domain.model.create_account_req import CreateAccountReq
from src.domain.model.create_account_res import CreateAccountRes
from src.domain.model.create_profile_req import CreateProfileReq
from src.domain.model.file_info import FileInfo
from src.domain.model.user_preferences import (
    SaveUserPreferencesReq,
    UserPreferencesExtended,
)
from src.domain.model.user import User, UserProfile
from src.domain.service.user_service import UserService
from src.api.configuration.route_guard import RouteGuardMixin
from src.domain.model.status_res import StatusRes
from src.domain.model.invite_user import (
    InviteUserReq,
    InviteUserRes,
    TokenSignupReq,
    TokenSignupRes,
)


class UserController(APIRouter, RouteGuardMixin):
    def __init__(self, user_service: UserService, prefix: str = "/user"):
        self._user_service = user_service
        super().__init__(prefix=prefix, tags=["User"])

        self.add_api_route(
            path="/create-account",
            methods=["POST"],
            status_code=201,
            endpoint=self.create_account,
            summary="Create a new user account",
            description="This endpoint allows for the creation of a new user account. It returns the user id upon successful account creation.",
        )

        self.add_api_route(
            path="/auth-token",
            methods=["POST"],
            status_code=201,
            endpoint=self.generate_auth_token,
            summary="Generate a new authentication token",
            description="This endpoint generates a new authentication token by providing the email and password of the user.",
        )

        self.add_api_route(
            path="/profile",
            methods=["GET"],
            status_code=200,
            endpoint=self.get_profile,
            summary="Get user profile",
            description="This endpoint retrieves the user profile.",
        )

        self.add_api_route(
            path="/create-profile",
            methods=["POST"],
            status_code=200,
            endpoint=self.create_profile,
            summary="Create user profile",
            description="This endpoint creates a user profile.",
        )

        self.add_api_route(
            path="/profile",
            methods=["PUT"],
            status_code=200,
            endpoint=self.update_profile,
            summary="Update user profile",
            description="This endpoint updates user profile details.",
        )

        self.add_api_route(
            path="/upload-profile-picture",
            methods=["POST"],
            status_code=200,
            endpoint=self.upload_profile_picture,
            summary="Upload profile picture",
            description="This endpoint upload profile picture and return file access information.",
        )

        self.add_api_route(
            path="/verification/upload-doc",
            methods=["POST"],
            status_code=200,
            endpoint=self.upload_user_verification_doc,
            summary="Upload user verification document",
            description="This endpoint uploads a user verification document. Accepts PDF, DOC, DOCX, PNG, JPEG up to 20MB.",
        )

        self.add_api_route(
            path="/preferences",
            methods=["POST"],
            status_code=200,
            endpoint=self.save_user_preferences,
            summary="Save user preferences",
            description="This endpoint saves user preferences including dress styles, club genres, and age preferences.",
        )

        self.add_api_route(
            path="/preferences",
            methods=["GET"],
            status_code=200,
            endpoint=self.get_user_preferences,
            summary="Get user preferences",
            description="This endpoint retrieves user preferences including dress styles, club genres, and age preferences.",
        )

        self.add_api_route(
            path="/delete-account",
            methods=["DELETE"],
            status_code=200,
            endpoint=self.delete_account,
            summary="Delete user account",
            description="This endpoint deletes the user account.",
        )

        self.add_api_route(
            path="/accept-invitation",
            methods=["POST"],
            status_code=200,
            endpoint=self.accept_invitation,
            summary="Accept invitation",
            description="Accepts an invitation token and returns user email and optional signup token.",
        )

        self.add_api_route(
            path="/token-signup",
            methods=["POST"],
            status_code=201,
            endpoint=self.token_signup,
            summary="Signup using token",
            description="Creates an account using a valid token and password.",
        )

    async def create_account(self, body: CreateAccountReq) -> CreateAccountRes:
        return await self._user_service.create_account(req=body)

    async def generate_auth_token(self, body: AuthTokenReq) -> AuthTokenRes:
        return await self._user_service.generate_auth_token(req=body)

    async def get_profile(self, request: Request) -> UserProfile:
        access_user = self.require_profile(request)
        return await self._user_service.get_profile(access_user=access_user)

    async def create_profile(
        self,
        request: Request,
        body: CreateProfileReq = Body(...),
    ) -> User:
        basic_user = self.require_account_without_profile(request)
        return await self._user_service.create_profile(
            basic_user=basic_user, user_detail=body
        )

    async def upload_profile_picture(
        self,
        request: Request,
        file: UploadFile = File(...),
    ) -> FileInfo:
        access_user = self.require_profile(request)
        allowed_content_types = ["image/png", "image/jpeg", "image/jpg"]
        if file.content_type not in allowed_content_types:
            raise BadRequestException(
                message=f"Only PNG and JPEG files are allowed. Received: {file.content_type}",
            )

        file_content = await file.read()

        max_size = 10 * 1024 * 1024
        if len(file_content) > max_size:
            raise BadRequestException(
                message=f"File size exceeds maximum allowed size of 10MB. Current size: {len(file_content) / (1024 * 1024):.2f}MB",
            )

        return await self._user_service.upload_profile_picture(
            access_user=access_user,
            file_name=str(file.filename),
            content_type=file.content_type,
            file_content=file_content,
        )

    async def upload_user_verification_doc(
        self,
        request: Request,
        file: UploadFile = File(...),
    ) -> FileInfo:
        access_user = self.require_profile(request)
        allowed_content_types = [
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "application/msword",
            "image/png",
            "image/jpeg",
            "image/jpg",
        ]
        if file.content_type not in allowed_content_types:
            raise BadRequestException(
                message=f"Only PDF, DOC, DOCX, PNG and JPEG files are allowed. Received: {file.content_type}",
            )

        file_content = await file.read()

        max_size = 20 * 1024 * 1024
        if len(file_content) > max_size:
            raise BadRequestException(
                message=f"File size exceeds maximum allowed size of 20MB. Current size: {len(file_content) / (1024 * 1024):.2f}MB",
            )

        return await self._user_service.upload_user_verification_doc(
            access_user=access_user,
            file_name=str(file.filename),
            content_type=file.content_type,
            file_content=file_content,
        )

    async def update_profile(
        self,
        request: Request,
        body: CreateProfileReq = Body(...),
    ) -> None:
        access_user = self.require_profile(request)
        return await self._user_service.update_profile(
            access_user=access_user, user_detail=body
        )

    async def save_user_preferences(
        self,
        request: Request,
        body: SaveUserPreferencesReq,
    ) -> None:
        access_user = self.require_profile(request)
        await self._user_service.save_user_preferences(
            access_user=access_user, preferences=body
        )

    async def get_user_preferences(
        self, request: Request
    ) -> UserPreferencesExtended | None:
        access_user = self.require_profile(request)
        return await self._user_service.get_user_preferences(user_id=access_user.id)

    async def delete_account(self, request: Request) -> StatusRes:
        access_user = self.require_profile(request)
        await self._user_service.delete_account(access_user=access_user)

        return StatusRes()

    async def accept_invitation(self, body: InviteUserReq) -> InviteUserRes:
        return await self._user_service.accept_invitation(req=body)

    async def token_signup(self, body: TokenSignupReq) -> TokenSignupRes:
        return await self._user_service.token_signup(req=body)
