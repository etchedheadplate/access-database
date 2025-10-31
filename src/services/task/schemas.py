from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt


class BaseTask(BaseModel):
    request_id: str
    request_type: str
    user_id: str
    error: bool = False
    result: Annotated[str | list[str], Field(description="Task result can be a string or list of strings")]


class AccessPermissionTask(BaseTask):
    request_type: str = "access_permission"
    permission_id: PositiveInt
    permission_groups: list[str]
    user_groups: list[str]


class JoinGroupTask(BaseTask):
    request_type: str = "join_group"
    group_id: PositiveInt
    user_groups: list[str]
    user_permissions: list[str]


class RemovePermissionTask(BaseTask):
    request_type: str = "remove_permission"
    permission_id: PositiveInt


class ExcludeFromGroupTask(BaseTask):
    request_type: str = "exclude_from_group"
    group_id: PositiveInt


class ViewUserGroupsTask(BaseTask):
    request_type: str = "view_user_groups"


class GetResourcePermissionTask(BaseTask):
    request_type: str = "get_resource_permission"
    resource_id: PositiveInt
