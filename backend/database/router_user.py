from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import SessionLocal, get_db
from database.schemas import UserResponse, UserCreate, UserUpdate
from typing import List
from database.crud import get_user, create_user, delete_user, update_user, get_users
from apps.jwt import get_current_user_email

router = APIRouter()

@router.post("/users/", response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@router.get("/users/", response_model=List[UserResponse])
def read_all_users_route(db: Session = Depends(get_db), current_email: str = Depends(get_current_user_email)):
    users = get_users(db)
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
def read_user_route(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/users/{user_id}", response_model=UserResponse)
def detele_user_route(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_route(
    user_id: int, user: UserUpdate, db: Session = Depends(get_db)
):
    db_user = update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user