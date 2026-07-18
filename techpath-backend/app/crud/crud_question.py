from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.training_roster import TrainingSessionQuestion
from app.schemas.training_roster import TrainingSessionQuestionCreate


class CRUDTrainingSessionQuestion(CRUDBase[TrainingSessionQuestion, TrainingSessionQuestionCreate, TrainingSessionQuestionCreate]):
    async def get_by_session(
        self, db: AsyncSession, *, session_id: int, skip: int = 0, limit: int = 100
    ) -> List[TrainingSessionQuestion]:
        stmt = (
            select(TrainingSessionQuestion)
            .where(TrainingSessionQuestion.session_id == session_id)
            .order_by(TrainingSessionQuestion.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def upvote(self, db: AsyncSession, *, db_obj: TrainingSessionQuestion) -> TrainingSessionQuestion:
        db_obj.upvotes += 1
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
        
    async def mark_answered(self, db: AsyncSession, *, db_obj: TrainingSessionQuestion) -> TrainingSessionQuestion:
        db_obj.is_answered = True
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


question = CRUDTrainingSessionQuestion(TrainingSessionQuestion)
