from http import HTTPStatus

from fastapi import APIRouter

from app.models.status import Status
from app.database.engine import check_availability

router = APIRouter()

@router.get('/status', status_code=HTTPStatus.OK)
async def get_status() -> Status:
    return  Status(database=check_availability())