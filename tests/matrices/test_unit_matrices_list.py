import pytest

from config import SHARD_SIZE
from src.matrices import MatricesList

pytestmark = pytest.mark.unit


def test_add(ids_vectors):
    matrices_list = MatricesList(max_size=SHARD_SIZE)
    matrices_list.add(ids_vectors=ids_vectors)
    assert matrices_list.quantity == len(ids_vectors)


@pytest.mark.skip()
def test_delete(ids_vectors):
    ids, _ = zip(*ids_vectors)
    matrices_list = MatricesList(max_size=SHARD_SIZE)
    matrices_list.add(ids_vectors=ids_vectors)
    matrices_list.delete(ids=ids)
    assert matrices_list.quantity == 0


def test_search(ids_vectors):
    matrices_list = MatricesList(max_size=SHARD_SIZE)
    matrices_list.add(ids_vectors=ids_vectors)
    result = matrices_list.search(searched_vectors=ids_vectors, min_score=0.99)
    assert result is not None
    assert len(result) == len(ids_vectors)
