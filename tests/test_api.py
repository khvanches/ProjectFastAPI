from email.policy import default
from http import HTTPStatus

import pytest
import requests
import json

from fastapi_pagination import response
from jsonschema import validate


@pytest.fixture
def users(app_url):
  response = requests.get(f"{app_url}/api/users/")
  assert response.status_code == HTTPStatus.OK
  return response.json()

#headers = {"x-api-key": "reqres-free-v1"}

@pytest.mark.parametrize("user_id", [2, 7, 8])
def test_get_user(app_url, user_id):
  response = requests.get(f"{app_url}/api/users/{user_id}")

  assert response.status_code == 200
  assert response.json()['data']['id'] == user_id
  with open("get_user.json") as file:
    validate(response.json(), schema=json.loads(file.read()))

@pytest.mark.parametrize("user_id", [223, 444, 555])
def test_get_failed_user(app_url, user_id):
  response = requests.get(f"{app_url}/api/users/{user_id}")

  assert response.status_code == HTTPStatus.NOT_FOUND

def test_users_no_duplicates(users):
  user_id = [user["id"] for user in users]
  assert len(users) == len(set(user_id))

# TODO move to config default_pagination and move p
def test_pagination_work(app_url, default_pagination=5):
  response = requests.get(f"{app_url}/api/users")

  assert response.status_code == HTTPStatus.OK
  assert len(response.json()) == default_pagination

def test_pagination_pages(app_url):
  first_page = requests.get(f"{app_url}/api/users/?page=1&size=5")
  second_page = requests.get(f"{app_url}/api/users/?page=2&size=5")

  assert first_page.status_code == HTTPStatus.OK
  assert second_page.status_code == HTTPStatus.OK
  assert first_page.json() != second_page.json()

@pytest.mark.parametrize("size, expected_page_count", [
    (4, 3),  # 12 users, size=4 => 3 pages
    (2, 6),  # 12 users, size=2 => 2 pages
    (5, 3),  # 12 users, size=5 => 3 pages
])
def test_pagination_page_count(app_url, size, expected_page_count):
  response = requests.get(f"{app_url}/api/users/?size={size}")

  assert response.status_code == HTTPStatus.OK
  data = response.json()
  assert data["total"] == 12  # Total 12 users
  assert data["size"] == size
  assert data["pages"] == expected_page_count
