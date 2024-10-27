from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal, get_db
from database.schemas import PostUpdate, PostCreate, PostResponse, UserResponse, PostBase
from typing import List
from database.crud import (get_posts, 
                           get_post_by_id, 
                           get_posts_by_user_id, 
                           get_posts_by_user_email, 
                           create_post, 
                           get_user_by_email,
                           get_recent_posts_by_user_email)

from apps.jwt import get_current_user_email
import datetime

router = APIRouter()

@router.post("/post/", response_model=PostResponse)
def create_post_route(data:PostCreate, db: Session = Depends(get_db), current_email: str = Depends(get_current_user_email)):

    user = get_user_by_email(db, email=current_email)
    post = PostBase(user_id=user.id, user_name=user.name, user_email=user.email, content=data.content, created_at=datetime.datetime.now())
    return create_post(db=db, post=post)

@router.get("/posts/recent", response_model=List[PostResponse])
def get_recent_posts(db: Session = Depends(get_db), limit: int = 3, current_email: str = Depends(get_current_user_email)):
    return get_recent_posts_by_user_email(db, email=current_email, limit=limit)

@router.get("/posts/", response_model=List[PostResponse])
def read_all_posts_route(db: Session = Depends(get_db), current_email: str = Depends(get_current_user_email)):
    posts = get_posts_by_user_email(db, email=current_email)
    return posts

@router.get("/posts/{post_id}", response_model=PostResponse)
def read_post_route(post_id: int, db: Session = Depends(get_db), current_email: str = Depends(get_current_user_email)):
    db_post = get_post_by_id(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.delete("/posts/{post_id}", response_model=PostResponse)
def detele_post_route(post_id: int, db: Session = Depends(get_db), current_email: str = Depends(get_current_user_email)):
    db_post = get_post_by_id(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return db_post

@router.put("/posts/{post_id}", response_model=PostResponse)
def update_post_route(
    post_id: int, post: PostUpdate, db: Session = Depends(get_db), current_email: str = Depends(get_current_user_email)
):
    db_post = get_post_by_id(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.title is not None:
        db_post.title = post.title
    if post.content is not None:
        db_post.content = post.content
    db.commit()
    return db_post

