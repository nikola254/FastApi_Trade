from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData, String, Integer, TIMESTAMP, ForeignKey, Column, Table, JSON, Boolean
from datetime import datetime
from config import DB_PORT, DB_NAME, DB_HOST, DB_USER, DB_PASS
from models.models import role


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    id = Column("id", Integer, primary_key=True)
    email = Column("email", String, nullable=False)
    username = Column("username", String, nullable=False)
    registered_at = Column("registered_at", TIMESTAMP, default=datetime.utcnow)
    role_id = Column("role_id", Integer, ForeignKey(role.c.id))
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active = Column("is_active", Boolean, default=True, nullable=False)
    is_superuser = Column("is_superuser", Boolean, default=False, nullable=False)
    is_verified = Column("is_verified", Boolean, default=False, nullable=False)


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)