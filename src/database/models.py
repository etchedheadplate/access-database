from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


permissions_resources = Table(
    "permissions_resources",
    Base.metadata,
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
    Column("resource_id", ForeignKey("resources.id"), primary_key=True),
)

groups_permissions = Table(
    "groups_permissions",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
)

user_groups = Table(
    "users_groups",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
)


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    groups = relationship(
        "Group",
        secondary=user_groups,
        back_populates="users",
    )


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    permissions = relationship(
        "Permission",
        secondary=permissions_resources,
        back_populates="resources",
    )


class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    resources = relationship(
        "Resource",
        secondary=permissions_resources,
        back_populates="permissions",
    )
    groups = relationship(
        "Group",
        secondary=groups_permissions,
        back_populates="permissions",
    )


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    permissions = relationship(
        "Permission",
        secondary=groups_permissions,
        back_populates="groups",
    )

    users = relationship(
        "User",
        secondary=user_groups,
        back_populates="groups",
    )
