import pytest

from src.schemas import Data
from src.texts_storage import Storage, Query
from src.utils import transpose

pytestmark = pytest.mark.unit


def test_add(session, prepared_data):
    storage = Storage(session=session)

    storage.add(data=prepared_data)
    result = storage.session.query(Query).all()
    assert all(isinstance(item, Query) for item in result)
    assert len(result) == len(prepared_data)


def test_search_by_answers(session, prepared_data):
    storage = Storage(session=session)
    storage.add(data=prepared_data)
    prepared_data_t = transpose(data=prepared_data)

    result = storage.search_by_answers(ids=prepared_data_t.answer_ids)
    assert len(result) == len(prepared_data)
    assert all(isinstance(item, Data) for item in result)
    assert sorted(result) == sorted(prepared_data)


def test_search_by_queries(session, prepared_data):
    storage = Storage(session=session)
    storage.add(data=prepared_data)
    prepared_data_t = transpose(data=prepared_data)

    result = storage.search_by_queries(ids=prepared_data_t.query_ids)
    assert len(result) == len(prepared_data)
    assert all(isinstance(item, Data) for item in result)
    assert sorted(result) == sorted(prepared_data)


def test_delete_by_queries(session, prepared_data):
    storage = Storage(session=session)
    storage.add(data=prepared_data)
    prepared_data_t = transpose(data=prepared_data)

    storage.delete_by_queries(ids=prepared_data_t.query_ids)
    result = storage.session.query(Query).all()
    assert isinstance(result, list)
    assert len(result) == 0


def test_delete_all(session, prepared_data):
    storage = Storage(session=session)
    storage.add(data=prepared_data)

    storage.delete_all()
    result = storage.session.query(Query).all()
    assert isinstance(result, list)
    assert len(result) == 0


def test_get_all(session, prepared_data):
    storage = Storage(session=session)
    storage.add(data=prepared_data)

    result = storage.get_all()
    assert all(isinstance(item, Data) for item in result)
    assert len(result) == len(prepared_data)
    assert sorted(result) == sorted(prepared_data)
