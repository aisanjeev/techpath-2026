"""Attendance boundary.

Nothing records attendance yet — the live classroom does not exist. This interface
exists now so that when it does, and when the external system eventually wants the
numbers pushed back to it, both land behind one seam instead of being scattered through
endpoint handlers.

TechPath is the source of truth for attendance today. Write-back to the external roster
API is a later addition: implement ``ExternalWriteBackAttendanceService`` and swap the
factory, and no caller changes.
"""
import logging
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class AttendanceService(ABC):
    """Records attendance for a live session."""

    @abstractmethod
    async def record_attendance(
        self,
        *,
        session_id: int,
        student_external_id: str,
        status: str,
        at: Optional[datetime] = None,
        minutes_present: Optional[int] = None,
    ) -> None:
        """Note that a student was (or wasn't) present."""

    @abstractmethod
    async def sync_pending(self) -> dict:
        """Push anything not yet delivered to an external system.

        A no-op while TechPath is the only consumer.
        """


class LocalAttendanceService(AttendanceService):
    """Phase 1 placeholder.

    Deliberately not backed by a table: the shape of an attendance record depends on
    what the live session actually captures (join events, heartbeats, engagement), and
    guessing that now would mean migrating it later.
    """

    async def record_attendance(
        self,
        *,
        session_id: int,
        student_external_id: str,
        status: str,
        at: Optional[datetime] = None,
        minutes_present: Optional[int] = None,
    ) -> None:
        logger.info(
            "attendance (not yet persisted): session=%s student=%s status=%s",
            session_id,
            student_external_id,
            status,
        )

    async def sync_pending(self) -> dict:
        return {"pushed": 0, "pending": 0, "note": "external write-back not enabled"}


_service: Optional[AttendanceService] = None


def get_attendance_service() -> AttendanceService:
    global _service
    if _service is None:
        _service = LocalAttendanceService()
    return _service
