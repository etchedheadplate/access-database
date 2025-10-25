from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


accesses_resources = Table(
    "accesses_resources",
    Base.metadata,
    Column("access_id", ForeignKey("accesses.id"), primary_key=True),
    Column("resource_id", ForeignKey("resources.id"), primary_key=True),
)

groups_accesses = Table(
    "groups_accesses",
    Base.metadata,
    Column("group_id", ForeignKey("groups.id"), primary_key=True),
    Column("access_id", ForeignKey("accesses.id"), primary_key=True),
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

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    accesses = relationship(
        "Access",
        secondary=accesses_resources,
        back_populates="resources",
    )


class Access(Base):
    __tablename__ = "accesses"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    resources = relationship(
        "Resource",
        secondary=accesses_resources,
        back_populates="accesses",
    )
    groups = relationship(
        "Group",
        secondary=groups_accesses,
        back_populates="accesses",
    )


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    accesses = relationship(
        "Access",
        secondary=groups_accesses,
        back_populates="groups",
    )

    users = relationship(
        "User",
        secondary=user_groups,
        back_populates="groups",
    )
