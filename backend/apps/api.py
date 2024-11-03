from fastapi import Depends
from fastapi import FastAPI
from database.database import engine
import database.models as models
from database.router_user import router as user_router
from apps.jwt import get_current_user_email

models.Base.metadata.create_all(bind=engine)

api_app = FastAPI()
api_app.include_router(router=user_router)

@api_app.get('/')
def test():
    return {'message': 'unprotected api_app endpoint'}


@api_app.get('/protected')
def test2(current_email: str = Depends(get_current_user_email)):
    print(f'Current email: {current_email}')
    return {'message': 'protected api_app endpoint'}
