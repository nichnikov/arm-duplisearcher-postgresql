from uuid import uuid4

import pytest
from gensim.matutils import corpus2csc

from config import VOCABULARY_SIZE
from src.matrices import IdsMatrix

pytestmark = pytest.mark.unit


@pytest.fixture()
def ids_vectors():
    corpus = [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)],
        [(5, 1), (6, 1), (7, 1), (8, 1)],
    ]
    ids_vectors = [(str(uuid4()), corpus2csc([x], num_terms=VOCABULARY_SIZE)) for x in corpus]
    return ids_vectors


def test_ids_matrix_add(ids_vectors):
    ids_matrix = IdsMatrix()
    ids_matrix.add(ids_vectors=ids_vectors)
    assert len(ids_matrix.ids) == len(ids_vectors)
    assert len(ids_matrix.ids) == len(ids_vectors)
    assert ids_matrix.matrix.shape[0] == len(ids_vectors)


def test_ids_matrix_delete(ids_vectors):
    ids, _ = zip(*ids_vectors)
    ids_matrix = IdsMatrix()
    ids_matrix.add(ids_vectors=ids_vectors)
    ids_matrix.delete(ids)
    assert len(ids_matrix.ids) == 0
    assert ids_matrix.matrix is None
