from pydantic import BaseModel

class SupportData(BaseModel):
    url: str = "https://contentcaddy.io?utm_source=reqres&utm_medium=json&utm_campaign=referral"
    text: str = "Tired of writing endless social media content? Let Content Caddy generate it for you."