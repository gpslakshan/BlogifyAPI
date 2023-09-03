from fastapi import FastAPI
from schemas import Post

app = FastAPI()

@app.post('/posts')
def create_post(post: Post):
    return post