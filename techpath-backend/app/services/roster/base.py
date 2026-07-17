"""The one interface between TechPath and whoever owns the student roster.

Everything above this layer speaks ``RosterProvider``. Swapping the mock for the real
HTTP API is a config change, and if the delivered API differs from the contract, only
``http_provider.py`` changes.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from app.schemas.roster_external import (
    ExternalBatch,
    ExternalStudent,
    ExternalTrainer,
    RosterPage,
)


class RosterProvider(ABC):
    """Read-only access to externally owned batches, students and trainers."""

    @abstractmethod
    async def list_batches(
        self,
        *,
        updated_since: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 100,
        status: Optional[str] = None,
        trainer_id: Optional[str] = None,
    ) -> RosterPage[ExternalBatch]:
        """One page of batches, optionally only those changed since a timestamp."""

    @abstractmethod
    async def get_batch(self, batch_id: str) -> Optional[ExternalBatch]:
        ...

    @abstractmethod
    async def list_batch_students(
        self, batch_id: str, *, page: int = 1, page_size: int = 100
    ) -> RosterPage[ExternalStudent]:
        ...

    @abstractmethod
    async def list_students(
        self,
        *,
        updated_since: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 100,
    ) -> RosterPage[ExternalStudent]:
        ...

    @abstractmethod
    async def get_student(self, student_id: str) -> Optional[ExternalStudent]:
        ...

    @abstractmethod
    async def list_trainers(
        self, *, updated_since: Optional[datetime] = None, page: int = 1, page_size: int = 100
    ) -> RosterPage[ExternalTrainer]:
        ...

    @abstractmethod
    async def health(self) -> bool:
        """Whether the provider is reachable. Never raises."""

    async def aclose(self) -> None:
        """Release any held resources. No-op unless overridden."""
        return None
