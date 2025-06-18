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

@pytest.fixture(scope="module")
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()["items"]

@pytest.fixture(scope="module")
def users_for_tests(app_url):
  with open("test_users.json") as f:
    users_for_tests = json.load(f)
    return users_for_tests

@pytest.fixture(scope='module')
def deleted_user(app_url, users_for_tests):
  user_data = users_for_tests["valid_user"]
  resp = requests.post(f"{app_url}/api/users", json=user_data)
  user_id = resp.json()["id"]
  resp = requests.delete(f"{app_url}/api/users/{user_id}")
  return user_id

@pytest.mark.usefixtures("fill_test_data")
def test_users_no_duplicates(users, fill_test_data):
  assert len(users) == len(set(fill_test_data))

@pytest.mark.usefixtures("fill_test_data")
def test_get_users_ok(app_url):
  resp = requests.get(f"{app_url}/api/users/")
  assert resp.status_code == HTTPStatus.OK

  users_list = resp.json()["items"]
  for user in users_list:
    User.model_validate(user)

def test_get_user_ok(app_url, fill_test_data):
  for user_id in (fill_test_data[0], fill_test_data[-1]):
    resp = requests.get(f"{app_url}/api/users/{user_id}")
    assert resp.status_code == HTTPStatus.OK
    User.model_validate(resp.json())

@pytest.mark.parametrize("user_id", [-1, 00, "dsdsd"])
def test_get_invalid_id_returns_422(app_url, user_id):
  resp = requests.get(f"{app_url}/api/users/{user_id}")

  assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

@pytest.mark.parametrize("user_id", [-1, 00, "dsdsd"])
def test_delete_invalid_id_returns_422(app_url, user_id):
  resp = requests.delete(f"{app_url}/api/users/{user_id}")

  assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

@pytest.mark.parametrize("user_id", [-1, 00, "dsdsd"])
@pytest.mark.usefixtures("users_for_tests")
def test_patch_invalid_id_returns_422(app_url, user_id, users_for_tests):
  user_data = users_for_tests["valid_user"]
  resp = requests.patch(f"{app_url}/api/users/{user_id}", json=user_data)
  assert resp.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

def test_put_method_not_allowed(app_url, fill_test_data):
  resp = requests.put(f"{app_url}/api/users/{fill_test_data[0]}")
  assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test_options_not_allowed(app_url, fill_test_data):
  resp = requests.options(f"{app_url}/api/users/{fill_test_data[0]}")
  assert resp.status_code == HTTPStatus.METHOD_NOT_ALLOWED

# Test CRUD user
@pytest.mark.usefixtures("users_for_tests")
def test_crud_user(app_url, users_for_tests):
  user_data = users_for_tests["valid_user"]
  resp = requests.post(f"{app_url}/api/users/", json=user_data)
  assert  resp.status_code == HTTPStatus.CREATED
  user = resp.json()

  resp = requests.get(f"{app_url}/api/users/{user["id"]}")
  assert  resp.status_code == HTTPStatus.OK
  user = resp.json()
  assert user_data["first_name"] == user["first_name"]

  update_data = users_for_tests["change_user"]
  resp = requests.patch(f"{app_url}/api/users/{user["id"]}", json=update_data)
  assert resp.status_code == HTTPStatus.OK
  user = resp.json()
  assert user_data["first_name"] != user["first_name"]
  assert user_data["email"] != user["email"]

  resp = requests.delete(f"{app_url}/api/users/{user["id"]}")
  assert resp.status_code == HTTPStatus.OK
  resp = requests.get(f"{app_url}/api/users/{user["id"]}")
  assert resp.status_code == HTTPStatus.NOT_FOUND

def test_create_user_bad_email(app_url, users_for_tests):
  user_data = users_for_tests["bad_email_user"]
  resp = requests.post(f"{app_url}/api/users/", json=user_data)
  assert  resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

def test_create_incomplete_user(app_url, users_for_tests):
  user_data = users_for_tests["bad_url_user"]
  resp = requests.post(f"{app_url}/api/users/", json=user_data)
  assert resp.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

@pytest.mark.usefixtures("deleted_user")
def test_get_deleted_user(app_url, deleted_user):
  resp = requests.get(f"{app_url}/api/users/{deleted_user}")
  assert resp.status_code == HTTPStatus.NOT_FOUND

@pytest.mark.usefixtures("deleted_user")
def test_patch_deleted_user(app_url, deleted_user, users_for_tests):
  user_data = users_for_tests["change_user"]
  resp = requests.patch(f"{app_url}/api/users/{deleted_user}", json=user_data)
  assert resp.status_code == HTTPStatus.NOT_FOUND

@pytest.mark.usefixtures("deleted_user")
def test_delete_deleted_user(app_url, deleted_user):
  resp = requests.delete(f"{app_url}/api/users/{deleted_user}")
  assert resp.status_code == HTTPStatus.NOT_FOUND