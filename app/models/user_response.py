from pydantic import BaseModel
from .user import User
from .support_data import SupportData

class UserResponse(BaseModel):
    data: User
    support: SupportData = SupportData()