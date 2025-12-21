"""Pytest configuration and fixtures."""
import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.session import get_db
from app.models.base import Base


# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    # Create async engine with in-memory SQLite
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session factory
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session

    # Drop all tables after test
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with overridden database dependency."""

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def sync_client() -> TestClient:
    """Create a synchronous test client."""
    return TestClient(app)


# Sample test data fixtures
@pytest.fixture
def sample_user_data() -> dict:
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "name": "Test User",
        "password": "SecurePassword123",
        "role": "admin",
    }


@pytest.fixture
def sample_service_data() -> dict:
    """Sample service data for testing."""
    return {
        "title": "Test Service",
        "slug": "test-service",
        "description": "This is a test service description that is long enough.",
        "short_description": "Brief test description",
        "features": ["Feature 1", "Feature 2"],
        "cta_text": "Get Started",
        "featured": True,
    }


@pytest.fixture
def sample_blog_post_data() -> dict:
    """Sample blog post data for testing."""
    return {
        "title": "Test Blog Post",
        "slug": "test-blog-post",
        "content": "This is the full content of the test blog post. It needs to be long enough.",
        "excerpt": "Brief excerpt",
        "status": "published",
        "featured": False,
    }


@pytest.fixture
def sample_contact_data() -> dict:
    """Sample contact inquiry data for testing."""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "company": "Test Company",
        "subject": "Test Inquiry",
        "message": "This is a test message that is long enough for validation.",
    }

