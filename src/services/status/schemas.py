from typing import Annotated

from pydantic import BaseModel, Field


class BaseStatus(BaseModel):
    request_id: str
    request_status: str
    request_result: Annotated[str | list[str], Field(description="Request result can be a string or list of strings")]


class StatusDoneResponse(BaseStatus):
    request_status: str = "done"
    request_result: Annotated[str | list[str], Field(description=None)] = ""


class StatusUnprocessableResponse(BaseStatus):
    request_status: str = "unprocessable"
    request_result: Annotated[str | list[str], Field(description=None)] = ""


class StatusValidatedResponse(BaseStatus):
    request_status: str = "validated"
    request_result: Annotated[str | list[str], Field(description=None)] = ""
