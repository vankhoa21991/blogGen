from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database.database import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)

class PostModel(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), index=True)
    user_name = Column(String, index=True)
    user_email = Column(String, index=True)
    user_id = Column(Integer, index=True)
