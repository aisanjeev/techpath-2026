#!/usr/bin/env python3
"""
Seed training landing page content into app_settings (idempotent).

Inserts the key training_landing_content with default JSON so the training page
has content on first deploy. Skips insert if the key already exists unless --force.

Usage:
  cd techpath-backend
  python scripts/seed_training_page.py
  python scripts/seed_training_page.py --force   # overwrite with default

Requires: Backend deps (poetry install). Set DATABASE_URL if not using default.
"""

import argparse
import asyncio
import json
import os
import sys

# Add backend root to path so app imports work
_script_dir = os.path.dirname(os.path.abspath(__file__))
_backend_root = os.path.dirname(_script_dir)
if _backend_root not in sys.path:
    sys.path.insert(0, _backend_root)

# Optional: load .env.local
_env_path = os.path.join(_backend_root, ".env.local")
if os.path.isfile(_env_path):
    try:
        with open(_env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k and os.environ.get(k) is None:
                        os.environ[k] = v
    except Exception:
        pass


async def main() -> None:
    parser = argparse.ArgumentParser(description="Seed training page content into app_settings")
    parser.add_argument("--force", action="store_true", help="Overwrite existing value with default")
    args = parser.parse_args()

    from app.api.v1.endpoints.content import get_builtin_training_content
    from app.crud.app_setting import app_setting_crud
    from app.db.session import AsyncSessionLocal, engine
    from app.schemas.app_setting import AppSettingCreate

    key = "training_landing_content"
    default_dict = get_builtin_training_content()
    value = json.dumps(default_dict, ensure_ascii=False)

    try:
        async with AsyncSessionLocal() as db:
            existing = await app_setting_crud.get_by_key(db, key)
            if existing and not args.force:
                print(f"Key '{key}' already exists. Use --force to overwrite.")
                return
            if existing and args.force:
                await app_setting_crud.update_value(db, key, value)
                print(f"Updated '{key}' with default training page content.")
                return
            await app_setting_crud.create(
                db,
                AppSettingCreate(
                    key=key,
                    value=value,
                    display_name="Training Landing Page Content",
                    description="JSON for /training page: hero, pain points, USPs, FAQs, stories, offer banner, CTA. Edit via API or admin.",
                    category="content",
                    value_type="json",
                    display_order=0,
                ),
            )
            print(f"Inserted '{key}' with default training page content.")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
