"""Live classroom audio/video: stream-path minting and MediaMTX URL builders.

No media ever flows through this backend — WHIP (publish) and WHEP/HLS (playback) are
direct browser-to-MediaMTX connections (see CLASSROOM-WEBAPP-GUIDE.md). MediaMTX itself
runs with no server-side auth (``authMethod: internal``), so this module is the entire
access-control story for live media: a stream path is a high-entropy secret that is only
ever handed to a caller who has already passed this app's own authorization (trainer
ownership for WHIP, a valid classroom participant token for WHEP/HLS — see
``app/api/v1/endpoints/trainer.py`` / ``classroom.py``). Unlike ``join_code`` this path is
never displayed or spoken aloud, so it can and does use much higher entropy than six
digits.
"""
import logging
import secrets

from app.core.config import settings
from app.services.http_client import BaseHttpClient

logger = logging.getLogger(__name__)


def mint_live_stream_path(session_id: int) -> str:
    """A per-session-goes-live secret, unguessable and never rendered to a user."""
    return f"class-{session_id}-{secrets.token_urlsafe(16)}"


def _base_url() -> str:
    return settings.LIVE_MEDIA_BASE_URL.rstrip("/")


def whip_url(stream_path: str) -> str:
    """The trainer-only publish URL."""
    return f"{_base_url()}/{stream_path}/whip"


def whep_url(stream_path: str) -> str:
    """The participant playback URL (WebRTC, ~200ms latency)."""
    return f"{_base_url()}/{stream_path}/whep"


def hls_url(stream_path: str) -> str:
    """The participant fallback playback URL for networks that block WebRTC/UDP."""
    return f"{_base_url()}/{stream_path}/index.m3u8"


def watch_url(stream_path: str) -> str:
    """The replay a student links to once transcoding finishes — deterministic from
    ``stream_path`` (see CLASSROOM-WEBAPP-GUIDE.md), not something the watch service
    needs to hand back to us."""
    return f"{settings.WATCH_SERVICE_BASE_URL.rstrip('/')}/{stream_path}"


async def trigger_transcode(stream_path: str) -> None:
    """Kick off transcoding of a just-ended session's recording.

    MediaMTX names the recording file itself from the record start time, a detail this
    backend never learns (see CLASSROOM-WEBAPP-GUIDE.md's example filename) — the watch
    service is expected to resolve "the recording for this stream path" itself rather
    than being handed an exact filename. Best-effort: a failed trigger leaves the
    recording row ``processing`` rather than raising, since ending a session must not
    fail just because the transcode kickoff did — see the caller in trainer.py.
    """
    client = BaseHttpClient(settings.WATCH_SERVICE_BASE_URL)
    client.service_name = "Watch service"
    try:
        await client.post(f"/api/transcode/{stream_path}")
    except Exception as exc:  # noqa: BLE001 — best-effort trigger, never blocks end_session
        logger.warning("Failed to trigger transcode for %s: %s", stream_path, exc)
    finally:
        await client.aclose()
