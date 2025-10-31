from typing import Any

from src.services.status.schemas import StatusDoneResponse, StatusUnprocessableResponse


class StatusProcessor:
    def __init__(self, message: dict[str, Any]):
        self.message = message
        self.request_id = message["request_id"]
        self.request_status = message["request_status"]
        self.is_appropriate = self._is_validated()

    def _is_validated(self) -> bool:
        return self.request_status == "validated"

    async def process(self, task_executed: bool, task_result: str | list[str]):
        self.request_result = task_result
        if not task_executed:
            return StatusUnprocessableResponse(request_id=self.request_id, request_result=self.request_result)
        return StatusDoneResponse(request_id=self.request_id, request_result=self.request_result)
