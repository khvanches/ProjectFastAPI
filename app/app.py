import uvicorn
from fastapi import FastAPI, Response, status
from models.status import Status
from models.user_response import UserResponse


app = FastAPI()

fake_data = [
    {
     "id": 2,
     "email" : "janet.weaver@reqres.in",
     "first_name" : "Janet",
     "last_name" : "Weaver",
     "avatar" : "https://reqres.in/img/faces/2-image.jpg"
     }
]

@app.get('/status')
async def get_status():
    return Status()

@app.get('/users/{user_id}', status_code=200)
async def get_user(user_id: int, response: Response):

    for user in fake_data:
        if user["id"] == user_id:
            return UserResponse(data=user)
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "User not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)