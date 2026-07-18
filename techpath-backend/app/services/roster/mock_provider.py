"""Fixture-backed roster provider used until the external API exists.

This is the contract made executable. It is deliberately faithful rather than
convenient: it paginates for real, honours ``updated_since``, and reports ``has_more``
honestly. A mock that always returns one page would leave the sync's paging loop
untested until the day the real API arrives — which is exactly the day you don't want
to be finding out about it.
"""
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, List, Optional, TypeVar

from app.schemas.roster_external import (
    ExternalBatch,
    ExternalStudent,
    ExternalTrainer,
    PageMeta,
    RosterPage,
)
from app.services.roster.base import RosterProvider

logger = logging.getLogger(__name__)

FIXTURES_DIR = Path(__file__).parent / "fixtures"

T = TypeVar("T")


def _as_aware(value: Optional[datetime]) -> Optional[datetime]:
    """Compare like with like — a naive fixture timestamp against an aware cursor is a
    TypeError waiting to happen."""
    if value is None:
        return None
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


class MockRosterProvider(RosterProvider):
    """Serves batches/students/trainers from JSON fixtures."""

    def __init__(self, fixtures_dir: Optional[Path] = None, page_size_cap: int = 100) -> None:
        self._dir = fixtures_dir or FIXTURES_DIR
        self._page_size_cap = page_size_cap

    def _load(self, name: str) -> List[dict]:
        path = self._dir / f"{name}.json"
        if not path.exists():
            logger.warning("Roster fixture %s not found; returning empty list", path)
            return []
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)

    def _paginate(
        self, rows: List[Any], page: int, page_size: int
    ) -> tuple[List[Any], PageMeta]:
        page = max(page, 1)
        page_size = max(1, min(page_size, self._page_size_cap))
        start = (page - 1) * page_size
        window = rows[start : start + page_size]
        return window, PageMeta(
            page=page,
            page_size=page_size,
            total=len(rows),
            has_more=start + page_size < len(rows),
        )

    def _filter_updated(self, rows: List[dict], updated_since: Optional[datetime]) -> List[dict]:
        if updated_since is None:
            return rows
        cutoff = _as_aware(updated_since)
        kept = []
        for row in rows:
            raw = row.get("updated_at")
            if not raw:
                kept.append(row)  # no timestamp -> always sync it, never silently drop
                continue
            ts = _as_aware(datetime.fromisoformat(str(raw).replace("Z", "+00:00")))
            if ts >= cutoff:
                kept.append(row)
        return kept

    async def list_batches(
        self,
        *,
        updated_since: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 100,
        status: Optional[str] = None,
        trainer_id: Optional[str] = None,
    ) -> RosterPage[ExternalBatch]:
        rows = self._filter_updated(self._load("batches"), updated_since)
        if status:
            rows = [r for r in rows if r.get("status") == status]
        if trainer_id:
            rows = [r for r in rows if r.get("trainer_id") == trainer_id]
        rows.sort(key=lambda r: str(r["id"]))  # stable ordering, as the contract requires

        window, meta = self._paginate(rows, page, page_size)
        return RosterPage[ExternalBatch](
            data=[ExternalBatch(**r) for r in window], meta=meta
        )

    async def get_batch(self, batch_id: str) -> Optional[ExternalBatch]:
        for row in self._load("batches"):
            if str(row["id"]) == batch_id:
                return ExternalBatch(**row)
        return None

    async def list_batch_students(
        self, batch_id: str, *, page: int = 1, page_size: int = 100
    ) -> RosterPage[ExternalStudent]:
        rows = [r for r in self._load("students") if batch_id in r.get("batch_ids", [])]
        rows.sort(key=lambda r: str(r["id"]))
        window, meta = self._paginate(rows, page, page_size)
        return RosterPage[ExternalStudent](
            data=[ExternalStudent(**r) for r in window], meta=meta
        )

    async def list_students(
        self,
        *,
        updated_since: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 100,
    ) -> RosterPage[ExternalStudent]:
        rows = self._filter_updated(self._load("students"), updated_since)
        rows.sort(key=lambda r: str(r["id"]))
        window, meta = self._paginate(rows, page, page_size)
        return RosterPage[ExternalStudent](
            data=[ExternalStudent(**r) for r in window], meta=meta
        )

    async def get_student(self, student_id: str) -> Optional[ExternalStudent]:
        for row in self._load("students"):
            if str(row["id"]) == student_id:
                return ExternalStudent(**row)
        return None

    async def list_trainers(
        self, *, updated_since: Optional[datetime] = None, page: int = 1, page_size: int = 100
    ) -> RosterPage[ExternalTrainer]:
        rows = self._filter_updated(self._load("trainers"), updated_since)
        rows.sort(key=lambda r: str(r["id"]))
        window, meta = self._paginate(rows, page, page_size)
        return RosterPage[ExternalTrainer](
            data=[ExternalTrainer(**r) for r in window], meta=meta
        )

    async def health(self) -> bool:
        return (self._dir / "batches.json").exists()
