"""Tests for spam protection on the public contact/newsletter endpoints.

Covers the honeypot silent-discard, per-IP rate limiting, and Turnstile
verification gating on POST /api/v1/contact/ and /api/v1/contact/newsletter.
"""

from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints import contact as contact_endpoint
from app.models.contact import ContactInquiry, NewsletterSubscriber


@pytest.fixture(autouse=True)
def reset_rate_limiters():
    """The limiters are module-level and in-memory; isolate tests from each other."""
    contact_endpoint._contact_limiter._hits.clear()
    contact_endpoint._newsletter_limiter._hits.clear()
    yield
    contact_endpoint._contact_limiter._hits.clear()
    contact_endpoint._newsletter_limiter._hits.clear()


@pytest.mark.asyncio
async def test_contact_submission_succeeds_without_turnstile_configured(
    client: AsyncClient, test_db: AsyncSession, sample_contact_data: dict
):
    """With no TURNSTILE_SECRET_KEY set, a normal submission is accepted."""
    response = await client.post("/api/v1/contact/", json=sample_contact_data)
    assert response.status_code == 201

    result = await test_db.execute(select(ContactInquiry))
    inquiries = list(result.scalars().all())
    assert len(inquiries) == 1
    assert inquiries[0].email == sample_contact_data["email"]


@pytest.mark.asyncio
async def test_honeypot_returns_success_but_discards(
    client: AsyncClient, test_db: AsyncSession, sample_contact_data: dict
):
    """A filled honeypot field gets the normal success response, saves nothing."""
    response = await client.post(
        "/api/v1/contact/", json={**sample_contact_data, "website": "https://spam.example"}
    )
    assert response.status_code == 201  # indistinguishable from success

    result = await test_db.execute(select(ContactInquiry))
    assert list(result.scalars().all()) == []


@pytest.mark.asyncio
async def test_newsletter_honeypot_discards(client: AsyncClient, test_db: AsyncSession):
    response = await client.post(
        "/api/v1/contact/newsletter",
        json={"email": "bot@example.com", "website": "spam"},
    )
    assert response.status_code == 201

    result = await test_db.execute(select(NewsletterSubscriber))
    assert list(result.scalars().all()) == []


@pytest.mark.asyncio
async def test_contact_rate_limit(client: AsyncClient, sample_contact_data: dict):
    """The 6th submission from the same IP within the window is rejected."""
    limit = contact_endpoint._contact_limiter.max_hits
    for _ in range(limit):
        response = await client.post("/api/v1/contact/", json=sample_contact_data)
        assert response.status_code == 201

    response = await client.post("/api/v1/contact/", json=sample_contact_data)
    assert response.status_code == 429


@pytest.mark.asyncio
async def test_turnstile_missing_token_rejected(
    client: AsyncClient, test_db: AsyncSession, sample_contact_data: dict
):
    """When Turnstile is configured, a submission without a token is rejected."""
    with patch.object(contact_endpoint.settings, "TURNSTILE_SECRET_KEY", "test-secret"):
        response = await client.post("/api/v1/contact/", json=sample_contact_data)

    assert response.status_code == 403

    result = await test_db.execute(select(ContactInquiry))
    assert list(result.scalars().all()) == []


@pytest.mark.asyncio
async def test_turnstile_valid_token_accepted(
    client: AsyncClient, test_db: AsyncSession, sample_contact_data: dict
):
    """A submission with a token Cloudflare accepts goes through."""
    with (
        patch.object(contact_endpoint.settings, "TURNSTILE_SECRET_KEY", "test-secret"),
        patch("app.services.turnstile.httpx.AsyncClient") as mock_client_cls,
    ):
        mock_response = AsyncMock()
        mock_response.raise_for_status = lambda: None
        mock_response.json = lambda: {"success": True}
        mock_client = mock_client_cls.return_value.__aenter__.return_value
        mock_client.post = AsyncMock(return_value=mock_response)

        response = await client.post(
            "/api/v1/contact/",
            json={**sample_contact_data, "turnstile_token": "valid-token"},
        )

    assert response.status_code == 201
    result = await test_db.execute(select(ContactInquiry))
    assert len(list(result.scalars().all())) == 1


@pytest.mark.asyncio
async def test_turnstile_invalid_token_rejected(
    client: AsyncClient, test_db: AsyncSession, sample_contact_data: dict
):
    with (
        patch.object(contact_endpoint.settings, "TURNSTILE_SECRET_KEY", "test-secret"),
        patch("app.services.turnstile.httpx.AsyncClient") as mock_client_cls,
    ):
        mock_response = AsyncMock()
        mock_response.raise_for_status = lambda: None
        mock_response.json = lambda: {"success": False, "error-codes": ["invalid-input-response"]}
        mock_client = mock_client_cls.return_value.__aenter__.return_value
        mock_client.post = AsyncMock(return_value=mock_response)

        response = await client.post(
            "/api/v1/contact/",
            json={**sample_contact_data, "turnstile_token": "bad-token"},
        )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_turnstile_outage_fails_open(
    client: AsyncClient, test_db: AsyncSession, sample_contact_data: dict
):
    """If Cloudflare is unreachable, real submissions still go through."""
    import httpx as httpx_mod

    with (
        patch.object(contact_endpoint.settings, "TURNSTILE_SECRET_KEY", "test-secret"),
        patch("app.services.turnstile.httpx.AsyncClient") as mock_client_cls,
    ):
        mock_client = mock_client_cls.return_value.__aenter__.return_value
        mock_client.post = AsyncMock(side_effect=httpx_mod.ConnectError("cloudflare down"))

        response = await client.post(
            "/api/v1/contact/",
            json={**sample_contact_data, "turnstile_token": "some-token"},
        )

    assert response.status_code == 201
