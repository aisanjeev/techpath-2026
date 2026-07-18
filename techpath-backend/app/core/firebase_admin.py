"""Firebase Admin SDK — token verification and user management."""
import base64
import json
import logging
import os
from typing import Any

import firebase_admin
from firebase_admin import auth, credentials

logger = logging.getLogger(__name__)

_initialized = False


def _ensure_initialized() -> None:
    global _initialized
    if _initialized:
        return

    from app.core.config import settings

    if not settings.FIREBASE_PROJECT_ID:
        raise RuntimeError("FIREBASE_PROJECT_ID is not set in environment")

    if not firebase_admin._apps:
        cred: credentials.Base | None = None

        # 1. Explicit JSON key file on disk
        sa_path = settings.FIREBASE_SERVICE_ACCOUNT_PATH
        if sa_path and os.path.isfile(sa_path):
            cred = credentials.Certificate(sa_path)
            logger.info("Firebase Admin SDK: using service-account key at %s", sa_path)

        # 2. Base64-encoded JSON from Key Vault or env var
        if cred is None:
            from app.services.secrets_loader import runtime_secrets
            sa_b64 = (
                runtime_secrets.get("FIREBASE_SERVICE_ACCOUNT_B64")
                or os.environ.get("FIREBASE_SERVICE_ACCOUNT_B64", "")
            )
            if sa_b64:
                try:
                    sa_json = json.loads(base64.b64decode(sa_b64))
                    cred = credentials.Certificate(sa_json)
                    logger.info("Firebase Admin SDK: using base64-encoded service account")
                except Exception as exc:
                    logger.warning("Failed to decode FIREBASE_SERVICE_ACCOUNT_B64: %s", exc)

        # 3. Application Default Credentials (GCP environments)
        if cred is None:
            try:
                candidate = credentials.ApplicationDefault()
                # ApplicationDefault resolves lazily, so its constructor cannot fail.
                # Force resolution here: otherwise a missing, expired or wrong-project
                # ADC passes startup and resurfaces as an "invalid or expired token"
                # 401 on the first sign-in, which points nowhere near the real cause.
                candidate.get_credential()
                cred = candidate
                logger.info("Firebase Admin SDK: using Application Default Credentials")
            except Exception as exc:
                logger.warning(
                    "Firebase Admin SDK: no usable credential (ADC: %s). Set "
                    "FIREBASE_SERVICE_ACCOUNT_PATH or FIREBASE_SERVICE_ACCOUNT_B64 — "
                    "sign-in and user management will fail until one is configured.",
                    exc,
                )

        # A None credential makes initialize_app fall back to ADC internally, so this
        # covers both branches; it is not a working "project ID only" mode.
        firebase_admin.initialize_app(
            cred, options={"projectId": settings.FIREBASE_PROJECT_ID}
        )

        logger.info(
            "Firebase Admin SDK initialised (project: %s)", settings.FIREBASE_PROJECT_ID
        )

    _initialized = True


# Tokens are minted against Google's clock and verified against ours, so any drift
# makes a fresh token look issued-in-the-future and it is rejected outright. The SDK
# tolerates nothing by default; allow a few seconds of ordinary drift.
CLOCK_SKEW_SECONDS = 10


def verify_firebase_token(id_token: str) -> dict[str, Any]:
    """Verify a Firebase ID token and return its decoded claims."""
    _ensure_initialized()
    return auth.verify_id_token(  # type: ignore[return-value]
        id_token, clock_skew_seconds=CLOCK_SKEW_SECONDS
    )


def create_firebase_user(email: str, password: str, display_name: str = "") -> str:
    """Create a Firebase Authentication user and return their UID."""
    _ensure_initialized()
    user_record = auth.create_user(
        email=email,
        password=password,
        display_name=display_name or email.split("@")[0],
    )
    logger.info("Created Firebase user: %s (uid=%s)", email, user_record.uid)
    return user_record.uid


def delete_firebase_user(uid: str) -> None:
    """Delete a Firebase Authentication user by UID."""
    _ensure_initialized()
    auth.delete_user(uid)
    logger.info("Deleted Firebase user: uid=%s", uid)
