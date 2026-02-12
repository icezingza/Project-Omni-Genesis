"""
Project Omni-Genesis: Database Setup
SQLAlchemy async database engine, session management, and Base class.
Defaults to SQLite for development; set DATABASE_URL for PostgreSQL.
"""

import logging
from typing import AsyncGenerator

from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from .config import settings

logger = logging.getLogger("omni_genesis.database")


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


# --- Engine ---
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

# --- Session Factory ---
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a database session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Create all database tables (for development/testing)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created")


async def close_db() -> None:
    """Dispose of the database engine."""
    await engine.dispose()
    logger.info("Database connection closed")
