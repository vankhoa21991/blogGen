import os
from datetime import datetime
from datetime import timedelta
import json
from dotenv import load_dotenv
load_dotenv()
import jwt
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.database import SessionLocal, get_db
from database.schemas import UserResponse, UserCreate, UserUpdate
from database.crud import create_user, get_users

# from apps.db import is_token_blacklisted

# Helper to read numbers using var envs
def cast_to_number(id):
    temp = os.environ.get(id)
    if temp is not None:
        try:
            return float(temp)
        except ValueError:
            return None
    return None


# Configuration
API_SECRET_KEY = os.environ.get('API_SECRET_KEY')
if API_SECRET_KEY is None:
    raise BaseException('Missing API_SECRET_KEY env var.')
API_ALGORITHM = os.environ.get('API_ALGORITHM') or 'HS256'
API_ACCESS_TOKEN_EXPIRE_MINUTES = cast_to_number('API_ACCESS_TOKEN_EXPIRE_MINUTES') or 15
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 30

# Token url (We should later create a token url that accepts just a user and a password to use swagger)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

# Error
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


# Create token internal function
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, API_SECRET_KEY, algorithm=API_ALGORITHM)
    return encoded_jwt


def create_refresh_token(email):
    expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data={'sub': email}, expires_delta=expires)


# Create token for an email
def create_token(email):
    access_token_expires = timedelta(minutes=API_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={'sub': email}, expires_delta=access_token_expires)
    return access_token


def valid_email_from_db(email):
    db_session = next(get_db())
    
    try:
        users = get_users(db=db_session)  # Fetch users from the database
        for user in users:
            if user.email == email:
                return True
    finally:
        db_session.close()  # Make sure to close the session

    return False


def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

def add_email_to_db(email, name):
    print('Adding email to db')
    user = UserCreate(name=name, email=email)
    db = next(get_db())
    try:
        create_user(db, user)
    finally:
        db.close()

def decode_token(token):
    return jwt.decode(token, API_SECRET_KEY, algorithms=[API_ALGORITHM])


async def get_current_user_email(token: str = Depends(oauth2_scheme)):
    # if is_token_blacklisted(token):
    #     raise CREDENTIALS_EXCEPTION
    try:
        payload = decode_token(token)
        email: str = payload.get('sub')
        if email is None:
            raise CREDENTIALS_EXCEPTION
    except jwt.PyJWTError:
        raise CREDENTIALS_EXCEPTION

    if valid_email_from_db(email):
        return email

    raise CREDENTIALS_EXCEPTION


async def get_current_user_token(token: str = Depends(oauth2_scheme)):
    _ = await get_current_user_email(token)
    return token
