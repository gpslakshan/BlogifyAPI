from fastapi import FastAPI
from schemas import Post
from database import engine
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.post('/posts')
def create_post(post: Post):
    return post
