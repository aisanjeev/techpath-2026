#!/usr/bin/env python3
"""Seed training modules for Python Full Stack Gen AI via the production API.

Idempotent: safe to run multiple times.
"""

import json
import os
import re
import sys
import time
from pathlib import Path

# Fix Windows encoding
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import httpx

# ─── Configuration ──────────────────────────────────────────────────────────────

API_BASE = "https://api.techpath.biz/api/v1"
TOKEN = os.environ.get("SEED_TOKEN", "").strip()
PROGRAM_ID = 2
ASSETS_DIR = Path(r"D:\project\techpath\techpath-2026\syllabus\python-full-stack\assests")
DELAY = 0.15  # seconds between API calls to avoid rate limiting

client = httpx.Client(
    base_url=API_BASE,
    headers={"Authorization": f"Bearer {TOKEN}"},
    timeout=60,
)

# ─── Helpers ────────────────────────────────────────────────────────────────────

def api_get(path):
    time.sleep(DELAY)
    r = client.get(path)
    return r

def api_post_json(path, payload):
    time.sleep(DELAY)
    r = client.post(path, json=payload)
    return r

def api_put_json(path, payload):
    time.sleep(DELAY)
    r = client.put(path, json=payload)
    return r

def api_delete(path):
    time.sleep(DELAY)
    r = client.delete(path)
    return r

def api_upload_file(filepath: Path, asset_type: str):
    """Upload a file via the lecture-asset upload endpoint → returns media_file_id."""
    time.sleep(DELAY)
    content_type = "text/html" if filepath.suffix == ".html" else "application/octet-stream"
    with open(filepath, "rb") as f:
        r = client.post(
            f"/uploads/lecture-asset?asset_type={asset_type}",
            files={"file": (filepath.name, f, content_type)},
        )
    if r.status_code >= 400:
        print(f"    UPLOAD ERROR {r.status_code}: {r.text[:300]}")
        return None
    data = r.json()
    media_id = data["data"]["id"]
    is_dup = data.get("is_duplicate", False)
    print(f"    Uploaded {filepath.name} → media_file_id={media_id} {'(dedup)' if is_dup else ''}")
    return media_id

def extract_md_title(content: str, default: str) -> str:
    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return m.group(1).strip() if m else default

def extract_md_description(content: str, max_len: int = 450) -> str:
    # Highly accurate semantic extraction:
    # Remove HTML comments, markdown images, and initial title headings
    text = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    text = re.sub(r'^#[^\n]*\n', '', text, count=1).strip()
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    
    # Extract the first substantive paragraph(s) that are not headings, code blocks, or tables
    paragraphs = []
    in_code_block = False
    for line in text.split('\n'):
        line_stripped = line.strip()
        if line_stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block or not line_stripped or line_stripped.startswith('#') or line_stripped.startswith('|'):
            continue
        # Remove formatting (bold, links, inline code)
        clean_line = re.sub(r'\*\*(.*?)\*\*', r'\1', line_stripped)
        clean_line = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', clean_line)
        clean_line = re.sub(r'`(.*?)`', r'\1', clean_line)
        paragraphs.append(clean_line)
        if len(' '.join(paragraphs)) > max_len + 100:
            break
            
    if paragraphs:
        desc = ' '.join(paragraphs).replace('\r', '').strip()
        if len(desc) > max_len:
            # truncate at the last full word
            desc = desc[:max_len].rsplit(' ', 1)[0] + '...'
        return desc
    return ""

def filename_to_title(name: str) -> str:
    stem = Path(name).stem
    stem = re.sub(r'^\d+-', '', stem)
    return stem.replace('-', ' ').replace('_', ' ').title()

def foldername_to_meta(name: str) -> dict:
    # Example: module-01-python-core
    m = re.match(r'^module-(\d+)-(.+)$', name)
    if m:
        num = int(m.group(1))
        topic = m.group(2).replace('-', ' ').title()
        topic = topic.replace('Uiux', 'UI/UX').replace('Ai', 'AI').replace('Cicd', 'CI/CD').replace('Api', 'API')
        return {
            "title": f"Module {num:02d} - {topic}",
            "description": f"Comprehensive learning materials for {topic}.",
            "display_order": num,
            "tags": [topic.lower().replace(' ', '-'), "python-fullstack"]
        }
    return {
        "title": filename_to_title(name),
        "description": f"Learning materials for {filename_to_title(name)}",
        "display_order": 99,
        "tags": ["python-fullstack"]
    }

def get_file_sort_key(name: str):
    n = name.lower()
    m = re.match(r'^(\d+)-', n)
    if m:
        return (0, int(m.group(1)), n)
    order = {'code-': 1, 'assignment-': 2, 'lab-': 3, 'quiz-': 4, 'cheatsheet-': 5, 'notes-': 6, 'resources-': 7}
    for prefix, o in order.items():
        if n.startswith(prefix):
            sub = 0 if n.endswith('.json') else 1
            return (1, o, sub, n)
    return (2, 0, 0, n)

def classify_file(filepath: Path) -> dict | None:
    name = filepath.name.lower()
    ext = filepath.suffix.lower()

    if ext == '.html':
        return {"asset_type": "html_bundle", "needs_upload": True}
    if name.startswith('assignment-') and ext == '.md':
        return {"asset_type": "assignment"}
    if name.startswith('cheatsheet-') and ext == '.md':
        return {"asset_type": "cheat_sheet"}
    if name.startswith('lab-') and ext == '.json':
        return {"asset_type": "lab"}
    if name.startswith('quiz-') and ext == '.json':
        return {"asset_type": "quiz"}
    if name.startswith('quiz-') and ext == '.md':
        return {"asset_type": "markdown"}  # readable quiz reference
    if name.startswith('notes-') and ext == '.md':
        return {"asset_type": "notes"}
    if name.startswith('resources-') and ext == '.md':
        return {"asset_type": "notes"}
    if name.startswith('code-') or ext in ['.py', '.sql', '.js', '.css', '.html', '.yml', '.yaml', '.sh', '.dockerfile']:
        lang_map = {'.py': 'python', '.sql': 'sql', '.css': 'css', '.yml': 'yaml', '.yaml': 'yaml', '.js': 'javascript', '.sh': 'bash', '.html': 'html'}
        lang = lang_map.get(ext, 'text')
        if ext == '' or ext == '.dockerfile':
            lang = 'dockerfile'
        return {"asset_type": "code_snippet", "language": lang}
    if ext == '.md':
        return {"asset_type": "markdown"}

    print(f"    SKIP unrecognized file: {filepath.name}")
    return None

def build_asset_payload(filepath: Path, meta: dict, classification: dict):
    try:
        content = filepath.read_text(encoding='utf-8-sig')
    except UnicodeDecodeError:
        content = filepath.read_text(encoding='latin-1')

    atype = classification["asset_type"]
    mod_tags = meta["tags"]
    topic = meta["title"].split(" - ", 1)[1] if " - " in meta["title"] else meta["title"]

    if atype == "markdown":
        title = extract_md_title(content, filename_to_title(filepath.name))
        desc = extract_md_description(content) or f"Lecture material for {topic}"
        return {
            "asset_type": "markdown",
            "title": title,
            "description": desc[:500],
            "tags": mod_tags,
            "status": "published",
            "body": content,
        }

    elif atype == "notes":
        title = extract_md_title(content, filename_to_title(filepath.name))
        desc = extract_md_description(content) or f"Study notes for {topic}"
        extra = ["notes", "revision"] if filepath.name.startswith("notes-") else ["resources", "links"]
        return {
            "asset_type": "notes",
            "title": title,
            "description": desc[:500],
            "tags": mod_tags + extra,
            "status": "published",
            "body": content,
        }

    elif atype == "cheat_sheet":
        title = extract_md_title(content, f"Cheat Sheet — {topic}")
        desc = f"Quick reference and revision sheet for {topic}"
        return {
            "asset_type": "cheat_sheet",
            "title": title,
            "description": desc[:500],
            "tags": mod_tags + ["cheat-sheet", "quick-reference"],
            "status": "published",
            "body": content,
        }

    elif atype == "code_snippet":
        lang = classification.get("language", "text")
        title = filename_to_title(filepath.name)
        first_line = content.strip().split('\n')[0] if content.strip() else ''
        if lang == "python" and first_line.startswith('#') and not first_line.startswith('#!'):
            t = first_line.lstrip('# ').strip()
            if 5 < len(t) < 200:
                title = t
        elif lang == "sql" and first_line.startswith('--'):
            t = first_line.lstrip('- ').strip()
            if 5 < len(t) < 200:
                title = t
        elif lang == "yaml" and first_line.startswith('#'):
            t = first_line.lstrip('# ').strip()
            if 5 < len(t) < 200:
                title = t
        elif lang in ["javascript", "css"] and first_line.startswith('/*'):
            t = first_line.lstrip('/* ').rstrip('*/ ').strip()
            if 5 < len(t) < 200:
                title = t
                
        # Deep extract for code descriptions from block comments or first multiple lines
        desc_lines = []
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('import') or line.startswith('from '):
                if desc_lines: break
                continue
            if line.startswith('#') or line.startswith('--') or line.startswith('/*') or line.startswith('*') or line.startswith('"""'):
                clean = line.strip('#-/*" ')
                if clean: desc_lines.append(clean)
            elif desc_lines:
                break
        desc = ' '.join(desc_lines) if desc_lines else f"{lang.title()} code example for {topic}"
        
        return {
            "asset_type": "code_snippet",
            "title": title,
            "description": desc[:500] if len(desc) < 500 else desc[:497] + "...",
            "tags": mod_tags + ["code-example", lang],
            "status": "published",
            "body": content,
            "language": lang,
        }

    elif atype == "assignment":
        title = extract_md_title(content, f"Assignment — {topic}")
        desc = extract_md_description(content) or f"Hands-on assignment for {topic}"
        return {
            "asset_type": "assignment",
            "title": title,
            "description": desc[:500],
            "tags": mod_tags + ["assignment", "hands-on"],
            "status": "published",
            "instructions": content,
            "due_in_days": 7,
        }

    elif atype == "quiz":
        data = json.loads(content)
        questions = data.get("questions", [])
        title = data.get("title") or f"Quiz — {topic}"
        desc = data.get("description") or f"Assessment quiz with {len(questions)} questions on {topic}"
        tags = data.get("tags", mod_tags + ["quiz", "assessment"])
        return {
            "asset_type": "quiz",
            "title": title,
            "description": desc[:500],
            "tags": tags,
            "status": "published",
            "questions": questions,
            "pass_mark_percent": data.get("pass_mark_percent", 60),
        }

    elif atype == "lab":
        data = json.loads(content)
        title = data.get("title") or f"Lab — {topic}"
        desc = data.get("description") or f"Hands-on lab exercise for {topic}"
        tags = data.get("tags", mod_tags + ["lab", "practical"])
        return {
            "asset_type": "lab",
            "title": title,
            "description": desc[:500],
            "tags": tags,
            "status": "published",
            "objective": data.get("objective", "Complete the lab exercise"),
            "steps": data.get("steps", []),
            "starter_code": data.get("starter_code"),
            "expected_output": data.get("expected_output"),
        }

    return None

def build_html_asset_payload(filepath: Path, media_file_id: int, meta: dict):
    topic = meta["title"].split(" - ", 1)[1] if " - " in meta["title"] else meta["title"]
    title = filename_to_title(filepath.name)
    try:
        html = filepath.read_text(encoding='utf-8-sig')
        m = re.search(r'<title>(.+?)</title>', html, re.IGNORECASE)
        if m and len(m.group(1).strip()) > 3:
            title = m.group(1).strip()
    except Exception:
        pass

    desc = f"Interactive {title} exercise for {topic}"
    return {
        "asset_type": "html_bundle",
        "title": title,
        "description": desc[:500],
        "tags": meta["tags"] + ["interactive", "hands-on"],
        "status": "published",
        "media_file_id": media_file_id,
    }


# ═══════════════════════════════════════════════════════════════════════════════

def seed():
    print("=" * 60)
    print("Seeding Python Full Stack Gen AI via API")
    print("=" * 60)

    for module_dir in sorted(ASSETS_DIR.glob("module-*")):
        if not module_dir.is_dir():
            continue
        slug = module_dir.name
        meta = foldername_to_meta(slug)
        
        print(f"\n{'─' * 50}")
        print(f"Module: {meta['title']}")
        print(f"{'─' * 50}")

        mod_payload = {
            "title": meta["title"],
            "slug": slug,
            "description": meta["description"],
            "display_order": meta["display_order"],
            "status": "published",
        }
        r = api_post_json(f"/training/programs/{PROGRAM_ID}/modules", mod_payload)
        if r.status_code == 201:
            module_id = r.json()["id"]
            print(f"  Created module id={module_id}")
        elif r.status_code == 409:
            print(f"  Module already exists, fetching...")
            r2 = api_get(f"/training/programs/{PROGRAM_ID}/modules")
            if r2.status_code == 200:
                mods = r2.json()
                match = [m for m in mods if m["slug"] == slug]
                if match:
                    module_id = match[0]["id"]
                    api_put_json(f"/training/modules/{module_id}", mod_payload)
                    print(f"  Updated module id={module_id}")
                else:
                    print(f"  ERROR: Could not find module by slug after 409")
                    continue
            else:
                print(f"  ERROR: Could not list modules: {r2.status_code}")
                continue
        else:
            print(f"  ERROR creating module: {r.status_code} {r.text[:300]}")
            continue

        # Get existing assets for this module to avoid duplicates
        r = api_get(f"/training/modules/{module_id}")
        existing_assets = []
        if r.status_code == 200:
             # Match existing assets by title or something? Actually, if we just want to avoid duplicates, 
             # the easiest is to just check if the module already has assets attached.
             mod_data = r.json()
             existing_assets = mod_data.get('assets', [])
        
        # Load AI semantic metadata if it exists
        meta_json_path = module_dir / "metadata.json"
        ai_metadata = {}
        if meta_json_path.exists():
            try:
                ai_metadata = json.loads(meta_json_path.read_text(encoding='utf-8-sig'))
                print(f"  Loaded semantic AI metadata for {len(ai_metadata)} files")
            except Exception as e:
                print(f"  Warning: could not parse metadata.json: {e}")
                
        files = [f for f in module_dir.iterdir() if f.is_file() and not f.name.startswith('.') and f.name != 'metadata.json']
        files.sort(key=lambda f: get_file_sort_key(f.name))

        display_order = 1
        for filepath in files:
            classification = classify_file(filepath)
            if classification is None:
                continue

            atype = classification["asset_type"]
            needs_upload = classification.get("needs_upload", False)

            if needs_upload:
                media_file_id = api_upload_file(filepath, atype)
                if media_file_id is None:
                    continue
                payload = build_html_asset_payload(filepath, media_file_id, meta)
            else:
                payload = build_asset_payload(filepath, meta, classification)
                if payload is None:
                    continue

            # Override with AI metadata if available
            if filepath.name in ai_metadata:
                ai_meta = ai_metadata[filepath.name]
                payload["title"] = ai_meta.get("title", payload.get("title"))
                payload["description"] = ai_meta.get("description", payload.get("description"))[:500]
                payload["tags"] = ai_meta.get("tags", payload.get("tags"))

            # Check if an asset with this title already exists in the module
            # to prevent duplicates on rerun.
            is_dup = False
            for ea in existing_assets:
                 if ea.get("asset", {}).get("title") == payload["title"]:
                      is_dup = True
                      break
            
            if is_dup:
                 print(f"  [{display_order:2d}] {atype:14s} → {payload['title']} (ALREADY EXISTS)")
                 display_order += 1
                 continue

            r = api_post_json("/training/assets", payload)
            if r.status_code == 201:
                asset_id = r.json()["id"]
                asset_title = r.json().get("title", "?")
                print(f"  [{display_order:2d}] {atype:14s} → {asset_title}")
            else:
                print(f"    ASSET CREATE ERROR for {filepath.name}: {r.status_code} {r.text[:300]}")
                continue

            attach_payload = {
                "asset_id": asset_id,
                "display_order": display_order,
                "is_required": True,
            }
            r = api_post_json(f"/training/modules/{module_id}/assets", attach_payload)
            if r.status_code not in (201, 409):
                print(f"    ATTACH ERROR: {r.status_code} {r.text[:200]}")

            display_order += 1

        print(f"  ✓ Processed assets for {meta['title']}")

    print("\n" + "=" * 60)
    print("SEEDING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    if not TOKEN:
        print("ERROR: Set SEED_TOKEN environment variable")
        sys.exit(1)

    r = api_get(f"/training/programs/{PROGRAM_ID}")
    if r.status_code == 401:
        print("ERROR: Token is expired or invalid. Please provide a fresh token.")
        sys.exit(1)
    if r.status_code != 200:
        print(f"ERROR: Could not reach API: {r.status_code} {r.text[:200]}")
        sys.exit(1)
    print(f"✓ Authenticated. Program: {r.json()['title']}\n")

    seed()
