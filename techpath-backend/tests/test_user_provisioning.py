"""Tests for Firebase-backed user provisioning and role enforcement."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies import require_roles
from app.core.constants import UserRole
from app.core.exceptions import ForbiddenError
from app.crud.user import user_crud
from app.models.user import User


class TestFirebaseProvisioning:
    """An unrecognised Firebase account must never gain privileges by signing in."""

    async def test_unknown_account_is_provisioned_inert(self, test_db: AsyncSession) -> None:
        user = await user_crud.get_or_create_from_firebase(
            test_db, "uid-unknown", "stranger@example.com", "Stranger"
        )

        assert user.role == UserRole.USER.value
        assert user.is_active is False

    async def test_unknown_account_never_becomes_admin(self, test_db: AsyncSession) -> None:
        """Regression: this path used to hardcode role="admin"."""
        for i in range(3):
            await user_crud.get_or_create_from_firebase(
                test_db, f"uid-{i}", f"user{i}@example.com", ""
            )

        admins = [
            u for u in (await user_crud.get_multi(test_db, limit=100))
            if u.role == UserRole.ADMIN.value
        ]
        assert admins == []

    async def test_display_name_falls_back_to_email_local_part(
        self, test_db: AsyncSession
    ) -> None:
        user = await user_crud.get_or_create_from_firebase(
            test_db, "uid-noname", "no.name@example.com", ""
        )
        assert user.name == "no.name"

    async def test_existing_uid_is_returned_untouched(self, test_db: AsyncSession) -> None:
        existing = User(
            email="admin@example.com",
            name="Admin",
            firebase_uid="uid-admin",
            password_hash=None,
            role=UserRole.ADMIN.value,
            is_active=True,
        )
        test_db.add(existing)
        await test_db.flush()

        user = await user_crud.get_or_create_from_firebase(
            test_db, "uid-admin", "admin@example.com", "Admin"
        )

        assert user.id == existing.id
        assert user.role == UserRole.ADMIN.value
        assert user.is_active is True


class TestEmailMigrationPath:
    """An admin-provisioned row is claimed by email on first sign-in, role intact."""

    @pytest.mark.parametrize(
        "role", [UserRole.ADMIN.value, UserRole.TRAINER.value, UserRole.USER.value]
    )
    async def test_preexisting_row_keeps_its_role_and_gains_uid(
        self, test_db: AsyncSession, role: str
    ) -> None:
        preexisting = User(
            email=f"{role}@example.com",
            name=role.title(),
            firebase_uid=None,
            password_hash=None,
            role=role,
            is_active=True,
        )
        test_db.add(preexisting)
        await test_db.flush()

        user = await user_crud.get_or_create_from_firebase(
            test_db, f"uid-{role}", f"{role}@example.com", role.title()
        )

        assert user.id == preexisting.id
        assert user.firebase_uid == f"uid-{role}"
        assert user.role == role, "migration must not alter an operator-set role"
        assert user.is_active is True, "existing users must not be locked out"


class TestRequireRoles:
    async def _call(self, dependency, user: User) -> User:
        return await dependency(current_user=user)

    def _user(self, role: str) -> User:
        return User(email=f"{role}@example.com", name=role, role=role, is_active=True)

    async def test_admin_dependency_admits_only_admin(self) -> None:
        dep = require_roles(UserRole.ADMIN)

        assert await self._call(dep, self._user(UserRole.ADMIN.value)) is not None
        for role in (UserRole.TRAINER.value, UserRole.USER.value):
            with pytest.raises(ForbiddenError):
                await self._call(dep, self._user(role))

    async def test_trainer_dependency_admits_trainer_and_admin(self) -> None:
        dep = require_roles(UserRole.TRAINER, UserRole.ADMIN)

        assert await self._call(dep, self._user(UserRole.TRAINER.value)) is not None
        assert await self._call(dep, self._user(UserRole.ADMIN.value)) is not None
        with pytest.raises(ForbiddenError):
            await self._call(dep, self._user(UserRole.USER.value))

    async def test_unknown_role_is_rejected(self) -> None:
        dep = require_roles(UserRole.ADMIN)
        with pytest.raises(ForbiddenError):
            await self._call(dep, self._user("superuser"))
