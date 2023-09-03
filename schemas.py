from pydantic import BaseModel
from typing import List


class Post(BaseModel):
    title: str
    content: str
    tags: List[str]
