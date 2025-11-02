import uuid

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from src.auth.config import JWT_SECRET
from src.database.connection import async_session_maker, get_user_db
from src.database.models import Group, User
from src.logger import logger


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = str(JWT_SECRET)
    verification_token_secret = str(JWT_SECRET)

    async def on_after_register(self, user: User, request: Request | None = None):
        async with async_session_maker() as session:
            stmt_group = select(Group).where(Group.name == "Developer")
            developer_group: Group | None = await session.scalar(stmt_group)

            if developer_group is None:
                developer_group = Group(name="Developer")
                session.add(developer_group)
                try:
                    await session.commit()
                except IntegrityError:
                    await session.rollback()
                    developer_group = await session.scalar(stmt_group)
                await session.refresh(developer_group)

            stmt_user = select(User).options(selectinload(User.groups)).where(User.id == user.id)  # type: ignore
            db_user: User | None = await session.scalar(stmt_user)
            if db_user is None:
                logger.error(f"User {user.id} not found after registration.")
                return

            db_user.groups.append(developer_group)
            await session.commit()

        logger.info(f"User {user.id} added to Developer group.")

    async def on_after_forgot_password(self, user: User, token: str, request: Request | None = None):
        logger.info(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: User, token: str, request: Request | None = None):
        logger.info(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase[User, uuid.UUID] = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/login")


def get_jwt_strategy() -> JWTStrategy[models.UP, models.ID]:  # type: ignore[arg-type]
    return JWTStrategy(secret=str(JWT_SECRET), lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])  # type: ignore[arg-type]

current_active_user = fastapi_users.current_user(active=True)
