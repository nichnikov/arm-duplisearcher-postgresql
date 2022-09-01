import logging

import pytest
from fastapi import status

pytestmark = pytest.mark.integration

logger = logging.getLogger(__name__)


def test_update(application, request_data):
    response_add = application.post("/api", json={"operation": "add", "data": request_data})
    response_update = application.post("/api", json={"operation": "update", "data": request_data})
    assert response_update.status_code == status.HTTP_200_OK
    assert response_add.json()["quantity"] == response_update.json()["quantity"]


def test_add(application, request_data):
    response = application.post("/api", json={"operation": "add", "data": request_data})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["quantity"] > 0


def test_search(application, request_data):
    application.post("/api", json={"operation": "add", "data": request_data})
    response = application.post("/api", json={"operation": "search", "data": request_data})
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


def test_delete(application, request_data):
    application.post("/api", json={"operation": "add", "data": request_data})
    response = application.post("/api", json={"operation": "delete", "data": request_data})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["quantity"] == 0


def test_delete_all(application, request_data):
    application.post("/api", json={"operation": "add", "data": request_data})
    response = application.post("/api", json={"operation": "delete_all"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["quantity"] == 0
