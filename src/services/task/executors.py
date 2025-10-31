from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database.connection import get_async_session
from src.database.models import Group, Permission, Resource, User
from src.services.task.schemas import (
    AccessPermissionTask,
    ExcludeFromGroupTask,
    GetResourcePermissionTask,
    JoinGroupTask,
    RemovePermissionTask,
    ViewUserGroupsTask,
)


class TaskExecutor:
    def __init__(self, request: dict[str, Any]):
        self.request = request
        self.request_id = request["request_id"]
        self.is_done = False
        self.result: str | list[str] = ""

    @asynccontextmanager
    async def session_scope(self) -> AsyncGenerator[AsyncSession, None]:
        async for session in get_async_session():
            try:
                yield session
                await session.commit()
            except Exception:
                self.result = "Error executing database query"
                await session.rollback()
                raise
            finally:
                await session.close()

    async def execute(self) -> None:
        self.is_done = await self._run()

    async def _run(self) -> bool:
        return False


class JoinGroupExecutor(TaskExecutor):
    """Adds User to Group"""

    async def _run(self) -> bool:
        self.task = JoinGroupTask(**self.request)
        try:
            async with self.session_scope() as session:
                user = await session.scalar(select(User).where(User.id == self.task.user_id))  # type: ignore[arg-type]
                group = await session.scalar(select(Group).where(Group.id == self.task.group_id))

                if not user or not group:
                    raise ValueError("User or Group not found")

                if group not in user.groups:
                    user.groups.append(group)

                    self.result = "User added to Group"
            return True
        except Exception:
            return False


class AccessPermissionExecutor(TaskExecutor):
    """Adds Permission to User via all related Groups"""

    async def _run(self) -> bool:
        self.task = AccessPermissionTask(**self.request)
        try:
            async with self.session_scope() as session:
                user = await session.scalar(select(User).where(User.id == self.task.user_id))  # type: ignore[arg-type]
                permission = await session.scalar(select(Permission).where(Permission.id == self.task.permission_id))

                if not user or not permission:
                    raise ValueError("User or Permission not found")

                groups_with_permission = (
                    await session.scalars(
                        select(Group).join(Group.permissions).where(Permission.id == self.task.permission_id)
                    )
                ).all()

                for group in groups_with_permission:
                    if group not in user.groups:
                        user.groups.append(group)

                        self.result = "Permission added to User"
            return True
        except Exception:
            return False


class RemovePermissionExecutor(TaskExecutor):
    """Removes Permission from User by detaching from related Groups"""

    async def _run(self) -> bool:
        self.task = RemovePermissionTask(**self.request)
        try:
            async with self.session_scope() as session:
                user = await session.scalar(select(User).where(User.id == self.task.user_id))  # type: ignore[arg-type]
                permission = await session.scalar(select(Permission).where(Permission.id == self.task.permission_id))

                if not user or not permission:
                    raise ValueError("User or Permission not found")

                groups_with_permission = (
                    await session.scalars(
                        select(Group).join(Group.permissions).where(Permission.id == self.task.permission_id)
                    )
                ).all()

                user.groups = [g for g in user.groups if g not in groups_with_permission]

                self.result = "Permission removed from User"
            return True
        except Exception:
            return False


class ExcludeFromGroupExecutor(TaskExecutor):
    """Removes User from specific Group"""

    async def _run(self) -> bool:
        self.task = ExcludeFromGroupTask(**self.request)
        try:
            async with self.session_scope() as session:
                user = await session.scalar(select(User).where(User.id == self.task.user_id))  # type: ignore[arg-type]
                group = await session.scalar(select(Group).where(Group.id == self.task.group_id))

                if not user or not group:
                    raise ValueError("User or Group not found")

                if group in user.groups:
                    user.groups.remove(group)

                    self.result = "User excluded from Group"
            return True
        except Exception:
            return False


class ViewUserGroupsExecutor(TaskExecutor):
    """Returns list of Groups the User belongs to"""

    async def _run(self) -> bool:
        self.task = ViewUserGroupsTask(**self.request)
        try:
            async with self.session_scope() as session:
                user = await session.scalar(select(User).where(User.id == self.task.user_id))  # type: ignore[arg-type]
                if not user:
                    raise ValueError("User not found")

                groups = [group.name for group in user.groups]

                self.result = groups
            return True
        except Exception:
            return False


class GetResourcePermissionExecutor(TaskExecutor):
    """Returns list of Permissions bound to a Resource"""

    async def _run(self) -> bool:
        self.task = GetResourcePermissionTask(**self.request)
        try:
            async with self.session_scope() as session:
                resource = await session.scalar(select(Resource).where(Resource.id == self.task.resource_id))
                if not resource:
                    raise ValueError("Resource not found")

                permissions = [perm.name for perm in resource.permissions]

                self.result = permissions
            return True
        except Exception:
            return False


def get_task_executor(request: dict[str, Any]) -> TaskExecutor:
    type = request["request_type"]
    executor = ExecutorMapping.TASK[type]
    return executor(request)


class ExecutorMapping:
    TASK = {
        "access_permission": AccessPermissionExecutor,
        "join_group": JoinGroupExecutor,
        "remove_permission": RemovePermissionExecutor,
        "exclude_from_group": ExcludeFromGroupExecutor,
        "view_user_groups": ViewUserGroupsExecutor,
        "get_resource_permission": GetResourcePermissionExecutor,
    }
