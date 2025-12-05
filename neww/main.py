from typing import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from src.api.configuration.jwt_middleware import AuthMiddleware
from src.api.configuration.swagger_config import SwaggerConfig
from src.app_container import AppContainer
from src.common.app_util import AppUtil


app_container = AppContainer()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    app_container.app_scheduler().start()
    yield
    app_container.app_scheduler().shutdown()


app = FastAPI(
    root_path="/api",
    title="CCO API",
    summary="API endpoints for CCO services",
    description="This API provides access to CCO backend services and resources.",
    version=AppUtil.get_version(),
    lifespan=lifespan,
)


app.add_middleware(
    AuthMiddleware,
    log=app_container.app_logger(),
    user_service=app_container.user_service(),
    exempt_routes=[
        "/docs",
        "/api/openapi.json",
        "/api/v1/user/create-account",
        "/api/v1/user/auth-token",
        "/api/v1/user/accept-invitation",
        "/api/v1/user/token-signup",
    ],
)


app.add_exception_handler(Exception, app_container.exception_handler().handle_exception)
app.add_exception_handler(
    RequestValidationError, app_container.exception_handler().handle_exception
)

swagger_config = SwaggerConfig(app)
swagger_config.add_security_scheme()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(app_container.v1_router())
