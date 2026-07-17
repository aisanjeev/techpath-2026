"""Database session management with SQLite/MySQL auto-detection."""
import logging
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.config import settings

logger = logging.getLogger(__name__)


def get_engine_args() -> dict:
    """Get engine arguments based on database type."""
    if settings.is_sqlite:
        # SQLite specific configuration
        return {
            "connect_args": {"check_same_thread": False},
            "poolclass": StaticPool,
            "echo": settings.DATABASE_ECHO,
        }
    else:
        # MySQL/PostgreSQL configuration
        return {
            "echo": settings.DATABASE_ECHO,
            "pool_pre_ping": True,
            "pool_size": 5,
            "max_overflow": 10,
        }


# Create async engine with appropriate settings
engine = create_async_engine(
    settings.DATABASE_URL,
    **get_engine_args(),
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides a database session.

    Yields:
        AsyncSession: Database session

    Usage:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Verify database connectivity on application startup.

    Schema is owned exclusively by Alembic; run ``alembic upgrade heads`` to create or
    migrate tables. This deliberately does not call ``Base.metadata.create_all``: doing
    so masked schema drift by silently conjuring missing tables, which let the migration
    history diverge unnoticed.
    """
    logger.info(f"Initializing database: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else settings.DATABASE_URL}")
    logger.info(f"Database type: {'SQLite' if settings.is_sqlite else 'MySQL'}")

    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    logger.info("Database connection verified")

