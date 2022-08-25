import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app_dupliseacher import app

pytestmark = pytest.mark.integration


client = TestClient(app)


def test_update(request_data):
    response_add = client.post("/api", json={"operation": "add", "data": request_data})
    response_update = client.post("/api", json={"operation": "update", "data": request_data})
    assert response_update.status_code == status.HTTP_200_OK
    assert response_add.json()["quantity"] == response_update.json()["quantity"]


def test_add(request_data):
    response = client.post("/api", json={"operation": "add", "data": request_data})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["quantity"] > 0


def test_search(request_data):
    client.post("/api", json={"operation": "add", "data": request_data})
    response = client.post("/api", json={"operation": "search", "data": request_data})
    assert response.status_code == status.HTTP_200_OK
    for request_item in request_data:
        for response_item in response.json():
            if request_item["id"] == response_item["id"]:
                assert request_item["locale"] == response_item["locale"]
                assert request_item["moduleId"] == response_item["moduleId"]
                for result in response_item["clustersWithDuplicate"]:
                    for duplicate in result["duplicates"]:
                        assert duplicate["pubId"] == request_item["pubIds"]


def test_search_case():
    pass


def test_delete(request_data):
    client.post("/api", json={"operation": "add", "data": request_data})
    response = client.post("/api", json={"operation": "delete", "data": request_data})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["quantity"] == 0


def test_delete_all(request_data):
    client.post("/api", json={"operation": "add", "data": request_data})
    response = client.post("/api", json={"operation": "delete_all"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["quantity"] == 0
