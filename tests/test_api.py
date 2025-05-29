import requests
import json
from jsonschema import validate


class TestUser:

  # base_url = 'https://reqres.in/api/users'
  base_url = "http://localhost/users"
  headers = {"x-api-key": "reqres-free-v1"}

  def test_get_list_users(self):
    user_id = "2"
    response = requests.get(
    self.base_url + f"/{user_id}",
    headers= self.headers
    )

    assert response.status_code == 200
    assert response.json()['data']['id'] == 2
    with open("tests\get_user.json") as file:
      validate(response.json(), schema=json.loads(file.read()))

  def test_get_failed_user(self):
    user_id = "223"
    response = requests.get(
    self.base_url + f"/{user_id}",
    headers=self.headers
    )

    assert response.status_code == 404


