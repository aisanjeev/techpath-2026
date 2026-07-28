import json
import os
import re
from pathlib import Path

ASSETS_DIR = Path(r"D:\project\techpath\techpath-2026\syllabus\ccc\assests")

def extract_md_title(content: str, default: str) -> str:
    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return m.group(1).strip() if m else default

def extract_md_description(content: str, max_len: int = 450) -> str:
    text = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    text = re.sub(r'^#[^\n]*\n', '', text, count=1).strip()
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    
    paragraphs = []
    in_code_block = False
    for line in text.split('\n'):
        line_stripped = line.strip()
        if line_stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block or not line_stripped or line_stripped.startswith('#') or line_stripped.startswith('|'):
            continue
        clean_line = re.sub(r'\*\*(.*?)\*\*', r'\1', line_stripped)
        clean_line = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', clean_line)
        clean_line = re.sub(r'`(.*?)`', r'\1', clean_line)
        paragraphs.append(clean_line)
        if len(' '.join(paragraphs)) > max_len + 100:
            break
            
    if paragraphs:
        desc = ' '.join(paragraphs).replace('\r', '').strip()
        if len(desc) > max_len:
            desc = desc[:max_len].rsplit(' ', 1)[0] + '...'
        return desc
    return ""

def filename_to_title(name: str) -> str:
    stem = Path(name).stem
    stem = re.sub(r'^\d+-', '', stem)
    return stem.replace('-', ' ').replace('_', ' ').title()

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
            "tags": [topic.lower().replace(' ', '-'), "ccc", "computer-concepts"]
        }
    return {
        "title": filename_to_title(name),
        "description": f"Learning materials for {filename_to_title(name)}",
        "display_order": 99,
        "tags": ["ccc"]
    }

def classify_file(filepath: Path) -> dict | None:
    name = filepath.name.lower()
    ext = filepath.suffix.lower()

    if ext == '.html': return {"asset_type": "html_bundle", "needs_upload": True}
    if name.startswith('assignment-') and ext == '.md': return {"asset_type": "assignment"}
    if name.startswith('cheatsheet-') and ext == '.md': return {"asset_type": "cheat_sheet"}
    if name.startswith('lab-') and ext == '.json': return {"asset_type": "lab"}
    if name.startswith('quiz-') and ext == '.json': return {"asset_type": "quiz"}
    if name.startswith('quiz-') and ext == '.md': return {"asset_type": "markdown"}
    if name.startswith('notes-') and ext == '.md': return {"asset_type": "notes"}
    if name.startswith('resources-') and ext == '.md': return {"asset_type": "notes"}
    if name.startswith('code-') or ext in ['.py', '.sql', '.js', '.css', '.html', '.yml', '.yaml', '.sh', '.dockerfile']:
        lang_map = {'.py': 'python', '.sql': 'sql', '.css': 'css', '.yml': 'yaml', '.js': 'javascript', '.sh': 'bash', '.html': 'html'}
        lang = lang_map.get(ext, 'text')
        return {"asset_type": "code_snippet", "language": lang}
    if ext == '.md': return {"asset_type": "markdown"}
    return None

def main():
    for module_dir in sorted(ASSETS_DIR.glob("module-*")):
        if not module_dir.is_dir():
            continue
        
        meta = foldername_to_meta(module_dir.name)
        topic = meta["title"].split(" - ", 1)[1] if " - " in meta["title"] else meta["title"]
        
        module_metadata = {}
        for filepath in module_dir.iterdir():
            if not filepath.is_file() or filepath.name.startswith('.') or filepath.name == 'metadata.json':
                continue
                
            cls = classify_file(filepath)
            if not cls: continue
            
            try:
                content = filepath.read_text(encoding='utf-8-sig')
            except UnicodeDecodeError:
                content = filepath.read_text(encoding='latin-1')
                
            atype = cls["asset_type"]
            title = filename_to_title(filepath.name)
            desc = ""
            tags = meta["tags"].copy()
            
            if atype == "markdown" or atype == "notes" or atype == "assignment":
                title = extract_md_title(content, title)
                desc = extract_md_description(content)
            elif atype == "quiz" or atype == "lab":
                try:
                    data = json.loads(content)
                    title = data.get("title", title)
                    desc = data.get("description", "")
                    tags = data.get("tags", tags)
                except:
                    pass
            elif atype == "code_snippet":
                lang = cls.get("language", "text")
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
            elif atype == "html_bundle":
                m = re.search(r'<title>(.+?)</title>', content, re.IGNORECASE)
                if m and len(m.group(1).strip()) > 3:
                    title = m.group(1).strip()
                desc = f"Interactive {title} exercise for {topic}"
            
            if not desc:
                desc = f"Learning material for {title}"
                
            module_metadata[filepath.name] = {
                "title": title,
                "description": desc[:500],
                "asset_type": atype,
                "tags": tags
            }
            
        out_path = module_dir / "metadata.json"
        out_path.write_text(json.dumps(module_metadata, indent=2), encoding='utf-8')
        print(f"Written metadata.json for {module_dir.name} ({len(module_metadata)} files)")

if __name__ == "__main__":
    main()
