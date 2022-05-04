from typing import Optional

from pydantic import BaseModel


class PostRequest(BaseModel):
    message: str
    ref: Optional[int] = -1
