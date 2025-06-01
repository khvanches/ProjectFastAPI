from http import HTTPStatus

import pytest

import requests

def test_check_status(app_url):
    response = requests.get(f"{app_url}/status")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["users"] == True
