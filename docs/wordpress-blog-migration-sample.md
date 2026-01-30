# WordPress Blog Migration – One Post Sample (Scraped)

This document shows **one post** from `https://techpath.biz/wp-json/wp/v2/posts` after scraping and normalizing for the current TechPath backend (categories, tags, content, featured image).

---

## 1. Raw WordPress API Summary (Post ID 22524)

| Field | WordPress API | Notes |
|-------|----------------|--------|
| **id** | 22524 | WP post ID (ignore for new system) |
| **slug** | `techpath-delivering-it-excellence-pan-india` | Use as-is |
| **title** | `TechPath: Delivering IT Excellence PAN India` | From `title.rendered` (strip HTML if any) |
| **date** | 2025-09-27T05:55:36 | Use for `published_at` |
| **status** | publish | Map to `published` |
| **categories** | [117] | Resolve 117 → category name/slug |
| **tags** | [] | This post has no tags |
| **featured_media** | 22527 | Resolve to image URL via `/wp/v2/media/22527` |
| **content** | HTML in `content.rendered` | Elementor markup; keep as HTML |
| **excerpt** | HTML in `excerpt.rendered` | Strip tags for short excerpt |

---

## 2. Resolved Category (from `/wp/v2/categories/117`)

| Field | Value |
|-------|--------|
| **id** | 117 |
| **name** | Services |
| **slug** | services |
| **description** | (HTML from WP; can strip for migration) |

**Current system:** Create or match `BlogCategory` with `name: "Services"`, `slug: "services"`, then use its `id` as `category_id` on the post.

---

## 3. Resolved Featured Image (from `/wp/v2/media/22527`)

| Field | Value |
|-------|--------|
| **id** | 22527 |
| **source_url** | `https://techpath.biz/wp-content/uploads/2025/09/ChatGPT-Image-Sep-26-2025-10_55_27-PM.webp` |
| **file path** | `2025/09/ChatGPT-Image-Sep-26-2025-10_55_27-PM.webp` |
| **alt_text** | TechPath: Delivering IT Excellence PAN India |

**Options for current system:**

- **A) Store full URL**  
  `featured_image`: `https://techpath.biz/wp-content/uploads/2025/09/ChatGPT-Image-Sep-26-2025-10_55_27-PM.webp`  
  (keeps images on WordPress until you move them.)

- **B) Download and re-upload**  
  Download the file, upload via your backend media API, then set `featured_image` to the new path/URL returned by your system.

---

## 4. One Post – Normalized Payload for Current TechPath Backend

This is the shape you can feed into your **BlogPostCreate** API (or equivalent) for one post.

### Category (create first if not exists)

```json
{
  "name": "Services",
  "slug": "services",
  "description": null,
  "parent_id": null,
  "display_order": 0,
  "is_active": true
}
```

### Tags (this post has none; example for others)

```json
[]
```

For a post that has tags, you’d have e.g. `[{"name": "AI", "slug": "ai"}, ...]` and create/fetch tag IDs to pass as `tag_ids`.

### Post payload (single post – ready to feed)

```json
{
  "title": "TechPath: Delivering IT Excellence PAN India",
  "slug": "techpath-delivering-it-excellence-pan-india",
  "content": "<div data-elementor-type=\"wp-post\" ...>(full HTML from content.rendered)</div>",
  "content_type": "html",
  "excerpt": "Technology is no longer a luxury-it is the backbone of modern businesses and a catalyst for personal growth. Across India, companies are adapting digital solutions to expand their reach, improve …",
  "featured_image": "https://techpath.biz/wp-content/uploads/2025/09/ChatGPT-Image-Sep-26-2025-10_55_27-PM.webp",
  "category_id": 1,
  "tag_ids": [],
  "status": "published",
  "featured": false,
  "reading_time": 5,
  "published_at": "2025-09-27T05:55:36+00:00",
  "meta_title": "TechPath: Delivering IT Excellence PAN India",
  "meta_description": "Technology is no longer a luxury-it is the backbone of modern businesses and a catalyst for personal growth. Across India, companies are adapting digital solutions to expand their reach, improve …"
}
```

**Notes:**

- **category_id**: Use the ID of the category after it’s created in your DB (e.g. 1 for “Services”).
- **excerpt**: Plain text or very short HTML; stripped from WordPress `excerpt.rendered`.
- **content**: Full HTML from WordPress `content.rendered` (Elementor markup preserved).
- **featured_image**: Full image URL as above; replace with your own path if you download and re-upload.
- **reading_time**: Optional; can be computed (e.g. word count / 200) or taken from Yoast if available.

---

## 5. Field Mapping: WordPress → TechPath Backend

| WordPress (WP-API) | TechPath backend |
|--------------------|------------------|
| `title.rendered` | `title` |
| `slug` | `slug` |
| `content.rendered` | `content` |
| `content_type` | always `"html"` for WP |
| `excerpt.rendered` (strip HTML) | `excerpt` |
| `featured_media` → resolve to media `source_url` | `featured_image` (URL or path) |
| `categories[]` → resolve to category slug/name, get or create | `category_id` |
| `tags[]` → resolve to tag slug/name, get or create | `tag_ids` |
| `status` (publish/draft) | `status` (published/draft) |
| `date` | `published_at` |
| Yoast `meta_title` / `og_title` | `meta_title` |
| Yoast `og_description` / meta description | `meta_description` |
| Optional: word count / 200 | `reading_time` |

---

## 6. Content Snippet (first ~500 chars of `content.rendered`)

The full post body is long; here is the start (HTML from WordPress):

```html
<div data-elementor-type="wp-post" data-elementor-id="22524" class="elementor elementor-22524">
  <section class="elementor-section ...">
    <div class="elementor-widget-wrap ...">
      <p>Technology is no longer a luxury-it is the<strong> backbone of modern businesses</strong> and a catalyst for personal growth. Across India, companies are adapting digital solutions to expand their reach, improve efficiency, and stay competitive. At the same time, students and professionals are<strong> seeking career-ready</strong> training to meet the demands of a digital-first economy.</p>
      <p>In this rapidly evolving landscape, <strong>TechPath Research and Development Pvt. Ltd.</strong> has positioned itself as a <strong>one-stop technology partner.</strong> ...
```

You will feed the **entire** `content.rendered` string into `content` (as in section 4).

---

## 7. Image Path Summary (this post)

| Use | Value |
|-----|--------|
| **Full URL** | `https://techpath.biz/wp-content/uploads/2025/09/ChatGPT-Image-Sep-26-2025-10_55_27-PM.webp` |
| **Relative path (WP)** | `2025/09/ChatGPT-Image-Sep-26-2025-10_55_27-PM.webp` |
| **Alt text** | TechPath: Delivering IT Excellence PAN India |

---

## How to Run the Full Sync (No Extra Backend Work)

A **sync script** runs the full migration using your existing backend API:

1. **Location:** [techpath-backend/scripts/sync_wordpress_blog.py](techpath-backend/scripts/sync_wordpress_blog.py)
2. **Docs:** [techpath-backend/scripts/README.md](techpath-backend/scripts/README.md)

**Steps:**

1. Install: `pip install requests`
2. Set env (or use backend `.env.local`):
   - `BACKEND_API_BASE` = `http://localhost:8000/api/v1` (or your backend URL)
   - `ADMIN_EMAIL` = admin email
   - `ADMIN_PASSWORD` = admin password
3. From `techpath-backend`:  
   `python scripts/sync_wordpress_blog.py`

The script:

- Fetches all WordPress categories and tags, creates missing ones in the backend.
- Fetches all published posts (with embedded featured media and terms).
- Creates each post; if slug already exists (409), updates that post.
- Uses the same mapping as this document (category, tag, content, image path).

**If no blog posts appear in the backend:**

1. Start the backend first (`poetry run uvicorn app.main:app --reload`).
2. Run a dry run to confirm WordPress data:  
   `python scripts/sync_wordpress_blog.py --dry-run`  
   You should see e.g. "would sync 52 posts, 7 categories, 29 tags".
3. Set `BACKEND_API_BASE`, `ADMIN_EMAIL`, `ADMIN_PASSWORD` (same admin as the admin panel) and run without `--dry-run`.
4. Check the script output: "Created: slug" or "Updated: slug" per post; any "Error 422" lines show validation failures (script prints the response body).
5. Ensure the backend has blog tables: run `alembic upgrade head` in the backend directory if you have not already.
