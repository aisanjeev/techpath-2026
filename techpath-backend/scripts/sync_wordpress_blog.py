#!/usr/bin/env python3
"""
WordPress to TechPath Backend – Blog sync script.

Fetches posts, categories, and tags from WordPress REST API and creates/updates
them in the TechPath backend via existing API. No backend code changes required.

Usage:
  Set env vars (or .env.local): BACKEND_API_BASE, ADMIN_EMAIL, ADMIN_PASSWORD.
  Optional: WORDPRESS_API_BASE (default https://techpath.biz)

  python scripts/sync_wordpress_blog.py

Requires: requests (pip install requests)
"""

import json
import os
import re
import sys
from html import unescape
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    print("Error: 'requests' is required. Run: pip install requests")
    sys.exit(1)

# Optional: load .env.local from backend root
_script_dir = os.path.dirname(os.path.abspath(__file__))
_env_path = os.path.join(os.path.dirname(_script_dir), ".env.local")
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

# -----------------------------------------------------------------------------
# Config from environment
# -----------------------------------------------------------------------------
WORDPRESS_API_BASE = os.environ.get("WORDPRESS_API_BASE", "https://techpath.biz").rstrip("/")
WP_JSON = f"{WORDPRESS_API_BASE}/wp-json/wp/v2"

BACKEND_API_BASE = os.environ.get("BACKEND_API_BASE", "http://localhost:8000/api/v1").rstrip("/")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")

# Slug: backend allows only [a-z0-9-]
SLUG_PATTERN = re.compile(r"[^a-z0-9-]+")


def slugify(text: str) -> str:
    """Normalize slug to [a-z0-9-] for backend."""
    s = text.lower().replace("_", "-")
    s = SLUG_PATTERN.sub("-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "post"


def strip_html(html: str) -> str:
    """Remove HTML tags and decode entities."""
    if not html:
        return ""
    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text).strip()
    return unescape(text)


def word_count(html: str) -> int:
    """Approximate word count from HTML content."""
    return len(strip_html(html).split())


# -----------------------------------------------------------------------------
# WordPress API
# -----------------------------------------------------------------------------
def wp_get(path: str, params: dict | None = None) -> requests.Response:
    url = urljoin(f"{WP_JSON}/", path.lstrip("/"))
    r = requests.get(url, params=params or {}, timeout=30)
    r.raise_for_status()
    return r


def wp_get_paginated(path: str, per_page: int = 100) -> list:
    out = []
    page = 1
    while True:
        r = wp_get(path, params={"per_page": per_page, "page": page})
        data = r.json()
        if not data:
            break
        out.extend(data)
        if len(data) < per_page:
            break
        page += 1
    return out


def wp_get_categories() -> list:
    return wp_get_paginated("categories")


def wp_get_tags() -> list:
    return wp_get_paginated("tags")


def wp_get_posts() -> list:
    """Fetch all posts with embedded featured media and terms."""
    out = []
    page = 1
    per_page = 100
    while True:
        r = wp_get(
            "posts",
            params={
                "per_page": per_page,
                "page": page,
                "_embed": "wp:featuredmedia,wp:term",
                "status": "publish",
            },
        )
        data = r.json()
        if not data:
            break
        out.extend(data)
        if len(data) < per_page:
            break
        page += 1
    return out


def wp_post_featured_image_url(post: dict) -> str | None:
    """Get featured image URL from post (with _embed)."""
    emb = post.get("_embedded") or {}
    media = emb.get("wp:featuredmedia") or []
    if not media:
        return None
    m = media[0] if isinstance(media[0], dict) else None
    if not m:
        return None
    return m.get("source_url")


def wp_post_categories(post: dict) -> list:
    """Get category slugs from embedded terms."""
    emb = post.get("_embedded") or {}
    terms = emb.get("wp:term") or []
    slugs = []
    for tax_list in terms:
        for t in tax_list if isinstance(tax_list, list) else []:
            if isinstance(t, dict) and t.get("taxonomy") == "category":
                slugs.append(t.get("slug", ""))
    return [s for s in slugs if s]


def wp_post_tags(post: dict) -> list:
    """Get tag slugs from embedded terms."""
    emb = post.get("_embedded") or {}
    terms = emb.get("wp:term") or []
    slugs = []
    for tax_list in terms:
        for t in tax_list if isinstance(tax_list, list) else []:
            if isinstance(t, dict) and t.get("taxonomy") == "post_tag":
                slugs.append(t.get("slug", ""))
    return [s for s in slugs if s]


# -----------------------------------------------------------------------------
# TechPath Backend API
# -----------------------------------------------------------------------------
class BackendClient:
    def __init__(self, base: str, email: str, password: str):
        self.base = base.rstrip("/")
        self.token = None
        self.session = requests.Session()
        self._login(email, password)

    def _login(self, email: str, password: str) -> None:
        r = self.session.post(
            f"{self.base}/auth/login",
            json={"email": email, "password": password},
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        self.token = data.get("access_token")
        if not self.token:
            raise RuntimeError("Login failed: no access_token in response")
        self.session.headers["Authorization"] = f"Bearer {self.token}"

    def _url(self, path: str) -> str:
        return f"{self.base}/{path.lstrip('/')}"

    def get_categories(self) -> list:
        r = self.session.get(self._url("blog/categories"), timeout=15)
        r.raise_for_status()
        return r.json()

    def get_tags(self) -> list:
        r = self.session.get(self._url("blog/tags"), timeout=15)
        r.raise_for_status()
        return r.json()

    def create_category(self, name: str, slug: str, description: str | None = None) -> dict:
        payload = {
            "name": name,
            "slug": slug,
            "description": description,
            "parent_id": None,
            "display_order": 0,
            "is_active": True,
        }
        r = self.session.post(self._url("blog/categories"), json=payload, timeout=15)
        if r.status_code == 409:
            # Already exists; fetch and return
            for c in self.get_categories():
                if c.get("slug") == slug:
                    return c
            raise RuntimeError(f"Category slug {slug} conflict but not found in list")
        r.raise_for_status()
        return r.json()

    def create_tag(self, name: str, slug: str) -> dict:
        payload = {"name": name, "slug": slug}
        r = self.session.post(self._url("blog/tags"), json=payload, timeout=15)
        if r.status_code == 409:
            for t in self.get_tags():
                if t.get("slug") == slug:
                    return t
            raise RuntimeError(f"Tag slug {slug} conflict but not found in list")
        r.raise_for_status()
        return r.json()

    def get_post_by_slug(self, slug: str) -> dict | None:
        r = self.session.get(self._url(f"blog/posts/{slug}"), timeout=15)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()

    def create_post(self, payload: dict) -> dict:
        r = self.session.post(self._url("blog/posts"), json=payload, timeout=30)
        return r

    def update_post(self, post_id: int, payload: dict) -> dict:
        r = self.session.put(self._url(f"blog/posts/{post_id}"), json=payload, timeout=30)
        r.raise_for_status()
        return r.json()


# -----------------------------------------------------------------------------
# Sync logic
# -----------------------------------------------------------------------------
def main() -> None:
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv

    if not dry_run and (not BACKEND_API_BASE or not ADMIN_EMAIL or not ADMIN_PASSWORD):
        print(
            "Set BACKEND_API_BASE, ADMIN_EMAIL, ADMIN_PASSWORD (e.g. in .env.local or export)."
        )
        sys.exit(1)

    print("WordPress API:", WP_JSON)
    print("Backend API:", BACKEND_API_BASE)
    if dry_run:
        print("Mode: DRY RUN (no backend writes)")
    print()

    # 1) Login (skip in dry-run)
    client = None
    if not dry_run:
        try:
            client = BackendClient(BACKEND_API_BASE, ADMIN_EMAIL, ADMIN_PASSWORD)
        except Exception as e:
            print("Backend login failed:", e)
            sys.exit(1)
        print("Backend login OK.")

    # 2) Fetch WP data
    print("Fetching WordPress categories...")
    wp_cats = wp_get_categories()
    print("  ", len(wp_cats), "categories")
    print("Fetching WordPress tags...")
    wp_tags = wp_get_tags()
    print("  ", len(wp_tags), "tags")
    print("Fetching WordPress posts...")
    wp_posts = wp_get_posts()
    print("  ", len(wp_posts), "posts")

    if dry_run:
        print()
        print("Dry run: would sync", len(wp_posts), "posts,", len(wp_cats), "categories,", len(wp_tags), "tags.")
        if wp_posts:
            p = wp_posts[0]
            slug = slugify(p.get("slug", ""))[:255] or slugify(str(p.get("id")))[:255]
            print("First post slug:", slug, "| title:", (p.get("title") or {}).get("rendered", "")[:60])
        sys.exit(0)

    # 3) Backend slug -> id maps
    backend_cats = {c["slug"]: c["id"] for c in client.get_categories()}
    backend_tags = {t["slug"]: t["id"] for t in client.get_tags()}
    print("Backend already has", len(backend_cats), "categories,", len(backend_tags), "tags.")

    # 4) Ensure all WP categories exist in backend
    for c in wp_cats:
        slug = slugify(c.get("slug", ""))
        name = (c.get("name") or "").strip() or slug
        if not slug:
            continue
        if slug not in backend_cats:
            try:
                created = client.create_category(
                    name=name,
                    slug=slug,
                    description=strip_html(c.get("description", "")) or None,
                )
                backend_cats[slug] = created["id"]
                print("  Created category:", slug)
            except Exception as e:
                print("  Skip category", slug, ":", e)
    print("Categories synced.")

    # 5) Ensure all WP tags exist in backend
    for t in wp_tags:
        slug = slugify(t.get("slug", ""))
        name = (t.get("name") or "").strip() or slug
        if not slug:
            continue
        if slug not in backend_tags:
            try:
                created = client.create_tag(name=name, slug=slug)
                backend_tags[slug] = created["id"]
                print("  Created tag:", slug)
            except Exception as e:
                print("  Skip tag", slug, ":", e)
    print("Tags synced.")

    # Ensure at least one category exists so we can assign posts
    if not backend_cats:
        try:
            created = client.create_category(
                name="Uncategorized",
                slug="uncategorized",
                description=None,
            )
            backend_cats["uncategorized"] = created["id"]
            print("Created fallback category: uncategorized")
        except Exception as e:
            print("Could not create fallback category:", e)
            print("Posts need at least one category. Create one in the admin and re-run.")
    if not backend_cats:
        print("No categories in backend. Aborting post sync.")
        sys.exit(1)

    # 6) Sync posts
    created_count = 0
    updated_count = 0
    error_count = 0

    for i, post in enumerate(wp_posts):
        wp_id = post.get("id")
        title = (post.get("title") or {}).get("rendered", "")
        if isinstance(title, str):
            title = strip_html(title)
        title = (title.strip() or "Untitled")[:255]
        slug = slugify(post.get("slug", ""))[:255]
        if not slug:
            slug = slugify(str(wp_id))[:255]

        content = (post.get("content") or {}).get("rendered", "")
        if not content or len(strip_html(content)) < 10:
            content = "<p>No content.</p>"

        excerpt_raw = (post.get("excerpt") or {}).get("rendered", "")
        excerpt = strip_html(excerpt_raw).strip()[:500] if excerpt_raw else None

        featured_image = wp_post_featured_image_url(post)

        cat_slugs = wp_post_categories(post)
        category_id = None
        if cat_slugs:
            for cs in cat_slugs:
                cs_norm = slugify(cs)
                if cs_norm in backend_cats:
                    category_id = backend_cats[cs_norm]
                    break
        if not category_id and backend_cats:
            category_id = backend_cats.get("uncategorized") or next(
                iter(backend_cats.values())
            )

        if not category_id:
            print(f"  Skip post (no category): {slug}")
            error_count += 1
            continue

        tag_slugs = wp_post_tags(post)
        tag_ids = [backend_tags[slugify(t)] for t in tag_slugs if slugify(t) in backend_tags]

        status = "published" if (post.get("status") == "publish") else "draft"
        date_str = post.get("date") or post.get("modified")
        published_at = f"{date_str}Z" if date_str and "Z" not in date_str else date_str

        reading_time = max(1, (word_count(content) // 200) + 1)

        payload = {
            "title": title,
            "slug": slug,
            "content": content,
            "content_type": "html",
            "excerpt": excerpt,
            "featured_image": featured_image,
            "category_id": category_id,
            "tag_ids": tag_ids,
            "status": status,
            "featured": bool(post.get("sticky")),
            "reading_time": reading_time,
            "published_at": published_at,
            "meta_title": (title or "")[:255] or None,
            "meta_description": (excerpt or "")[:500] or None,
        }

        try:
            resp = client.create_post(payload)
            if resp.status_code in (200, 201):
                created_count += 1
                print("  Created:", slug)
            elif resp.status_code == 409:
                existing = client.get_post_by_slug(slug)
                if existing:
                    update_payload = {
                        "title": payload["title"],
                        "content": payload["content"],
                        "content_type": payload["content_type"],
                        "excerpt": payload["excerpt"],
                        "featured_image": payload["featured_image"],
                        "category_id": payload["category_id"],
                        "tag_ids": payload["tag_ids"],
                        "status": payload["status"],
                        "featured": payload["featured"],
                        "reading_time": payload["reading_time"],
                        "published_at": payload["published_at"],
                        "meta_title": payload["meta_title"],
                        "meta_description": payload["meta_description"],
                    }
                    client.update_post(existing["id"], update_payload)
                    updated_count += 1
                    print("  Updated:", slug)
                else:
                    error_count += 1
                    print("  Conflict but get failed:", slug)
            else:
                error_count += 1
                print("  Error", resp.status_code, slug)
                try:
                    err_body = resp.json() if resp.text else {}
                    print("    Response:", json.dumps(err_body, indent=2)[:500])
                except Exception:
                    print("    Response:", (resp.text or "")[:400])
        except Exception as e:
            error_count += 1
            print("  Exception", slug, ":", e)

    print()
    print("Done. Created:", created_count, "Updated:", updated_count, "Errors:", error_count)


if __name__ == "__main__":
    main()
