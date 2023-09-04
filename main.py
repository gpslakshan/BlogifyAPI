from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from datetime import datetime
import models
import schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/posts')
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Post(
        title=post.title,
        content=post.content,
        category=post.category,
        created_at=datetime.now()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
