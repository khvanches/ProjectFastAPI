from pydantic import BaseModel
from models.user_data import UserData
from models.support_data import SupportData

class UserResponse(BaseModel):
    data: UserData
    support: SupportData = SupportData()