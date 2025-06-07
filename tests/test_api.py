from http import HTTPStatus

import pytest
import requests
import json

from app.models.user import User


@pytest.fixture(scope="module")
def fill_test_data(app_url):
  with open("users.json") as f:
    test_data_users = json.load(f)
  api_users=[]

  for user in test_data_users:
    resp = requests.post(f"{app_url}/api/users", json=user)
    api_users.append(resp.json())

  user_ids = [user["id"] for user in api_users]

  yield user_ids

  for user_id in user_ids:
    requests.delete(f"{app_url}/api/users/{user_id}")

@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()["items"]

#"???
@pytest.fixture
def test_user(app_url):
  with open("users.json") as f:
    user = json.load(f)
  return user

@pytest.mark.usefixtures("fill_test_data")
def test_get_users(app_url):
  resp = requests.get(f"{app_url}/api/users/")
  assert resp.status_code == HTTPStatus.OK

  users_list = resp.json()["items"]
  for user in users_list:
    User.model_validate(user)

def test_get_user(app_url, fill_test_data):
  for user_id in (fill_test_data[0], fill_test_data[-1]):
    resp = requests.get(f"{app_url}/api/users/{user_id}")
    assert resp.status_code == HTTPStatus.OK
    User.model_validate(resp.json())


@pytest.mark.parametrize("user_id", [-1, 00, "dsdsd"])
def test_get_failed_user(app_url, user_id):
  resp = requests.get(f"{app_url}/api/users/{user_id}")

  assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

def test_users_no_duplicates(users, fill_test_data):
  assert len(users) == len(set(fill_test_data))


# TODO move to config default_pagination and move p
def test_pagination_work(app_url, fill_test_data):
  resp = requests.get(f"{app_url}/api/users")

  assert resp.status_code == HTTPStatus.OK
  assert len(resp.json()["items"]) == len(fill_test_data)


def test_pagination_pages(app_url):
  first_page = requests.get(f"{app_url}/api/users/?page=1&size=5")
  second_page = requests.get(f"{app_url}/api/users/?page=2&size=5")

  assert first_page.status_code == HTTPStatus.OK
  assert second_page.status_code == HTTPStatus.OK
  assert first_page.json() != second_page.json()

def test_create_user(app_url, test_user):
  resp = requests.post(f"{app_url}/api/users", json=test_user)
  assert resp.status_code == HTTPStatus.CREATED

  resp_new_user = requests.get(f"{app_url}/api/users{resp.json()['id']}")
  assert resp_new_user.status_code == HTTPStatus.OK
  assert resp_new_user.json()["first_name"] == test_user["first_name"]


def test_update_user(app_url, fill_test_data):
  new_id = fill_test_data[-1] + 1
  resp = requests.get(f"{app_url}/api/user/{new_id}")
  user = resp.json()

