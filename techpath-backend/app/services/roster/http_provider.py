"""Roster provider backed by the customer-built external API.

If the delivered API deviates from ``docs/ROSTER_API.md``, this file is the only thing
that should need to change — that is the entire reason the provider interface exists.
"""
import logging
from datetime import datetime
from typing import Any, Optional

from app.schemas.roster_external import (
    ExternalBatch,
    ExternalStudent,
    ExternalTrainer,
    PageMeta,
    RosterPage,
)
from app.services.http_client import BaseHttpClient
from app.services.roster.base import RosterProvider

logger = logging.getLogger(__name__)


class HttpRosterProvider(RosterProvider):
    """Talks to the external roster API over HTTPS with an API key."""

    def __init__(self, base_url: str, api_key: str) -> None:
        self._client = BaseHttpClient(base_url, headers={"X-API-Key": api_key})
        self._client.service_name = "Roster API"

    @staticmethod
    def _params(
        updated_since: Optional[datetime], page: int, page_size: int, **extra: Any
    ) -> dict:
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if updated_since is not None:
            params["updated_since"] = updated_since.isoformat()
        params.update({k: v for k, v in extra.items() if v is not None})
        return params

    @staticmethod
    def _envelope(payload: Any) -> tuple[list, PageMeta]:
        """Unwrap ``{data: [...], meta: {...}}``.

        Tolerates a bare array, because an API delivered without the envelope is a
        likely first-integration reality and a hard crash there is unhelpful.
        """
        if isinstance(payload, list):
            return payload, PageMeta(page=1, page_size=len(payload), total=len(payload))
        data = payload.get("data", [])
        meta = payload.get("meta") or {}
        return data, PageMeta(**meta) if meta else PageMeta(
            page=1, page_size=len(data), total=len(data)
        )

    # All paths are absolute from the host root so they work regardless of what the
    # caller passes as base_url (host+port only, no path prefix needed there).
    _PREFIX = "/api/v1/roster"

    async def list_batches(
        self,
        *,
        updated_since: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 100,
        status: Optional[str] = None,
        trainer_id: Optional[str] = None,
    ) -> RosterPage[ExternalBatch]:
        payload = await self._client.get(
            f"{self._PREFIX}/batches",
            params=self._params(
                updated_since, page, page_size, status=status, trainer_id=trainer_id
            ),
        )
        data, meta = self._envelope(payload)
        return RosterPage[ExternalBatch](data=[ExternalBatch(**r) for r in data], meta=meta)

    async def get_batch(self, batch_id: str) -> Optional[ExternalBatch]:
        payload = await self._client.get(f"{self._PREFIX}/batches/{batch_id}")
        row = payload.get("data", payload) if isinstance(payload, dict) else payload
        return ExternalBatch(**row) if row else None

    async def list_batch_students(
        self, batch_id: str, *, page: int = 1, page_size: int = 100
    ) -> RosterPage[ExternalStudent]:
        payload = await self._client.get(
            f"{self._PREFIX}/batches/{batch_id}/students",
            params={"page": page, "page_size": page_size},
        )
        data, meta = self._envelope(payload)
        return RosterPage[ExternalStudent](data=[ExternalStudent(**r) for r in data], meta=meta)

    async def list_students(
        self,
        *,
        updated_since: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 100,
    ) -> RosterPage[ExternalStudent]:
        payload = await self._client.get(
            f"{self._PREFIX}/students", params=self._params(updated_since, page, page_size)
        )
        data, meta = self._envelope(payload)
        return RosterPage[ExternalStudent](data=[ExternalStudent(**r) for r in data], meta=meta)

    async def get_student(self, student_id: str) -> Optional[ExternalStudent]:
        payload = await self._client.get(f"{self._PREFIX}/students/{student_id}")
        row = payload.get("data", payload) if isinstance(payload, dict) else payload
        return ExternalStudent(**row) if row else None

    async def list_trainers(
        self, *, updated_since: Optional[datetime] = None, page: int = 1, page_size: int = 100
    ) -> RosterPage[ExternalTrainer]:
        payload = await self._client.get(
            f"{self._PREFIX}/trainers", params=self._params(updated_since, page, page_size)
        )
        data, meta = self._envelope(payload)
        return RosterPage[ExternalTrainer](data=[ExternalTrainer(**r) for r in data], meta=meta)

    async def health(self) -> bool:
        try:
            await self._client.get(f"{self._PREFIX}/health")
            return True
        except Exception as exc:
            logger.warning("Roster API health check failed: %s", exc)
            return False

    async def aclose(self) -> None:
        await self._client.aclose()
