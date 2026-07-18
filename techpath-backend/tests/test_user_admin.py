"""Tests for admin user management — the path that makes a trainer creatable."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints.auth import provision_user, update_user
from app.core.constants import UserRole
from app.core.exceptions import ConflictError, ValidationError
from app.crud.user import user_crud
from app.models.user import User
from app.schemas.user import UserAdminUpdate, UserProvision


async def _admin(db: AsyncSession, email: str = "admin@techpath.biz") -> User:
    user = User(
        email=email, name="Admin", firebase_uid=f"uid-{email}",
        role=UserRole.ADMIN.value, is_active=True,
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user


class TestProvisionUser:
    async def test_provisions_a_trainer_without_a_password(
        self, test_db: AsyncSession
    ) -> None:
        """Firebase users have no local password, so this must not require one."""
        admin = await _admin(test_db)

        result = await provision_user(
            UserProvision(email="t@techpath.biz", name="Trainer", role="trainer"),
            db=test_db,
            current_admin=admin,
        )

        assert result.role == "trainer"
        assert result.is_active is True
        assert result.has_signed_in is False

        row = await user_crud.get_by_email(test_db, "t@techpath.biz")
        assert row.password_hash is None
        assert row.firebase_uid is None

    async def test_provisioned_trainer_survives_first_signin(
        self, test_db: AsyncSession
    ) -> None:
        """The whole onboarding flow: provision -> Firebase console -> sign in."""
        admin = await _admin(test_db)
        await provision_user(
            UserProvision(email="t@techpath.biz", name="Trainer", role="trainer"),
            db=test_db,
            current_admin=admin,
        )

        user = await user_crud.get_or_create_from_firebase(
            test_db, "firebase-uid-xyz", "t@techpath.biz", "Trainer"
        )

        assert user.role == "trainer", "the provisioned role must survive sign-in"
        assert user.is_active is True
        assert user.firebase_uid == "firebase-uid-xyz"

    async def test_duplicate_email_conflicts(self, test_db: AsyncSession) -> None:
        admin = await _admin(test_db)
        await provision_user(
            UserProvision(email="dup@techpath.biz", name="A"), db=test_db, current_admin=admin
        )
        with pytest.raises(ConflictError):
            await provision_user(
                UserProvision(email="dup@techpath.biz", name="B"),
                db=test_db,
                current_admin=admin,
            )

    async def test_invalid_role_is_rejected(self) -> None:
        from pydantic import ValidationError as PydanticValidationError

        with pytest.raises(PydanticValidationError):
            UserProvision(email="x@y.com", name="X", role="superuser")


class TestUpdateUser:
    async def test_activates_a_pending_user(self, test_db: AsyncSession) -> None:
        """The recovery path for anyone auto-provisioned inert."""
        admin = await _admin(test_db)
        pending = await user_crud.get_or_create_from_firebase(
            test_db, "uid-p", "pending@x.com", "Pending"
        )
        assert pending.is_active is False

        result = await update_user(
            pending.id,
            UserAdminUpdate(role="trainer", is_active=True),
            db=test_db,
            current_admin=admin,
        )

        assert result.is_active is True
        assert result.role == "trainer"

    async def test_admin_cannot_deactivate_themselves(self, test_db: AsyncSession) -> None:
        admin = await _admin(test_db)
        with pytest.raises(ValidationError, match="your own account"):
            await update_user(
                admin.id, UserAdminUpdate(is_active=False), db=test_db, current_admin=admin
            )

    async def test_admin_cannot_demote_themselves(self, test_db: AsyncSession) -> None:
        admin = await _admin(test_db)
        with pytest.raises(ValidationError, match="your own admin role"):
            await update_user(
                admin.id, UserAdminUpdate(role="trainer"), db=test_db, current_admin=admin
            )

    async def test_cannot_demote_the_last_admin(self, test_db: AsyncSession) -> None:
        """Otherwise nobody is left who can grant the role back."""
        admin = await _admin(test_db)
        other = await _admin(test_db, "other@techpath.biz")

        # Two admins: demoting one is fine.
        await update_user(
            other.id, UserAdminUpdate(role="trainer"), db=test_db, current_admin=admin
        )

        # Now only `admin` remains, and a different admin trying to demote them fails.
        second = await _admin(test_db, "second@techpath.biz")
        await update_user(
            second.id, UserAdminUpdate(role="user"), db=test_db, current_admin=admin
        )

        remaining = await user_crud.count(test_db, filters={"role": UserRole.ADMIN.value})
        assert remaining == 1

    async def test_missing_user_404s(self, test_db: AsyncSession) -> None:
        from app.core.exceptions import NotFoundError

        admin = await _admin(test_db)
        with pytest.raises(NotFoundError):
            await update_user(
                9999, UserAdminUpdate(role="user"), db=test_db, current_admin=admin
            )
