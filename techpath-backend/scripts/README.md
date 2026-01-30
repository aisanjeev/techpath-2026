# TechPath Backend Scripts

## Create Python Course (`create_python_course.py`)

Creates the **Python Programming** course via the Courses API with full content: markdown description (with code blocks), curriculum, projects, learning outcomes, prerequisites, pricing, and SEO.

### Requirements

- Python 3.11+
- `requests`: `pip install requests`
- Backend running; at least one course category (e.g. Programming) in the admin.

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `BACKEND_API_BASE` | Backend API base URL | `http://localhost:8000/api/v1` |
| `ADMIN_EMAIL` | Admin user email (for JWT) | `admin@techpath.biz` |
| `ADMIN_PASSWORD` | Admin password | your password |
| `ADMIN_TOKEN` | Optional: Bearer token (skip login) | JWT string |

The script loads `.env.local` from the backend root if present.

### Run

1. Start the backend (if local):
   ```bash
   cd techpath-backend
   poetry run uvicorn app.main:app --reload
   ```

2. In another terminal, set credentials and run:
   ```bash
   cd techpath-backend
   set BACKEND_API_BASE=http://localhost:8000/api/v1
   set ADMIN_EMAIL=your-admin@techpath.biz
   set ADMIN_PASSWORD=your-password
   python scripts/create_python_course.py
   ```
   On Linux/macOS use `export` instead of `set`.

3. If the course with slug `python-programming` already exists, delete it in the admin first, or the script will exit with 409.

---

## Create Course from JSON (`create_course_from_json.py`)

**Generic script:** pass any course JSON file and it creates the course via the API. The payload must match the Course API (title, slug, description, curriculum, projects, **faqs**, learning_outcomes, prerequisites, etc.). Use `category_id` in the JSON, or `category_slug` to resolve by slug, or omit both and use `--default-category` to use the first category.

### Run

```bash
cd techpath-backend
# Use first category if JSON has no category_id/category_slug
python scripts/create_course_from_json.py scripts/courses/digital-marketing-gen-ai.json --default-category
```

Or with a specific category in JSON (set `"category_id": 1` or `"category_slug": "marketing"` in the file):

```bash
python scripts/create_course_from_json.py path/to/course.json
```

Read JSON from stdin:

```bash
cat course.json | python scripts/create_course_from_json.py --stdin --default-category
```

### Sample course JSON

- **`scripts/courses/digital-marketing-gen-ai.json`** – Digital Marketing using Gen AI, 6 months, with FAQs, curriculum, projects, and full description. Run with `--default-category` if the file has no `category_id`.

---

## Seed Training Page (`seed_training_page.py`)

Seeds the **training landing page** content into `app_settings` (key `training_landing_content`) so the `/training` page has hero, pain points, USPs, FAQs, stories, and offer banner from the API. Idempotent: skips insert if the key already exists. Use `--force` to overwrite with defaults.

**Run (from backend root):**

```bash
cd techpath-backend
python scripts/seed_training_page.py
python scripts/seed_training_page.py --force   # overwrite existing
```

Requires backend deps (`poetry install`) and `DATABASE_URL` (or default SQLite). The frontend fetches content from `GET /api/v1/content/training-page`; if the key is missing, the API returns a built-in default so the page still works.

---

## Seed Page Content (`seed_page_content.py`)

Seeds **all page content** keys into `app_settings`: `home_landing_content`, `about_page_content`, `services_landing_content`, `contact_page_content`, `pricing_page_content`, `privacy_page_content`, `terms_page_content`, `cookie_page_content`. Optional: add `--training` to also seed `training_landing_content`. Policy pages (privacy, terms, cookie) store body content as **markdown**. Idempotent: skips insert if a key already exists. Use `--force` to overwrite with defaults.

**Run (from backend root):**

```bash
cd techpath-backend
python scripts/seed_page_content.py              # home, about, services, contact
python scripts/seed_page_content.py --training   # also training page
python scripts/seed_page_content.py --force      # overwrite all with defaults
```

The frontend fetches content from `GET /api/v1/content/home-page`, `/about-page`, `/services-page`, `/contact-page`, `/pricing-page`, `/privacy-page`, `/terms-page`, `/cookie-page` (and `/training-page`). If a key is missing, each API returns a built-in default. Seeded JSON includes **SEO** for each page (`seo.title`, `seo.description`, optional `seo.image`, `seo.canonical_url`, `seo.no_index`). Edit content in **Admin > Settings > App Settings** (Content category) via the JSON popup.

---

## WordPress Blog Sync (`sync_wordpress_blog.py`)

Syncs blog posts, categories, and tags from WordPress (techpath.biz) to the TechPath backend using existing APIs. No backend code changes required.

### Requirements

- Python 3.11+
- `requests`: `pip install requests`

### Environment Variables

Set these before running (e.g. in `.env.local` in the backend root, or export):

| Variable | Description | Example |
|----------|-------------|---------|
| `BACKEND_API_BASE` | Backend API base URL | `http://localhost:8000/api/v1` |
| `ADMIN_EMAIL` | Admin user email (for JWT) | `admin@techpath.biz` |
| `ADMIN_PASSWORD` | Admin password | your password |
| `WORDPRESS_API_BASE` | WordPress site URL (optional) | `https://techpath.biz` |

The script will load `.env.local` from the backend root if present (simple key=value parsing).

### Run

1. **Start the backend** (so the script can call it):
   ```bash
   cd techpath-backend
   poetry run uvicorn app.main:app --reload
   ```
   Leave it running in one terminal.

2. **Set credentials** and run the sync in another terminal:
   ```bash
   cd techpath-backend
   set BACKEND_API_BASE=http://localhost:8000/api/v1
   set ADMIN_EMAIL=your-admin@techpath.biz
   set ADMIN_PASSWORD=your-password
   python scripts/sync_wordpress_blog.py
   ```
   On Linux/macOS use `export` instead of `set`.  
   For a **remote** backend (e.g. staging):  
   `set BACKEND_API_BASE=https://staging.api.techpath.biz/api/v1`

3. **Optional – dry run** (fetch from WordPress only, no backend writes):
   ```bash
   python scripts/sync_wordpress_blog.py --dry-run
   ```
   You should see: "would sync 52 posts, 7 categories, 29 tags" (or similar).

4. **Using `.env.local`**: Put `BACKEND_API_BASE`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` in `techpath-backend/.env.local`; the script loads it and you can run:
   ```bash
   python scripts/sync_wordpress_blog.py
   ```

### Behavior

- Fetches all **categories** and **tags** from WordPress, creates any missing ones in the backend.
- Fetches all **published posts** with embedded featured media and terms.
- For each post: creates it if the slug is new; if the slug already exists (409), updates the existing post.
- Featured image is stored as the WordPress image URL (no download). Content and excerpt are normalized (HTML stripped for excerpt).
- Slug is normalized to `[a-z0-9-]+` to match backend validation.

### Errors

- **Backend login failed / connection refused**: Start the backend first and use the correct `BACKEND_API_BASE` (no trailing slash). Example: `http://localhost:8000/api/v1`.
- **Invalid email or password**: Use the same admin email/password you use in the admin panel.
- **Conflict / 409**: Script will update the existing post by slug (no error).
- **Error 422**: Backend validation failed; the script prints the response body (e.g. slug pattern, field length). Fix the payload or backend rules.
- **No categories**: The script creates all WordPress categories first; if none exist it creates "Uncategorized". Ensure the backend blog tables are migrated (`alembic upgrade head`).
