import pytest

from src.matrices import IdsMatrix

pytestmark = pytest.mark.unit


def test_ids_matrix_add(ids_vectors):
    ids_matrix = IdsMatrix()
    ids_matrix.add(ids_vectors=ids_vectors)
    assert len(ids_matrix.ids) == len(ids_vectors)
    assert len(ids_matrix.ids) == len(ids_vectors)
    assert ids_matrix.matrix.shape[0] == len(ids_vectors)


@pytest.mark.skip()
def test_ids_matrix_delete(ids_vectors):
    ids, _ = zip(*ids_vectors)
    ids_matrix = IdsMatrix()
    ids_matrix.add(ids_vectors=ids_vectors)
    ids_matrix.delete(ids)
    assert ids_matrix.matrix is None
