"""Roster provider selection.

Mirrors ``get_storage_service()``: Key Vault wins over environment, resolution is lazy
so secrets are loaded first, and the choice is a config value rather than a code change.
"""
import logging
from typing import Optional

from app.core.config import settings
from app.services.roster.base import RosterProvider
from app.services.roster.mock_provider import MockRosterProvider
from app.services.secrets_loader import runtime_secrets

logger = logging.getLogger(__name__)

_provider: Optional[RosterProvider] = None


def _resolve(key: str, fallback: Optional[str] = None) -> Optional[str]:
    return runtime_secrets.get(key) or getattr(settings, key, None) or fallback


def get_roster_provider() -> RosterProvider:
    """Return the configured provider, building it on first use."""
    global _provider
    if _provider is not None:
        return _provider

    provider_name = (_resolve("ROSTER_PROVIDER", "mock") or "mock").lower()

    if provider_name == "http":
        base_url = _resolve("ROSTER_API_BASE_URL")
        api_key = _resolve("ROSTER_API_KEY")
        if not base_url or not api_key:
            # Falling back to the mock would quietly serve fixture data as if it were
            # real students. Better to fail loudly than to teach the wrong roster.
            raise RuntimeError(
                "ROSTER_PROVIDER=http requires ROSTER_API_BASE_URL and ROSTER_API_KEY"
            )
        from app.services.roster.http_provider import HttpRosterProvider

        logger.info("Roster provider: http (%s)", base_url)
        _provider = HttpRosterProvider(base_url, api_key)
    else:
        logger.info("Roster provider: mock (fixtures)")
        _provider = MockRosterProvider()

    return _provider


def reset_roster_provider() -> None:
    """Drop the cached provider. For tests and config reloads."""
    global _provider
    _provider = None
