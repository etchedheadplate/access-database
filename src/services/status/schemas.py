from typing import Annotated

from pydantic import BaseModel, Field


class BaseStatus(BaseModel):
    request_id: str
    request_status: str
    request_result: Annotated[
        str | list[str], Field(description="Request result can be a string or list of strings")
    ] = ""


class StatusCreatedResponse(BaseStatus):
    request_status: str = "created"


class StatusValidatedResponse(BaseStatus):
    request_status: str = "validated"


class StatusRejectedResponse(BaseStatus):
    request_status: str = "rejected"


class StatusDoneResponse(BaseStatus):
    request_status: str = "done"


class StatusUnprocessableResponse(BaseStatus):
    request_status: str = "unprocessable"


class StatusNotFoundResponse(BaseStatus):
    request_status: str = "not_found"
