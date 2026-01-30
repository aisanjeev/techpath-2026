#!/usr/bin/env python3
"""
Seed all page content keys into app_settings (idempotent).

Inserts home_landing_content, about_page_content, services_landing_content,
contact_page_content, pricing_page_content, privacy_page_content, terms_page_content, cookie_page_content (and optionally training_landing_content) with default JSON.
Skips insert if key already exists unless --force.

Usage:
  cd techpath-backend
  python scripts/seed_page_content.py
  python scripts/seed_page_content.py --force   # overwrite all with defaults
  python scripts/seed_page_content.py --training # also seed training_landing_content

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


PAGE_CONTENT_ENTRIES = [
    (
        "home_landing_content",
        "Home Landing Page Content",
        "JSON for / page: hero, stats, services, features, testimonials, FAQs, CTA. Edit via API or admin.",
        "get_builtin_home_content",
    ),
    (
        "about_page_content",
        "About Page Content",
        "JSON for /about page: hero, mission, stats, values, team, CTA. Edit via API or admin.",
        "get_builtin_about_content",
    ),
    (
        "services_landing_content",
        "Services Landing Page Content",
        "JSON for /services page: hero, CTA. Edit via API or admin.",
        "get_builtin_services_content",
    ),
    (
        "contact_page_content",
        "Contact Page Content",
        "JSON for /contact page: hero, contact methods. Edit via API or admin.",
        "get_builtin_contact_content",
    ),
    (
        "pricing_page_content",
        "Pricing Page Content",
        "JSON for /pricing page: hero, plans, FAQs, CTA. Edit via API or admin.",
        "get_builtin_pricing_content",
    ),
    (
        "privacy_page_content",
        "Privacy Policy Page Content",
        "JSON for /privacy page: seo, page_title, last_updated, markdown_content. Edit via API or admin.",
        "get_builtin_privacy_content",
    ),
    (
        "terms_page_content",
        "Terms of Service Page Content",
        "JSON for /terms page: seo, page_title, last_updated, markdown_content. Edit via API or admin.",
        "get_builtin_terms_content",
    ),
    (
        "cookie_page_content",
        "Cookie Policy Page Content",
        "JSON for /cookies page: seo, page_title, last_updated, markdown_content. Edit via API or admin.",
        "get_builtin_cookie_content",
    ),
]

TRAINING_ENTRY = (
    "training_landing_content",
    "Training Landing Page Content",
    "JSON for /training page: hero, pain points, USPs, FAQs, stories, offer banner, CTA. Edit via API or admin.",
    "get_builtin_training_content",
)


async def main() -> None:
    parser = argparse.ArgumentParser(description="Seed page content into app_settings")
    parser.add_argument("--force", action="store_true", help="Overwrite existing values with defaults")
    parser.add_argument("--training", action="store_true", help="Also seed training_landing_content")
    args = parser.parse_args()

    from app.api.v1.endpoints.content import (
        get_builtin_about_content,
        get_builtin_contact_content,
        get_builtin_cookie_content,
        get_builtin_home_content,
        get_builtin_privacy_content,
        get_builtin_pricing_content,
        get_builtin_services_content,
        get_builtin_terms_content,
        get_builtin_training_content,
    )
    from app.crud.app_setting import app_setting_crud
    from app.db.session import AsyncSessionLocal, engine
    from app.schemas.app_setting import AppSettingCreate

    builtin_fns = {
        "get_builtin_home_content": get_builtin_home_content,
        "get_builtin_about_content": get_builtin_about_content,
        "get_builtin_services_content": get_builtin_services_content,
        "get_builtin_contact_content": get_builtin_contact_content,
        "get_builtin_pricing_content": get_builtin_pricing_content,
        "get_builtin_privacy_content": get_builtin_privacy_content,
        "get_builtin_terms_content": get_builtin_terms_content,
        "get_builtin_cookie_content": get_builtin_cookie_content,
        "get_builtin_training_content": get_builtin_training_content,
    }

    entries = list(PAGE_CONTENT_ENTRIES)
    if args.training:
        entries.append(TRAINING_ENTRY)

    try:
        async with AsyncSessionLocal() as db:
            for key, display_name, description, fn_name in entries:
                get_builtin = builtin_fns[fn_name]
                default_dict = get_builtin()
                value = json.dumps(default_dict, ensure_ascii=False)

                existing = await app_setting_crud.get_by_key(db, key)
                if existing and not args.force:
                    print(f"Key '{key}' already exists. Skipping.")
                    continue
                if existing and args.force:
                    await app_setting_crud.update_value(db, key, value)
                    print(f"Updated '{key}' ({display_name}).")
                    continue
                await app_setting_crud.create(
                    db,
                    AppSettingCreate(
                        key=key,
                        value=value,
                        display_name=display_name,
                        description=description,
                        category="content",
                        value_type="json",
                        display_order=0,
                    ),
                )
                print(f"Inserted '{key}' ({display_name}).")
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
