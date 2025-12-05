from pydantic import BaseModel
from src.domain.model.error_code import ErrorCodeEnum


class ErrorResponse(BaseModel):
    error: str
    err_code: ErrorCodeEnum | None = None
