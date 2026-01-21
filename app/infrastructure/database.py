"""
Database configuration module.
Handles SQLAlchemy async engine, session factory, and ORM models.
"""

from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Integer, Numeric, DateTime

from app.core.config import settings


_DATABASE_URL = settings.DATABASE_URL
if _DATABASE_URL.startswith("sqlite:///") and not _DATABASE_URL.startswith("sqlite+aiosqlite://"):
    ASYNC_DATABASE_URL = _DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
else:
    ASYNC_DATABASE_URL = _DATABASE_URL


engine = create_async_engine(ASYNC_DATABASE_URL, echo=False, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database connections."""
    await engine.dispose()
