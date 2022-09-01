import json
import random

import pytest
from fastapi.testclient import TestClient
from pytest_postgresql import factories
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app_dupliseacher import app, get_db
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD
from src.texts_storage import Base
from src.utils import fix_path_to_tests

postgresql_dev = factories.postgresql_noproc(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD)


@pytest.fixture(scope="session")
def request_data():
    with open(fix_path_to_tests("static/request_data.json")) as file:
        data = json.load(file)
    return random.sample(data, 100)


@pytest.fixture()
def application(postgresql):
    def get_test_db():
        connection = f"postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}"

        engine = create_engine(connection, echo=True)
        Base.metadata.create_all(bind=engine)
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    return TestClient(app)
