import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.responses import JSONResponse

from src.exceptions.user_define_execptions import NonAlphanumericError, UserNameTooLongError, UserNameAlreadyTaken, \
    FollowingHimselfError, UserNotFound
from src.api.requests.user_request import UserRequest
from src.service.user_service import UserService

app = FastAPI()


@app.post("/users")
def create_user(user: UserRequest):
    try:
        UserService().create_user(user)
    except NonAlphanumericError:
        body = {'description': 'Only alphanumeric characters can be used for username'}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=body)
    except UserNameTooLongError:
        body = {'description': 'Maximum 14 characters for username'}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=body)
    except UserNameAlreadyTaken:
        body = {'description': 'Username already exist'}
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=body)


@app.get("/users/{username}")
def get_user(username: str):
    try:
        return UserService().find_user(username)
    except UserNotFound:
        body = {'description': 'User not found'}
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=body)


@app.get("/users/{username}/follows")
def get_user_followers(username: str):
    return UserService().list_follows(username)


@app.post("/users/{username}/follows")
def create_user_followers(username: str, user: UserRequest):
    try:
        UserService().user_follows(username, user.username)
        return UserService().list_follows(username)
    except FollowingHimselfError:
        body = {'description': 'Cannot follow yourself'}
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=body)


@app.delete("/users/{username}/follows")
def delete_user_followers(username: str, user: UserRequest):
    try:
        UserService().user_unfollows(username, user.username)
        return UserService().list_follows(username)
    except FollowingHimselfError:
        body = {'description': 'Cannot follow yourself'}
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=body)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
