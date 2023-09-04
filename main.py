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


@app.get('/posts')
def get_all_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get('/posts/{id}')
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    return post


@app.delete('/posts/{id}')
def delete_post_by_id(id: int, db: Session = Depends(get_db)):
    db.query(models.Post).filter(models.Post.id ==
                                 id).delete(synchronize_session=False)
    db.commit()
    return {"mesg": f'Blog Post with id: {id} deleted successfully.'}


@app.put('/posts/{id}')
def update_post_by_id(id: int, request: schemas.Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        pass
    post.update(request.model_dump())
    db.commit()
    return {"mesg": f'Blog Post with id: {id} successfully updated.'}
