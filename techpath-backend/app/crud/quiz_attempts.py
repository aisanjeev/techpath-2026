"""CRUD for graded quiz attempts.

Attempts are append-only — nothing here updates a stored score. The read helpers are
shaped around the two questions the rest of the feature asks: "which quizzes has this
student passed in this session?" (progress gating, one query for the whole session) and
"how did the group do on this quiz?" (the trainer's report).
"""

from typing import Any, Dict, List, Sequence, Set

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.training_roster import SessionQuizAttempt


class CRUDSessionQuizAttempt(CRUDBase[SessionQuizAttempt, Any, Any]):
    async def next_attempt_number(self, db: AsyncSession, student_id: int, asset_id: int) -> int:
        """The number to assign the attempt about to be written.

        Racy by nature — two concurrent submits can both read the same max. That's
        intentional and handled by the unique constraint on
        ``(student_id, asset_id, attempt_number)``: the loser gets an IntegrityError,
        which is exactly the double-submit case the endpoint swallows.
        """
        result = await db.execute(
            select(func.max(SessionQuizAttempt.attempt_number)).where(
                SessionQuizAttempt.student_id == student_id,
                SessionQuizAttempt.asset_id == asset_id,
            )
        )
        return (result.scalar() or 0) + 1

    async def list_for_student_asset(
        self, db: AsyncSession, student_id: int, asset_id: int
    ) -> List[SessionQuizAttempt]:
        result = await db.execute(
            select(SessionQuizAttempt)
            .where(
                SessionQuizAttempt.student_id == student_id,
                SessionQuizAttempt.asset_id == asset_id,
            )
            .order_by(SessionQuizAttempt.attempt_number)
        )
        return list(result.scalars().all())

    async def passed_asset_ids(
        self, db: AsyncSession, student_id: int, session_id: int
    ) -> Set[int]:
        """Every asset this student has a passing attempt on, for one session.

        One query for the whole session — the progress endpoint renders a page per
        asset and must not fan out into a query per asset to do it.
        """
        result = await db.execute(
            select(SessionQuizAttempt.asset_id)
            .where(
                SessionQuizAttempt.student_id == student_id,
                SessionQuizAttempt.session_id == session_id,
                SessionQuizAttempt.passed.is_(True),
            )
            .distinct()
        )
        return set(result.scalars().all())

    async def summary_for_student(
        self, db: AsyncSession, student_id: int, session_id: int
    ) -> Dict[int, Dict[str, Any]]:
        """Per-asset attempt summary for one student: best score, attempt count, pass.

        Keyed by ``asset_id``. Used to show a student what they've already done on each
        quiz without replaying every attempt.
        """
        result = await db.execute(
            select(
                SessionQuizAttempt.asset_id,
                func.max(SessionQuizAttempt.score).label("best_score"),
                func.count(SessionQuizAttempt.id).label("attempt_count"),
                func.max(SessionQuizAttempt.total_questions).label("total_questions"),
                func.max(SessionQuizAttempt.passed).label("passed"),
            )
            .where(
                SessionQuizAttempt.student_id == student_id,
                SessionQuizAttempt.session_id == session_id,
            )
            .group_by(SessionQuizAttempt.asset_id)
        )
        return {
            row.asset_id: {
                "best_score": row.best_score,
                "attempt_count": row.attempt_count,
                "total_questions": row.total_questions,
                "passed": bool(row.passed),
            }
            for row in result.all()
        }

    async def list_for_session_assets(
        self, db: AsyncSession, session_id: int, asset_ids: Sequence[int]
    ) -> List[SessionQuizAttempt]:
        """Every attempt on the given assets in one session, for the trainer's report.

        Returned raw rather than pre-aggregated because the report needs both a
        per-student best and a per-question success rate computed from each student's
        best attempt — two different reductions over the same rows, so aggregating in
        SQL would mean two queries.
        """
        if not asset_ids:
            return []
        result = await db.execute(
            select(SessionQuizAttempt)
            .where(
                SessionQuizAttempt.session_id == session_id,
                SessionQuizAttempt.asset_id.in_(list(asset_ids)),
            )
            .order_by(SessionQuizAttempt.student_id, SessionQuizAttempt.attempt_number)
        )
        return list(result.scalars().all())


session_quiz_attempt_crud = CRUDSessionQuizAttempt(SessionQuizAttempt)
