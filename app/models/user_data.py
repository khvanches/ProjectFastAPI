from pydantic import BaseModel, EmailStr, HttpUrl

class UserData(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    avatar: HttpUrl