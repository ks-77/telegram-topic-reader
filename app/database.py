from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
sync_engine = create_engine(
    DB_URL,
    echo=True,
)
sync_session_maker = sessionmaker(sync_engine, expire_on_commit=False)

Base = declarative_base()
