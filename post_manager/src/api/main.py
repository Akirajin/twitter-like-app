from typing import Optional

import uvicorn
from fastapi import FastAPI
from starlette import status
from starlette.responses import JSONResponse

from src.api.requests.post_request import PostRequest
from src.exceptions.user_define_execptions import UserNotFound, MessageTooLong, DailyPostLimitReached
from src.service.post_service import PostService

app = FastAPI()


@app.post("/users/{username}/posts")
def create_post(username, post: PostRequest):
    try:
        PostService().create_post(username, post.message, post.ref)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"result": "created"})
    except UserNotFound:
        response = {'description': 'Username does not exist'}
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)
    except MessageTooLong:
        response = {'description': 'Message must be less or equal than 777 characters'}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response)
    except DailyPostLimitReached:
        response = {'description': 'Users cannot create more than 5 messages per day'}
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response)


@app.get("/users/{username}/posts")
def read_post(username):
    try:
        response = PostService().get_posts(username)
        return JSONResponse(status_code=status.HTTP_200_OK, content=response)
    except UserNotFound:
        response = {'description': 'Username does not exist'}
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
