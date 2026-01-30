#!/usr/bin/env python3
"""
Create a course via TechPath Courses API from a JSON file.

Pass the full course payload as JSON (file path or stdin). The script resolves
category_id from the API if you pass category_slug instead. All other fields
follow the Course API schema (title, slug, description, curriculum, projects,
faqs, learning_outcomes, prerequisites, etc.).

Usage:
  Set env (or .env.local in backend root): BACKEND_API_BASE, ADMIN_EMAIL, ADMIN_PASSWORD.
  Or: ADMIN_TOKEN.

  python scripts/create_course_from_json.py path/to/course.json
  python scripts/create_course_from_json.py --stdin   # read JSON from stdin

  # Optional: use first category if category_id/category_slug missing
  python scripts/create_course_from_json.py path/to/course.json --default-category

Requires: requests (pip install requests)
"""

import argparse
import json
import os
import sys

try:
    import requests
except ImportError:
    print("Error: 'requests' is required. Run: pip install requests")
    sys.exit(1)

# Optional: load .env.local from backend root
_script_dir = os.path.dirname(os.path.abspath(__file__))
_backend_root = os.path.dirname(_script_dir)
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

BACKEND_API_BASE ="http://localhost:8000/api/v1".rstrip("/")
ADMIN_EMAIL ="admin@techpath.biz"
ADMIN_PASSWORD ="TechPath2025!"
ADMIN_TOKEN = os.environ.get("ADMIN_TOKEN", "")


def get_token() -> str:
    if ADMIN_TOKEN:
        return ADMIN_TOKEN.strip()
    if not ADMIN_EMAIL or not ADMIN_PASSWORD:
        print("Set ADMIN_EMAIL and ADMIN_PASSWORD, or ADMIN_TOKEN (e.g. in .env.local).")
        sys.exit(1)
    r = requests.post(
        f"{BACKEND_API_BASE}/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
        timeout=15,
    )
    r.raise_for_status()
    data = r.json()
    token = data.get("access_token")
    if not token:
        raise RuntimeError("Login failed: no access_token in response")
    return token


def get_categories(session: requests.Session) -> list:
    r = session.get(f"{BACKEND_API_BASE}/courses/categories", timeout=15)
    r.raise_for_status()
    return r.json()


def resolve_category_id(session: requests.Session, payload: dict, default_category: bool) -> dict:
    """Ensure payload has category_id. Resolve from category_slug or use first category."""
    if "category_id" in payload and payload["category_id"] is not None:
        return payload

    slug = payload.get("category_slug")
    if slug:
        categories = get_categories(session)
        for c in categories:
            if c.get("slug") == slug:
                payload = dict(payload)
                payload["category_id"] = c["id"]
                payload.pop("category_slug", None)
                return payload
        print(f"Category slug '{slug}' not found.")
        sys.exit(1)

    if default_category:
        categories = get_categories(session)
        if not categories:
            print("No course categories found. Create a category in admin first.")
            sys.exit(1)
        payload = dict(payload)
        payload["category_id"] = categories[0]["id"]
        payload.pop("category_slug", None)
        return payload

    print("Payload must include category_id or category_slug (or use --default-category).")
    sys.exit(1)


def normalize_payload(payload: dict) -> dict:
    """Ensure payload matches API: remove category_slug, ensure nulls for optional."""
    # Deep copy and drop keys API doesn't expect
    out = {}
    for k, v in payload.items():
        if k == "category_slug":
            continue
        out[k] = v
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a course from JSON via Courses API")
    parser.add_argument("json_file", nargs="?", help="Path to course JSON file")
    parser.add_argument("--stdin", action="store_true", help="Read JSON from stdin")
    parser.add_argument("--default-category", action="store_true", help="Use first category if category_id/slug missing")
    args = parser.parse_args()

    if args.stdin:
        raw = sys.stdin.read()
    elif args.json_file:
        with open(args.json_file, encoding="utf-8") as f:
            raw = f.read()
    else:
        parser.print_help()
        sys.exit(1)

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        sys.exit(1)

    if not isinstance(payload, dict):
        print("JSON root must be an object.")
        sys.exit(1)

    if not BACKEND_API_BASE:
        print("Set BACKEND_API_BASE (e.g. http://localhost:8000/api/v1).")
        sys.exit(1)

    print("Backend API:", BACKEND_API_BASE)
    token = get_token()
    print("Auth OK.")

    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {token}"
    session.headers["Content-Type"] = "application/json"

    payload = resolve_category_id(session, payload, args.default_category)
    payload = normalize_payload(payload)

    r = session.post(f"{BACKEND_API_BASE}/courses/", json=payload, timeout=30)

    if r.status_code == 409:
        print("Course with this slug already exists. Delete it first or use a different slug.")
        sys.exit(1)
    r.raise_for_status()

    data = r.json()
    print("Course created successfully.")
    print("  id:", data.get("id"))
    print("  title:", data.get("title"))
    print("  slug:", data.get("slug"))
    print("  status:", data.get("status"))


if __name__ == "__main__":
    main()
