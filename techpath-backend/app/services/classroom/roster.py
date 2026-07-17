"""Publishes the roster snapshot the trainer panel renders directly from.

One event type covers join, leave, and confusion changes rather than three, so the
trainer's WS handler has one case to implement instead of stitching partial updates
together. The payload is small — a training batch, not a lecture hall — so resending
the full list on every change is cheap and removes a whole class of "my local state
drifted from the server" bugs.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.classroom import session_participant_crud
from app.services.classroom import bus


async def publish_roster_snapshot(db: AsyncSession, session_id: int) -> None:
    participants = await session_participant_crud.list_for_session(db, session_id)
    summary = await session_participant_crud.confusion_summary(db, session_id)
    hands_raised = await session_participant_crud.hands_raised_queue(db, session_id)
    await bus.publish(
        db,
        session_id,
        "roster_changed",
        {
            "participants": [
                {
                    "id": p.id,
                    "display_name": p.display_name,
                    "is_guest": p.is_guest,
                    "is_online": p.is_online,
                    "is_confused": p.is_confused,
                    "hand_raised": p.hand_raised,
                    "hand_raised_at": (
                        p.hand_raised_at.isoformat() if p.hand_raised_at else None
                    ),
                }
                for p in participants
            ],
            "confusion": summary,
            # Additive: participants currently with a hand up, first-raised first, so
            # the trainer panel can render a call-on-me queue without a second request.
            "hands_raised_queue": [
                {
                    "participant_id": p.id,
                    "display_name": p.display_name,
                    "hand_raised_at": (
                        p.hand_raised_at.isoformat() if p.hand_raised_at else None
                    ),
                }
                for p in hands_raised
            ],
        },
    )
