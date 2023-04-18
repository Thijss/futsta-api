"""Unit tests for the goals router."""
# pylint: disable=missing-function-docstring
import os
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


_GOALS_URL = "goals/"


def test_get_by_match_date_no_api_key():
    response = client.get(f"{_GOALS_URL}2023-03-03")
    assert response.status_code == 403


def test_get_by_match_date_unauthorized():
    headers = {"ApiKey": "NOT READ"}
    response = client.get(f"{_GOALS_URL}2023-03-03", headers=headers)
    assert response.status_code == 401


def test_get_by_match_date_authorized():
    headers = {"ApiKey": "READ"}

    with patch.dict(os.environ, {"api_key_read_access": "READ", "local_access": "read"}):
        response = client.get(f"{_GOALS_URL}2023-03-03", headers=headers)
    assert response.status_code == 200
