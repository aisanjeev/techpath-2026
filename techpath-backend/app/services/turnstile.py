"""Cloudflare Turnstile server-side token verification."""

import logging

import httpx

from app.core.config import settings


logger = logging.getLogger(__name__)

TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


async def verify_turnstile_token(token: str | None, remote_ip: str | None = None) -> bool:
    """Verify a Turnstile token with Cloudflare's siteverify endpoint.

    Returns True when verification is disabled (TURNSTILE_SECRET_KEY unset) so
    local dev and tests work without keys. Fails closed on a missing or invalid
    token, but open on a Cloudflare outage — a brief spam window is cheaper
    than dropping real leads.
    """
    if not settings.is_turnstile_enabled:
        return True
    if not token:
        return False

    payload = {"secret": settings.TURNSTILE_SECRET_KEY, "response": token}
    if remote_ip:
        payload["remoteip"] = remote_ip

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(TURNSTILE_VERIFY_URL, data=payload)
            response.raise_for_status()
            outcome = response.json()
    except (httpx.HTTPError, ValueError) as exc:
        logger.warning("Turnstile verification unavailable, allowing request: %s", exc)
        return True

    if not outcome.get("success"):
        logger.info("Turnstile rejected token: %s", outcome.get("error-codes"))
    return bool(outcome.get("success"))
