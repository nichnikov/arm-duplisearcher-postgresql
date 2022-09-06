from uuid import uuid4

import pytest

from src import Worker, Storage
from src.schemas import Data

pytestmark = pytest.mark.integration


def test_add(session, prepared_data):
    storage = Storage(session=session)
    worker = Worker(storage=storage)

    worker.add(data=prepared_data)
    assert worker.matrix_list.quantity == len(prepared_data)
    assert sorted(storage.get_all()) == sorted(prepared_data)


def test_delete(session, prepared_data):
    storage = Storage(session=session)
    worker = Worker(storage=storage)
    worker.add(data=prepared_data)

    worker.delete(data=prepared_data)
    assert worker.matrix_list.quantity == 0
    assert len(storage.get_all()) == 0


def test_delete_all(session, prepared_data):
    storage = Storage(session=session)
    worker = Worker(storage=storage)
    worker.add(data=prepared_data)

    worker.delete_all()
    assert worker.matrix_list.quantity == 0
    assert len(storage.get_all()) == 0


def test_update(session, prepared_data):
    data_add = prepared_data[0]
    data_update = Data(**{**data_add._asdict(), "query_id": str(uuid4())})

    storage = Storage(session=session)
    worker = Worker(storage=storage)
    worker.add(data=[data_add])
    old_id = worker.matrix_list.ids_matrix_list[0].ids[0]
    old_id_s = storage.get_all()[0].query_id
    assert old_id == old_id_s

    worker.update(data=[data_update])
    new_id = worker.matrix_list.ids_matrix_list[0].ids[0]
    new_id_s = storage.get_all()[0].query_id
    assert new_id_s == new_id_s

    assert old_id != new_id
    assert old_id_s != new_id_s


def test_search(session, prepared_data):
    storage = Storage(session=session)
    worker = Worker(storage=storage)
    worker.add(data=prepared_data)

    result = worker.search(data=[prepared_data[0]], score=0.99)
    assert len(result) == 1
    assert result[0]["clustersWithDuplicate"][0]["duplicates"][0]["cluster"] == prepared_data[0].cluster
