#!/usr/bin/env python3
"""Seed training modules for Course on Computer Concepts (CCC) via the production API.

Idempotent: safe to run multiple times.
"""

import json
import os
import re
import sys
import time
from pathlib import Path
import httpx

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

API_BASE = "https://api.techpath.biz/api/v1"
TOKEN = os.environ.get("SEED_TOKEN", "").strip()
PROGRAM_ID = 3
ASSETS_DIR = Path(r"D:\project\techpath\techpath-2026\syllabus\ccc\assests")
DELAY = 0.15

client = httpx.Client(
    base_url=API_BASE,
    headers={"Authorization": f"Bearer {TOKEN}"},
    timeout=60,
)

def api_get(path):
    time.sleep(DELAY)
    return client.get(path)

def api_post_json(path, payload):
    time.sleep(DELAY)
    return client.post(path, json=payload)

def api_put_json(path, payload):
    time.sleep(DELAY)
    return client.put(path, json=payload)

def api_upload_file(filepath: Path, asset_type: str):
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

def foldername_to_meta(name: str) -> dict:
    m = re.match(r'^module-(\d+)-(.+)$', name)
    if m:
        num = int(m.group(1))
        topic = m.group(2).replace('-', ' ').title()
        topic = topic.replace('Uiux', 'UI/UX').replace('Ai', 'AI').replace('Seo', 'SEO').replace('Crm', 'CRM')
        return {
            "title": f"Module {num:02d} - {topic}",
            "description": f"Comprehensive learning materials for {topic}.",
            "display_order": num,
        }
    return {
        "title": name.title().replace('-', ' '),
        "description": f"Learning materials for {name}",
        "display_order": 99,
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

def build_payload(filepath: Path, ai_meta: dict):
    try:
        content = filepath.read_text(encoding='utf-8-sig')
    except UnicodeDecodeError:
        content = filepath.read_text(encoding='latin-1')

    # Convert unsupported asset_type 'lab' to 'markdown' payload format as a fallback
    # Because backend API rejects 'lab' for InlineTextAssetIn
    atype = ai_meta["asset_type"]
    if atype == "lab":
        atype = "markdown"

    payload = {
        "asset_type": atype,
        "title": ai_meta["title"],
        "description": ai_meta.get("description", "")[:500],
        "tags": ai_meta.get("tags", []),
        "status": "published",
    }
    
    if atype in ["markdown", "notes", "cheat_sheet", "code_snippet"]:
        payload["body"] = content
        if atype == "code_snippet":
            ext = filepath.suffix.lower()
            lang = 'text'
            if ext == '.html': lang = 'html'
            elif ext == '.js': lang = 'javascript'
            elif ext == '.css': lang = 'css'
            elif ext == '.py': lang = 'python'
            payload["language"] = lang
    elif atype == "assignment":
        payload["instructions"] = content
        payload["due_in_days"] = 7
    elif atype == "quiz":
        try:
            data = json.loads(content)
            payload["questions"] = data.get("questions", [])
            payload["pass_mark_percent"] = data.get("pass_mark_percent", 60)
        except:
            payload["questions"] = []

    return payload

def seed():
    print("=" * 60)
    print("Seeding CCC via API (using metadata.json exclusively)")
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

        r = api_get(f"/training/modules/{module_id}")
        existing_assets = []
        if r.status_code == 200:
             existing_assets = r.json().get('assets', [])
        
        meta_json_path = module_dir / "metadata.json"
        if not meta_json_path.exists():
            print(f"  Skipping {slug}: no metadata.json found.")
            continue
            
        ai_metadata = json.loads(meta_json_path.read_text(encoding='utf-8-sig'))
        print(f"  Loaded metadata.json for {len(ai_metadata)} files")

        files = [f for f in module_dir.iterdir() if f.is_file() and not f.name.startswith('.') and f.name != 'metadata.json']
        files.sort(key=lambda f: get_file_sort_key(f.name))

        display_order = 1
        for filepath in files:
            if filepath.name not in ai_metadata:
                print(f"  Warning: {filepath.name} missing from metadata.json, skipping.")
                continue

            ai_meta = ai_metadata[filepath.name]
            payload = build_payload(filepath, ai_meta)
            atype = payload["asset_type"]

            if atype == "html_bundle":
                media_file_id = api_upload_file(filepath, atype)
                if media_file_id is None:
                    continue
                payload["media_file_id"] = media_file_id

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
                print(f"  [{display_order:2d}] {atype:14s} → {payload['title']}")
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
