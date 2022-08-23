import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app_dupliseacher import app

pytestmark = pytest.mark.integration


client = TestClient(app)


def test_add(session, request_data):
    response = client.post("/api", json={"operation": "add", "data": request_data})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["quantity"] > 0


def test_update(session, request_data):
    client.post("/api", json={"operation": "add", "data": request_data})
    response = client.post("/api", json={"operation": "update", "data": request_data})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.skip()
def test_search(session, request_data):
    client.post("/api", json={"operation": "add", "data": request_data})
    response = client.post("/api", json={"operation": "search", "data": request_data})
    assert response.status_code == status.HTTP_200_OK


def test_delete(session, request_data):
    client.post("/api", json={"operation": "add", "data": request_data})
    response = client.post("/api", json={"operation": "delete", "data": request_data})
    assert response.status_code == status.HTTP_200_OK


def test_delete_all(session, request_data):
    client.post("/api", json={"operation": "add", "data": request_data})
    response = client.post("/api", json={"operation": "delete_all"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["quantity"] == 0
