from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from google.cloud.sql.connector import Connector, IPTypes

from dotenv import load_dotenv
load_dotenv()
import os 

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Connect to the database
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

def init_connection_engine(connector: Connector) -> Engine:
    # if env var PRIVATE_IP is set to True, use private IP Cloud SQL connections
    ip_type = IPTypes.PRIVATE if os.getenv("PRIVATE_IP") is True else IPTypes.PUBLIC
    # if env var DB_IAM_USER is set, use IAM database authentication
    user, enable_iam_auth = (
        (os.getenv("DB_IAM_USER"), True)
        if os.getenv("DB_IAM_USER")
        else (os.getenv("DB_USER"), False)
    )

    # Cloud SQL Python Connector creator function
    def getconn():
        conn = connector.connect(
            os.getenv("INSTANCE_CONNECTION_NAME"),
            "pg8000",
            user=user,
            password=os.getenv("DB_PASS", ""),
            db=os.getenv("DB_NAME"),
            ip_type=ip_type,
            enable_iam_auth=enable_iam_auth,
        )
        return conn

    SQLALCHEMY_DATABASE_URL = "postgresql+pg8000://"

    engine = create_engine(SQLALCHEMY_DATABASE_URL, creator=getconn)
    return engine

# Create the engine
engine = init_connection_engine(Connector())

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
