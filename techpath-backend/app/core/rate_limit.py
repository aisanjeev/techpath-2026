"""In-memory per-IP rate limiting for public (unauthenticated) endpoints."""

import time

from fastapi import Request

from app.core.exceptions import RateLimitError


def get_client_ip(request: Request) -> str | None:
    """Best-effort real client IP.

    Behind the VPS nginx proxy, `request.client.host` is only the real client
    when uvicorn runs with --proxy-headers; as a fallback we honor the first
    X-Forwarded-For entry. The header is only spoofable when the app is reached
    directly — and then `request.client.host` is already the real IP, so a
    spoofed header just lets an attacker rate-limit themselves.
    """
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip() or None
    return request.client.host if request.client else None


class SlidingWindowRateLimiter:
    """Per-key sliding-window counter held in process memory.

    Same trade-off as the classroom join-code limiter (classroom.py): survives
    neither restarts nor multiple workers, which is fine for abuse damping —
    with N uvicorn workers the effective limit is at most N * max_hits.
    """

    # Prune stale keys once the dict grows past this, so a slow scan across
    # many IPs can't grow memory unboundedly.
    _PRUNE_THRESHOLD = 10_000

    def __init__(self, *, max_hits: int, window_seconds: int = 3600) -> None:
        self.max_hits = max_hits
        self.window_seconds = window_seconds
        self._hits: dict[str, list[float]] = {}

    def check(
        self,
        key: str | None,
        message: str = "Too many requests — please try again later",
    ) -> None:
        """Record a hit for `key`, raising RateLimitError when over the limit."""
        if key is None:
            return
        now = time.monotonic()
        window_start = now - self.window_seconds

        if len(self._hits) > self._PRUNE_THRESHOLD:
            self._hits = {
                k: recent
                for k, v in self._hits.items()
                if (recent := [t for t in v if t > window_start])
            }

        hits = [t for t in self._hits.get(key, []) if t > window_start]
        if len(hits) >= self.max_hits:
            self._hits[key] = hits
            raise RateLimitError(message)
        hits.append(now)
        self._hits[key] = hits
