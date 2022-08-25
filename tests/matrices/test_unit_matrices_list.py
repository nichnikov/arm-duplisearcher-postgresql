import pytest

from config import SHARD_SIZE
from src.matrices import MatricesList
from src.types import FastAnswer
from src.utils import data_prepare, transpose

pytestmark = pytest.mark.unit


@pytest.fixture()
def prepared_data(request_data):
    data = list(map(FastAnswer.parse_obj, request_data))
    return data_prepare(data=data)


def test_add(prepared_data):
    matrices_list = MatricesList(max_size=SHARD_SIZE)
    matrices_list.add(data=prepared_data)
    assert matrices_list.quantity == len(prepared_data)


def test_delete(prepared_data):
    prepared_data_t = transpose(prepared_data)
    matrices_list = MatricesList(max_size=SHARD_SIZE)
    matrices_list.add(data=prepared_data)
    matrices_list.delete(ids=prepared_data_t.queryIds)
    assert matrices_list.quantity == 0
    assert len(matrices_list.ids_matrix_list[0].ids) == 0
    assert matrices_list.ids_matrix_list[0].matrix is None


def test_search(prepared_data):
    matrices_list = MatricesList(max_size=SHARD_SIZE)
    matrices_list.add(data=prepared_data)
    results = matrices_list.search(data=prepared_data, min_score=0.99)
    assert len(results) > 0
