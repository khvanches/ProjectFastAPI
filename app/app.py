from http import HTTPStatus

import uvicorn
import json
from fastapi import FastAPI, Response, status, Query
from fastapi_pagination import Page as BasePage, add_pagination, paginate
from fastapi_pagination.customization import UseParamsFields, CustomizedPage

from models.user_data import UserData
from models.status import Status
from models.user_response import UserResponse

# ?page=1&size=5
Page = CustomizedPage[
    BasePage,
    UseParamsFields(
        size=Query(5, ge=0),
    ),
]

app = FastAPI()
add_pagination(app)

users = list[UserData]

@app.get('/status', status_code=HTTPStatus.OK)
async def get_status() -> Status:
    return  Status(users=bool(users))

@app.get('/api/users/{user_id}', status_code=200)
async def get_user(user_id: int, response: Response) -> UserResponse | dict[str, str]:

    for user in users:
        if user["id"] == user_id:
            return UserResponse(data=user)
    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error" : "User not found"}


@app.get('/api/users/', status_code=200)
async def get_users()-> Page[UserData]:
    return paginate(users)

if __name__ == "__main__":
    with open ("users.json") as f:
        users = json.load(f)

    for user in users:
        UserData.model_validate(user)

    print("Users have been loaded")

    uvicorn.run(app, host="0.0.0.0", port=8081)