import os

from dotenv import load_dotenv, find_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# from config import get_database_url
load_dotenv(find_dotenv())

DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "ecommerce"
DB_PASSWORD = "postgres"
DB_NAME = "postgres"

# DATABASE_URL = f"{get_database_url()}"
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
