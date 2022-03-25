import psycopg2
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine

from migrations import downgrade_migrations, upgrade_migrations
from models import TalkRequest  # noqa: F401
from web_app.config import load_config
from web_app.main import app, get_session


@pytest.fixture(scope="session")
def database():
    dsn_parts = load_config().SQLMODEL_DATABASE_URI.split("/")
    database_name = dsn_parts[-1]
    dsn = "/".join(
        dsn_parts[:-1] + ["postgres"]
    )  # to login to postgres database instead of application one
    con = psycopg2.connect(dsn)
    con.autocommit = True
    cur = con.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {database_name};")
    cur.execute(f"CREATE DATABASE {database_name};")


@pytest.fixture(name="session")
def database_session(database):
    dsn = load_config().SQLMODEL_DATABASE_URI
    engine = create_engine(dsn)
    # SQLModel.metadata.create_all(engine)
    upgrade_migrations(dsn)
    with Session(engine) as session:
        yield session
    downgrade_migrations(dsn)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
