from http import HTTPStatus
from typing import Iterable

from fastapi import APIRouter, Query, Response, HTTPException
from fastapi_pagination import Page as BasePage, add_pagination, paginate
from fastapi_pagination.customization import UseParamsFields, CustomizedPage

from database import users
from app.models.user import User, UserCreate, UserUpdate

router = APIRouter(prefix='/api/users')

# ?page=1&size=5
Page = CustomizedPage[
    BasePage,
    UseParamsFields(
        size=Query(50, ge=0),
    ),
]

@router.get('/{user_id}', status_code=HTTPStatus.OK)
async def get_user(user_id: int, response: Response) -> User :
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user")
    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user

@router.get('/', response_model=Page[User], status_code=HTTPStatus.OK)
async def get_users()-> Page[User]:
    return paginate(users.get_all_users())

@router.post("/", status_code=HTTPStatus.CREATED)
def create_user(user: User) -> User:
    UserCreate.model_validate(user)
    return users.create_user(user)

@router.patch("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id: int, user: User) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user")
    UserUpdate.model_validate(user)
    return users.update_user(user_id, user)

@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user")
    users.delete_user(user_id)
    return {"message":"User deleted"}
