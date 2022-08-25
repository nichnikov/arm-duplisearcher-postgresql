import json
import random

import pytest

from src.utils import fix_path_to_tests


@pytest.fixture(scope="session")
def request_data():
    with open(fix_path_to_tests("static/request_data.json")) as file:
        data = json.load(file)
    return random.sample(data, 100)
