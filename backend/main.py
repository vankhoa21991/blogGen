import uvicorn
from fastapi import FastAPI
from apps.api import api_app
from apps.auth import auth_app
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.mount('/auth', auth_app)
app.mount('/api', api_app)

if __name__ == '__main__':
    uvicorn.run(app, port=7000)
