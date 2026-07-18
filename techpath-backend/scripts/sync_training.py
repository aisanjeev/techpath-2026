#!/usr/bin/env python
"""Sync batches and students from the external roster API into the local mirror.

Run from cron or a systemd timer:

    poetry run python scripts/sync_training.py            # batches + students
    poetry run python scripts/sync_training.py --resource batches

Deliberately a script rather than a background task inside the app: production runs
uvicorn with multiple workers, so an in-process loop would run once per worker and
double-sync. A timer gives one scheduler, visible logs, and a non-zero exit code when
something breaks.
"""
import argparse
import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.config import settings  # noqa: E402
from app.db.session import AsyncSessionLocal  # noqa: E402
from app.services.roster_sync_service import RosterSyncService  # noqa: E402
from app.services.secrets_loader import load_secrets_from_keyvault  # noqa: E402

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger("sync_training")


async def main(resource: str) -> int:
    if settings.has_keyvault_config:
        await load_secrets_from_keyvault(update_db=False)

    service = RosterSyncService(page_size=settings.ROSTER_SYNC_PAGE_SIZE)

    async with AsyncSessionLocal() as db:
        try:
            if resource == "batches":
                results = {"batches": (await service.sync_batches(db)).as_dict()}
            elif resource == "students":
                results = {"students": (await service.sync_students(db)).as_dict()}
            else:
                results = await service.sync_all(db)
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    failed = False
    for name, result in results.items():
        if result.get("error"):
            logger.error("%s: FAILED — %s", name, result["error"])
            failed = True
        elif result.get("skipped_locked"):
            logger.warning("%s: skipped, another sync is running", name)
        else:
            logger.info(
                "%s: %s processed (%s created, %s updated)",
                name,
                result["processed"],
                result["created"],
                result["updated"],
            )

    return 1 if failed else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync the external training roster")
    parser.add_argument(
        "--resource",
        choices=["batches", "students", "all"],
        default="all",
        help="What to sync (default: all)",
    )
    args = parser.parse_args()
    sys.exit(asyncio.run(main(args.resource)))
