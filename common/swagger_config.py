from typing import Any
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


class SwaggerConfig:
    def __init__(self, app: FastAPI, security_scheme_name: str = "BearerAuth") -> None:
        self.app = app
        self.security_scheme_name = security_scheme_name

    def add_security_scheme(self) -> None:
        def custom_openapi() -> dict[str, Any]:
            if self.app.openapi_schema:
                return self.app.openapi_schema

            openapi_schema = get_openapi(
                title=self.app.title,
                version=self.app.version,
                description=self.app.description,
                routes=self.app.routes,
            )

            openapi_schema["components"] = openapi_schema.get("components", {})
            openapi_schema["components"]["securitySchemes"] = {
                self.security_scheme_name: {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            }

            for _, methods in openapi_schema["paths"].items():
                for method in methods:
                    methods[method]["security"] = [{self.security_scheme_name: []}]

            openapi_schema["servers"] = [{"url": "/api"}]
            self.app.openapi_schema = openapi_schema
            return openapi_schema

        self.app.openapi = custom_openapi  # type: ignore
