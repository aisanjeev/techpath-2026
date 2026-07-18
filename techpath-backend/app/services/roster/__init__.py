"""External roster integration (batches, students, trainers)."""
from app.services.roster.base import RosterProvider
from app.services.roster.factory import get_roster_provider, reset_roster_provider
from app.services.roster.mock_provider import MockRosterProvider

__all__ = [
    "RosterProvider",
    "MockRosterProvider",
    "get_roster_provider",
    "reset_roster_provider",
]
