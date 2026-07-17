"""Base async HTTP client for outbound calls to third-party services.

``httpx`` was already a declared dependency but nothing in ``app/`` used it, so this
establishes the convention rather than bolting retries onto one call site: a pooled
client, sane timeouts, bounded retries on the failures that are actually transient, and
logging that never prints a credential.
"""
import asyncio
import logging
import random
from typing import Any, Optional

import httpx

from app.core.exceptions import ExternalServiceError

logger = logging.getLogger(__name__)

# Retrying a 4xx just means failing four times as slowly — the request is wrong and it
# will stay wrong. Only transient server-side and network faults are worth another go.
RETRY_STATUS_CODES = frozenset({429, 500, 502, 503, 504})
RETRY_EXCEPTIONS = (httpx.ConnectError, httpx.ReadTimeout, httpx.WriteTimeout, httpx.PoolTimeout)

# Header names whose values must never reach the logs.
_REDACTED_HEADERS = frozenset({"x-api-key", "authorization", "cookie", "proxy-authorization"})


def redact_headers(headers: dict[str, str]) -> dict[str, str]:
    """Mask credential headers so a debug log can't leak an API key."""
    return {
        k: ("***" if k.lower() in _REDACTED_HEADERS else v) for k, v in headers.items()
    }


class BaseHttpClient:
    """A thin, retrying wrapper around a pooled ``httpx.AsyncClient``.

    The client is created once and reused: building one per request throws away
    connection pooling and is the usual reason a healthy integration starts exhausting
    sockets under load.
    """

    service_name = "External service"

    def __init__(
        self,
        base_url: str,
        *,
        headers: Optional[dict[str, str]] = None,
        max_retries: int = 3,
        connect_timeout: float = 5.0,
        read_timeout: float = 30.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self._headers = headers or {}
        self._max_retries = max_retries
        self._timeout = httpx.Timeout(
            connect=connect_timeout, read=read_timeout, write=read_timeout, pool=5.0
        )
        self._client: Optional[httpx.AsyncClient] = None
        self._lock = asyncio.Lock()

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            async with self._lock:
                if self._client is None or self._client.is_closed:
                    self._client = httpx.AsyncClient(
                        base_url=self.base_url,
                        headers=self._headers,
                        timeout=self._timeout,
                        limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
                        follow_redirects=True,
                    )
        return self._client

    async def aclose(self) -> None:
        """Release the pool. Wired into application shutdown."""
        if self._client is not None and not self._client.is_closed:
            await self._client.aclose()
        self._client = None

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json_body: Optional[dict[str, Any]] = None,
    ) -> Any:
        """Issue a request, retrying transient failures, and return the decoded JSON."""
        client = await self._get_client()
        last_error: Optional[Exception] = None

        for attempt in range(self._max_retries):
            try:
                response = await client.request(method, path, params=params, json=json_body)

                if response.status_code in RETRY_STATUS_CODES:
                    last_error = ExternalServiceError(
                        self.service_name,
                        f"{method} {path} returned {response.status_code}",
                    )
                    if attempt < self._max_retries - 1:
                        await self._backoff(attempt, response)
                        continue
                    raise last_error

                if response.status_code >= 400:
                    # A client error is a bug in our request or their data. Surface it
                    # immediately rather than hammering them.
                    logger.warning(
                        "%s %s%s -> %s", method, self.base_url, path, response.status_code
                    )
                    raise ExternalServiceError(
                        self.service_name,
                        f"{method} {path} failed with {response.status_code}: "
                        f"{response.text[:200]}",
                    )

                logger.debug(
                    "%s %s%s -> %s in %.0fms",
                    method,
                    self.base_url,
                    path,
                    response.status_code,
                    response.elapsed.total_seconds() * 1000,
                )
                return response.json()

            except RETRY_EXCEPTIONS as exc:
                last_error = exc
                if attempt < self._max_retries - 1:
                    await self._backoff(attempt)
                    continue
                raise ExternalServiceError(
                    self.service_name, f"{method} {path} failed: {exc}"
                ) from exc

        raise ExternalServiceError(self.service_name, str(last_error))

    async def _backoff(self, attempt: int, response: Optional[httpx.Response] = None) -> None:
        """Exponential backoff with jitter, honouring Retry-After when offered.

        Jitter matters: without it, every worker that failed at the same moment retries
        at the same moment.
        """
        if response is not None:
            retry_after = response.headers.get("retry-after")
            if retry_after:
                try:
                    await asyncio.sleep(min(float(retry_after), 30.0))
                    return
                except ValueError:
                    pass

        delay = min(2**attempt, 8) + random.uniform(0, 0.5)
        await asyncio.sleep(delay)

    async def get(self, path: str, *, params: Optional[dict[str, Any]] = None) -> Any:
        return await self.request("GET", path, params=params)

    async def post(self, path: str, *, json_body: Optional[dict[str, Any]] = None) -> Any:
        return await self.request("POST", path, json_body=json_body)
