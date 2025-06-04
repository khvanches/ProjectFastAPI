from http import HTTPStatus

from fastapi import APIRouter

from models.status import Status
# from database import users_db

router = APIRouter()

@router.get('/status', status_code=HTTPStatus.OK)
async def get_status() -> Status:
    return  Status(users=True)