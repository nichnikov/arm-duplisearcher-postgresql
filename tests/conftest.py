import json
import random
import sqlite3
from uuid import uuid4

import pytest
from gensim.matutils import corpus2csc

from config import VOCABULARY_SIZE
from src.utils import fix_path_to_tests


@pytest.fixture(scope="session")
def request_data():
    with open(fix_path_to_tests("static/request_data.json")) as file:
        data = json.load(file)
    return random.sample(data, 100)


@pytest.fixture()
def session():
    connection = sqlite3.connect(":memory:")
    db_session = connection.cursor()
    yield db_session
    connection.close()


@pytest.fixture()
def ids_vectors():
    corpus = [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)],
        [(5, 1), (6, 1), (7, 1), (8, 1)],
    ]
    ids_vectors = [(str(uuid4()), corpus2csc([x], num_terms=VOCABULARY_SIZE)) for x in corpus]
    return ids_vectors
