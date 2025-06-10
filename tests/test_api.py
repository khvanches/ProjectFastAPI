from email.policy import default
from http import HTTPStatus

import pytest
import requests
import json
import math

from jsonschema import validate


@pytest.fixture
def users(app_url):
  response = requests.get(f"{app_url}/api/users/")
  assert response.status_code == HTTPStatus.OK

  users = []
  data = response.json()
  for i in range(1,data["pages"]+1):
    response = requests.get(f"{app_url}/api/users/?page={i}")
    for item in response.json()["items"]:
      users.append(item)
  return users


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

def test_pagination_work(app_url, default_pagination, users):
  response = requests.get(f"{app_url}/api/users")

  assert response.status_code == HTTPStatus.OK
  data = response.json()
  assert len(data['items']) == default_pagination
  assert data['total'] == len(users)
  assert data['page'] == 1
  assert data['pages'] == math.ceil(len(users)/default_pagination)
  assert data['size'] == default_pagination

def test_pagination_pages(app_url):
  first_page = requests.get(f"{app_url}/api/users/?page=1&size=5")
  second_page = requests.get(f"{app_url}/api/users/?page=2&size=5")

  assert first_page.status_code == HTTPStatus.OK
  assert second_page.status_code == HTTPStatus.OK

  items_1 = first_page.json()["items"]
  items_2 = second_page.json()["items"]

  assert items_1 != items_2
  assert not all(i1 == i2 for i1, i2 in zip(items_1, items_2))


@pytest.mark.parametrize("size", [3, 5, 8] )
def test_pagination_page_count(app_url, users, size):
  response = requests.get(f"{app_url}/api/users/?size={size}")
  assert response.status_code == HTTPStatus.OK

  data = response.json()
  assert data["total"] == len(users)  # Total 12 users
  assert data["size"] == size
  assert data["pages"] == math.ceil(len(users)/size)
