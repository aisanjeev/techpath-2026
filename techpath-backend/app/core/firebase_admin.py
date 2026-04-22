"""Firebase Admin SDK — token verification for admin panel auth."""
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

        # Prefer explicit service-account JSON file if configured
        sa_path = settings.FIREBASE_SERVICE_ACCOUNT_PATH
        if sa_path and os.path.isfile(sa_path):
            cred = credentials.Certificate(sa_path)
            logger.info("Firebase Admin SDK: using service-account key at %s", sa_path)
        else:
            # Fall back to Application Default Credentials (ADC).
            # On Google Cloud (Cloud Run, App Engine, GCE) ADC is automatic.
            # Locally: run `gcloud auth application-default login`.
            # If neither is available, verify_id_token() still works for
            # signature-only verification via Google's public-key endpoint.
            try:
                cred = credentials.ApplicationDefault()
                logger.info("Firebase Admin SDK: using Application Default Credentials")
            except Exception:
                # No ADC available — initialize without credentials.
                # verify_id_token() will still work (public-key verification only).
                cred = None
                logger.warning(
                    "Firebase Admin SDK: no service-account or ADC found — "
                    "initialising with project ID only. verify_id_token() will "
                    "use public-key verification (check_revoked is not supported)."
                )

        if cred is not None:
            firebase_admin.initialize_app(
                cred, options={"projectId": settings.FIREBASE_PROJECT_ID}
            )
        else:
            firebase_admin.initialize_app(options={"projectId": settings.FIREBASE_PROJECT_ID})

        logger.info(
            "Firebase Admin SDK initialised (project: %s)", settings.FIREBASE_PROJECT_ID
        )

    _initialized = True


def verify_firebase_token(id_token: str) -> dict[str, Any]:
    """Verify a Firebase ID token and return its decoded claims.

    Raises firebase_admin.auth.InvalidIdTokenError on invalid/expired tokens.
    """
    _ensure_initialized()
    return auth.verify_id_token(id_token)  # type: ignore[return-value]
