import json
import random

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app_dupliseacher import app, get_db
from src.schemas import FastAnswer
from src.texts_storage import Base
from src.utils import fix_path_to_tests, data_prepare


@pytest.fixture(scope="session")
def request_data():
    with open(fix_path_to_tests("static/request_data.json")) as file:
        data = json.load(file)
    return random.sample(data, 100)


@pytest.fixture(scope="session")
def prepared_data(request_data):
    data = list(map(FastAnswer.parse_obj, request_data))
    return data_prepare(data=data)


@pytest.fixture()
def session(postgresql):
    connection = (
        f"postgresql://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}"
        + f"/{postgresql.info.dbname}"
    )
    engine = create_engine(connection, echo=True)
    Base.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture()
def application(session):
    app.dependency_overrides[get_db] = lambda: session
    return TestClient(app)
