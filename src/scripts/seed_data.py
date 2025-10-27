from uuid import uuid4

from fastapi_users.password import PasswordHelper
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from src.database.models import Asset, Group, Resource, User  # type: ignore[reportAttributeAccessIssue]
from src.logger import logger

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def seed():
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
        logger.info("Data seeded to tables: 'resources'")

        api = Asset(name="API", resources=[api_urls, api_keys])
        databases = Asset(name="Databases", resources=[db_users, db_goods, db_sales])
        deploy = Asset(name="Deploy", resources=[ssh_addr, ssh_keys])
        reports = Asset(name="Reports", resources=[report_strategy, report_operations, report_shareholders])

        session.add_all([api, databases, deploy, reports])
        session.commit()
        logger.info("Data seeded to tables: 'permissions', 'permissions_resources'")

        developer = Group(name="Developer", permissions=[api, databases])
        db_admin = Group(name="DB Admin", permissions=[databases])
        devops = Group(name="DevOps", permissions=[api, databases, deploy])
        owner = Group(name="Owner", permissions=[reports])

        session.add_all([developer, db_admin, devops, owner])
        session.commit()
        logger.info("Data seeded to tables: 'groups', 'groups_permissions'")

        pwd_helper = PasswordHelper()
        hashed_password = pwd_helper.hash("secure")
        users_data = [
            {"email": "alice@example.com", "password": hashed_password, "groups": [developer]},
            {"email": "bob@example.com", "password": hashed_password, "groups": [developer]},
            {"email": "charlie@example.com", "password": hashed_password, "groups": [db_admin]},
            {"email": "david@example.com", "password": hashed_password, "groups": [devops]},
            {"email": "eve@example.com", "password": hashed_password, "groups": [owner]},
            {"email": "frank@example.com", "password": hashed_password, "groups": [developer, devops]},
        ]

        for udata in users_data:
            user = User(
                id=uuid4(),
                email=udata["email"],
                hashed_password=udata["password"],
                is_active=True,
                is_superuser=False,
                is_verified=True,
                groups=udata["groups"],
            )
            session.add(user)
            session.commit()
        logger.info("Data seeded to tables: 'users', 'users_groups'")

        logger.info("All data seeded successfully")

    except Exception as e:
        session.rollback()
        logger.info("Error seeding data:", e)
    finally:
        session.close()


if __name__ == "__main__":
    seed()
