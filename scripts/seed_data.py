from uuid import uuid4

from fastapi_users.password import PasswordHelper
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker

from src.config import Settings
from src.database.models import Base, Group, Permission, Resource, User
from src.logger import logger

settings = Settings()  # type: ignore[call-arg]

DATABASE_URL = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def seed():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    try:
        resource_names = [
            "API URLs",
            "API keys",
            "Database Users",
            "Database Goods",
            "Database Sales",
            "SSH address",
            "SSH keys",
            "Report on Strategy",
            "Report on Operations",
            "Report for Shareholders",
        ]

        resources_dict = {}
        for name in resource_names:
            stmt = insert(Resource).values(name=name).on_conflict_do_nothing(index_elements=["name"])
            session.execute(stmt)
        session.commit()

        for name in resource_names:
            resources_dict[name] = session.query(Resource).filter_by(name=name).first()

        logger.info("Resources added or verified")

        permissions_data = [
            ("API Access", ["API URLs", "API keys"]),
            ("Database Access", ["Database Users", "Database Goods", "Database Sales"]),
            ("Deploy Access", ["SSH address", "SSH keys"]),
            ("Report Access", ["Report on Strategy", "Report on Operations", "Report for Shareholders"]),
        ]

        permissions_dict = {}
        for perm_name, res_names in permissions_data:
            perm = session.query(Permission).filter_by(name=perm_name).first()
            if not perm:
                perm = Permission(name=perm_name, resources=[resources_dict[r] for r in res_names])
                session.add(perm)
            permissions_dict[perm_name] = perm
        session.commit()
        logger.info("Permissions added or verified")

        groups_data = [
            ("Developer", ["API Access", "Database Access"], ["API URLs", "Database Goods"]),
            ("DB Admin", ["Database Access"], ["Database Users", "Database Sales"]),
            ("DevOps", ["API Access", "Database Access", "Deploy Access"], ["SSH address"]),
            ("Owner", ["Report Access"], ["Report on Strategy", "Report for Shareholders"]),
        ]

        groups_dict = {}
        for group_name, perm_names, res_names in groups_data:
            group = session.query(Group).filter_by(name=group_name).first()
            if not group:
                group = Group(
                    name=group_name,
                    permissions=[permissions_dict[p] for p in perm_names],
                    resources=[resources_dict[r] for r in res_names],
                )
                session.add(group)
            groups_dict[group_name] = group
        session.commit()
        logger.info("Groups added or verified")

        pwd_helper = PasswordHelper()
        hashed_password = pwd_helper.hash("secure")

        users_data = [
            ("alice@example.com", ["Developer"], ["API Access"], ["API URLs"]),
            ("bob@example.com", ["Developer"], ["API Access", "Database Access"], ["API keys", "Database Goods"]),
            ("charlie@example.com", ["DB Admin"], ["Database Access"], ["Database Users", "Database Sales"]),
            ("david@example.com", ["DevOps"], ["Deploy Access"], ["SSH address"]),
            ("eve@example.com", ["Owner"], ["Report Access"], ["Report for Shareholders"]),
            ("frank@example.com", ["Developer", "DevOps"], ["API Access", "Deploy Access"], ["API URLs", "SSH keys"]),
        ]

        for email, group_names, perm_names, res_names in users_data:
            user = session.query(User).filter_by(email=email).first()
            if not user:
                user = User(
                    id=uuid4(),
                    email=email,
                    hashed_password=hashed_password,
                    is_active=True,
                    is_superuser=False,
                    is_verified=True,
                    groups=[groups_dict[g] for g in group_names],
                    permissions=[permissions_dict[p] for p in perm_names],
                    resources=[resources_dict[r] for r in res_names],
                )
                session.add(user)
        session.commit()
        logger.info("Users added or verified")

        logger.info("All data seeded successfully")

    except Exception as e:
        session.rollback()
        logger.exception(f"Error seeding data: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed()
