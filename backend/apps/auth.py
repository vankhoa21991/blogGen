import os
from datetime import datetime

from authlib.integrations.starlette_client import OAuth
from authlib.integrations.starlette_client import OAuthError
from fastapi import FastAPI
from fastapi import Request
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from starlette.responses import HTMLResponse, RedirectResponse

from apps.jwt import create_refresh_token, create_access_token, create_token, CREDENTIALS_EXCEPTION, decode_token, valid_email_from_db, add_email_to_db

# Create the auth app
auth_app = FastAPI()

# OAuth settings
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID') or None
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET') or None
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

# Set up OAuth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID, 'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

# Set up the middleware to read the request session
SECRET_KEY = os.environ.get('SECRET_KEY') or None
if SECRET_KEY is None:
    raise 'Missing SECRET_KEY'
auth_app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Frontend URL:
FRONTEND_URL = os.environ.get('FRONTEND_URL')
BACKEND_URL = os.environ.get('BACKEND_URL')
REDIRECT_LOGIN_URL = BACKEND_URL+'/auth/auth' #os.environ.get('REDIRECT_LOGIN_URL') 
REDIRECT_SIGNUP_URL = BACKEND_URL + '/auth/add' #os.environ.get('REDIRECT_SIGNUP_URL')

@auth_app.route('/login')
async def login(request: Request):
    redirect_uri = REDIRECT_LOGIN_URL  # This creates the url for our /auth endpoint
    print(f'Login request: {request}')
    print("Redirecting to:", redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)

@auth_app.get('/signup')
async def signup(request: Request):
    redirect_uri = REDIRECT_SIGNUP_URL
    return await oauth.google.authorize_redirect(request, redirect_uri)

@auth_app.get('/auth')
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    # Parse user information from ID token
    user_data = await oauth.google.parse_id_token(request, token)
    if valid_email_from_db(user_data['email']):
        print('Email exists in db')
        # Create access and refresh tokens for the user
        access_token = create_token(user_data['email'])
        refresh_token = create_refresh_token(user_data['email'])

        # Redirect to Streamlit with the tokens in query parameters
        redirect_url = f"{FRONTEND_URL}/?" + get_response(access_token, refresh_token, user_data['name'])
    else:
        # If email is not valid, redirect to the signup page with the email in query parameters
        redirect_url = f"{FRONTEND_URL}/?state=signup&email={user_data['email']}&name={user_data['name']}"
    return RedirectResponse(url=redirect_url)
    

@auth_app.get('/add')
async def add(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return HTMLResponse(f'<h1>{error.error}</h1>')
    # Parse user information from ID token
    user_data = await oauth.google.parse_id_token(request, token)
    if valid_email_from_db(user_data['email']):
        print('Email already in db')
        # # Create access and refresh tokens for the user
        # access_token = create_token(user_data['email'])
        # refresh_token = create_refresh_token(user_data['email'])

        # # Redirect to Streamlit with the tokens in query parameters
        # redirect_url = f"{FRONTEND_URL}/?" + get_response(access_token, refresh_token, user_data['name'])
        # return RedirectResponse(url=redirect_url)
    else:
        print('Adding email to db')
        add_email_to_db(user_data['email'], user_data['name'])

    access_token = create_token(user_data['email'])
    refresh_token = create_refresh_token(user_data['email'])
    redirect_url = f"{FRONTEND_URL}/?" + get_response(access_token, refresh_token, user_data['name'])
    return RedirectResponse(url=redirect_url)

def get_response(access_token, refresh_token, name, **kwargs):
    return f'access_token={access_token}&refresh_token={refresh_token}&name={name}'

@auth_app.post('/refresh')
async def refresh(request: Request):
    try:
        # Only accept post requests
        if request.method == 'POST':
            form = await request.json()
            if form.get('grant_type') == 'refresh_token':
                token = form.get('refresh_token')
                payload = decode_token(token)
                # Check if token is not expired
                if datetime.utcfromtimestamp(payload.get('exp')) > datetime.utcnow():
                    email = payload.get('sub')
                    # Validate email
                    if valid_email_from_db(email):
                        # Create and return token
                        return JSONResponse({'result': True, 'access_token': create_token(email)})

    except Exception:
        raise CREDENTIALS_EXCEPTION
    raise CREDENTIALS_EXCEPTION
