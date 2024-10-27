from sqlalchemy.orm import Session
from database.schemas import UserCreate, UserUpdate, PostCreate, PostUpdate, PostResponse
from database.models import  UserModel, PostModel


def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_users(db: Session):
    return db.query(UserModel).all()

def create_user(db: Session, user: UserCreate):
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if db_user is None:
        return None

    if user.name is not None:
        db_user.name = user.name
    if user.email is not None:
        db_user.email = user.email

    db.commit()
    return db_user

def get_posts(db: Session):
    return db.query(PostModel).all()

def get_post_by_id(db: Session, post_id: int):
    return db.query(PostModel).filter(PostModel.id == post_id).first()

def get_posts_by_user_id(db: Session, user_id: int):
    return db.query(PostModel).filter(PostModel.user_id == user_id).all()

def get_posts_by_user_email(db: Session, email: str):
    return db.query(PostModel).filter(PostModel.user_email == email).all()

def get_recent_posts_by_user_email(db: Session, email: str, limit: int):
    return db.query(PostModel).filter(PostModel.user_email == email).order_by(PostModel.created_at.desc()).limit(limit).all()

def create_post(db: Session, post: PostCreate):
    db_post = PostModel(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
    db.delete(db_post)
    db.commit()
    return db_post

def update_post(db: Session, post_id: int, post: PostUpdate):
    db_post = db.query(PostModel).filter(PostModel.id == post_id).first()

    if db_post is None:
        return None

    if post.content is not None:
        db_post.content = post.content

    db.commit()
    return db_post



