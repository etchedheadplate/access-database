from uuid import uuid4

from fastapi_users.password import PasswordHelper
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from src.database.models import (
    Base,
    Group,
    Permission,
    Resource,
    User,
)
from src.logger import logger

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def seed():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    try:
        api_urls = Resource(name="API URLs")
        api_keys = Resource(name="API keys")

        db_users = Resource(name="Database Users")
        db_goods = Resource(name="Database Goods")
        db_sales = Resource(name="Database Sales")

        ssh_addr = Resource(name="SSH address")
        ssh_keys = Resource(name="SSH keys")

        report_strategy = Resource(name="Report on Strategy")
        report_operations = Resource(name="Report on Operations")
        report_shareholders = Resource(name="Report for Shareholders")

        session.add_all(
            [
                api_urls,
                api_keys,
                db_users,
                db_goods,
                db_sales,
                ssh_addr,
                ssh_keys,
                report_strategy,
                report_operations,
                report_shareholders,
            ]
        )
        session.commit()
        logger.info("Resources added")

        perm_api = Permission(name="API Access", resources=[api_urls, api_keys])
        perm_db = Permission(name="Database Access", resources=[db_users, db_goods, db_sales])
        perm_deploy = Permission(name="Deploy Access", resources=[ssh_addr, ssh_keys])
        perm_reports = Permission(
            name="Report Access", resources=[report_strategy, report_operations, report_shareholders]
        )

        session.add_all([perm_api, perm_db, perm_deploy, perm_reports])
        session.commit()
        logger.info("Permissions added")

        developer = Group(
            name="Developer",
            permissions=[perm_api, perm_db],
            resources=[api_urls, db_goods],
        )
        db_admin = Group(
            name="DB Admin",
            permissions=[perm_db],
            resources=[db_users, db_sales],
        )
        devops = Group(
            name="DevOps",
            permissions=[perm_api, perm_db, perm_deploy],
            resources=[ssh_addr],
        )
        owner = Group(
            name="Owner",
            permissions=[perm_reports],
            resources=[report_strategy, report_shareholders],
        )

        session.add_all([developer, db_admin, devops, owner])
        session.commit()

        pwd_helper = PasswordHelper()
        hashed_password = pwd_helper.hash("secure")

        users_data = [
            {
                "email": "alice@example.com",
                "groups": [developer],
                "permissions": [perm_api],
                "resources": [api_urls],
            },
            {
                "email": "bob@example.com",
                "groups": [developer],
                "permissions": [perm_api, perm_db],
                "resources": [api_keys, db_goods],
            },
            {
                "email": "charlie@example.com",
                "groups": [db_admin],
                "permissions": [perm_db],
                "resources": [db_users, db_sales],
            },
            {
                "email": "david@example.com",
                "groups": [devops],
                "permissions": [perm_deploy],
                "resources": [ssh_addr],
            },
            {
                "email": "eve@example.com",
                "groups": [owner],
                "permissions": [perm_reports],
                "resources": [report_shareholders],
            },
            {
                "email": "frank@example.com",
                "groups": [developer, devops],
                "permissions": [perm_api, perm_deploy],
                "resources": [api_urls, ssh_keys],
            },
        ]

        for data in users_data:
            user = User(
                id=uuid4(),
                email=data["email"],
                hashed_password=hashed_password,
                is_active=True,
                is_superuser=False,
                is_verified=True,
                groups=data["groups"],
                permissions=data["permissions"],
                resources=data["resources"],
            )
            session.add(user)

        session.commit()
        logger.info("Users added")

        logger.info("All data seeded successfully")

    except Exception as e:
        session.rollback()
        logger.exception(f"❌ Error seeding data: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed()
