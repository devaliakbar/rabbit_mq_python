from typing import Any
from fastapi.responses import JSONResponse
from starlette.background import BackgroundTask


class CORSAllowJsonResponse(JSONResponse):
    def __init__(
        self,
        content: Any,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ) -> None:
        cors_headers: dict[str, str] = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }

        final_headers = {**(headers or {}), **cors_headers}

        super().__init__(
            content=content,
            status_code=status_code,
            headers=final_headers,
            media_type=media_type,
            background=background,
        )
