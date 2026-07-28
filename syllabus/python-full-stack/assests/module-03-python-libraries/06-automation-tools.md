# Automation Tools

**Module 03 — Python Libraries: Data, Automation & APIs | Topic 6**

---

## Why Automate?

Many tasks in a developer's day are repetitive — organizing files, renaming images, processing data, sending reminders. Python can automate all of them.

**Common automation tasks:**
- Organize files by type or date
- Process CSV/Excel files in bulk
- Schedule tasks to run automatically
- Read environment variables for configuration
- Set up logging for your applications

---

## os Module — Operating System Interface

```python
import os

# Current directory
print(os.getcwd())    # C:\Users\Rahul\project

# List files
print(os.listdir("."))    # ['app.py', 'data', 'venv']

# Check existence
print(os.path.exists("data/students.csv"))    # True/False
print(os.path.isfile("app.py"))               # True
print(os.path.isdir("data"))                  # True

# Create directory
os.makedirs("output/reports", exist_ok=True)

# Environment variables
print(os.environ.get("HOME"))
print(os.environ.get("DATABASE_URL", "sqlite:///default.db"))

# File info
size = os.path.getsize("app.py")    # Size in bytes
print(f"File size: {size / 1024:.1f} KB")

# Join paths (cross-platform)
path = os.path.join("data", "students", "marks.csv")
print(path)    # data/students/marks.csv (or data\students\marks.csv on Windows)
```

---

## pathlib — Modern Path Handling

`pathlib` is the modern, object-oriented way to handle paths. It is preferred over `os.path`.

```python
from pathlib import Path

# Create path objects
project = Path(".")
data_dir = Path("data")
csv_file = data_dir / "students.csv"    # Use / operator!

# Check existence
print(csv_file.exists())      # True/False
print(csv_file.is_file())     # True
print(data_dir.is_dir())      # True

# File properties
print(csv_file.name)          # students.csv
print(csv_file.stem)          # students
print(csv_file.suffix)        # .csv
print(csv_file.parent)        # data
print(csv_file.absolute())    # Full path

# List files
for f in Path(".").iterdir():
    print(f"{'DIR' if f.is_dir() else 'FILE'}: {f.name}")

# Find files by pattern
for py_file in Path(".").glob("**/*.py"):    # Recursive!
    print(py_file)

# Read and write
content = csv_file.read_text(encoding="utf-8")
Path("output.txt").write_text("Hello!", encoding="utf-8")

# Create directories
Path("output/reports").mkdir(parents=True, exist_ok=True)
```

---

## shutil — File Operations

`shutil` handles copying, moving, and deleting files and directories.

```python
import shutil

# Copy a file
shutil.copy("data/students.csv", "backup/students_backup.csv")

# Copy entire directory
shutil.copytree("data", "data_backup")

# Move/rename a file
shutil.move("old_name.txt", "new_name.txt")

# Delete a directory (including contents!)
shutil.rmtree("temp_data")    # Be careful!

# Get disk usage
total, used, free = shutil.disk_usage("/")
print(f"Free space: {free / (1024**3):.1f} GB")
```

### Practical: Organize Files by Extension

```python
from pathlib import Path
import shutil

def organize_downloads(folder):
    """Sort files into folders by extension."""
    categories = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov"],
        "Code": [".py", ".js", ".html", ".css", ".json"],
        "Archives": [".zip", ".rar", ".tar", ".gz"],
    }
    
    folder = Path(folder)
    for file in folder.iterdir():
        if file.is_dir():
            continue
        
        ext = file.suffix.lower()
        target = "Others"
        for category, extensions in categories.items():
            if ext in extensions:
                target = category
                break
        
        target_dir = folder / target
        target_dir.mkdir(exist_ok=True)
        shutil.move(str(file), str(target_dir / file.name))
        print(f"Moved {file.name} → {target}/")

organize_downloads("C:/Users/Rahul/Downloads")
```

---

## schedule — Task Scheduling

```bash
pip install schedule
```

```python
import schedule
import time
from datetime import datetime

def morning_report():
    """Generate daily report."""
    print(f"[{datetime.now().strftime('%H:%M')}] Generating morning report...")

def check_attendance():
    """Check student attendance."""
    print(f"[{datetime.now().strftime('%H:%M')}] Checking attendance...")

def weekly_backup():
    """Backup data weekly."""
    print(f"[{datetime.now().strftime('%H:%M')}] Running weekly backup...")

# Schedule tasks
schedule.every().day.at("09:00").do(morning_report)
schedule.every(30).minutes.do(check_attendance)
schedule.every().monday.at("06:00").do(weekly_backup)
schedule.every(2).hours.do(lambda: print("Heartbeat check..."))

print("Scheduler running... Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(1)
```

---

## python-dotenv — Environment Variables

Environment variables keep sensitive data (API keys, passwords) out of your code.

```bash
pip install python-dotenv
```

### .env File

```
# .env
DATABASE_URL=sqlite:///data/techpath.db
SECRET_KEY=my-super-secret-key-2026
API_KEY=sk-abc123def456
DEBUG=true
INSTITUTE_NAME=TechPath Institute
```

### Loading .env in Python

```python
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Access them
db_url = os.getenv("DATABASE_URL")
secret = os.getenv("SECRET_KEY")
debug = os.getenv("DEBUG", "false").lower() == "true"
institute = os.getenv("INSTITUTE_NAME", "Default Institute")

print(f"Database: {db_url}")
print(f"Debug mode: {debug}")
print(f"Institute: {institute}")
```

**Important:** Add `.env` to `.gitignore` so it is never uploaded to GitHub!

```
# .gitignore
.env
.env.local
```

---

## logging — Professional Logging

Print statements are for debugging. Logging is for production.

```python
import logging

# Basic setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("TechPath")

# Log levels (from least to most severe)
logger.debug("Detailed info for debugging")        # Not shown by default
logger.info("Student Rahul enrolled successfully")
logger.warning("Disk space is running low")
logger.error("Failed to connect to database")
logger.critical("Application crashed!")
```

### Logging to File

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler(),    # Also print to console
    ],
)

logger = logging.getLogger("TechPath")
logger.info("Application started")
logger.error("Database connection failed")
```

### Log Levels

| Level | Value | Use When |
|-------|-------|----------|
| DEBUG | 10 | Detailed debugging info |
| INFO | 20 | Normal operations |
| WARNING | 30 | Something unexpected but not critical |
| ERROR | 40 | Something failed |
| CRITICAL | 50 | Application is crashing |

---

## Practical: Bulk File Renamer

```python
from pathlib import Path

def rename_photos(folder, prefix="IMG"):
    """Rename all photos in a folder with sequential numbers."""
    folder = Path(folder)
    image_extensions = {".jpg", ".jpeg", ".png", ".gif"}
    
    photos = sorted([
        f for f in folder.iterdir()
        if f.suffix.lower() in image_extensions
    ])
    
    for i, photo in enumerate(photos, start=1):
        new_name = f"{prefix}_{i:04d}{photo.suffix.lower()}"
        new_path = folder / new_name
        photo.rename(new_path)
        print(f"Renamed: {photo.name} → {new_name}")
    
    print(f"\nRenamed {len(photos)} files.")

rename_photos("C:/Users/Rahul/Photos")
```

---

## Practical: CSV Batch Processor

```python
from pathlib import Path
import csv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("BatchProcessor")

def process_csv_files(input_dir, output_dir):
    """Process all CSV files: filter passing students and save."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    for csv_file in input_path.glob("*.csv"):
        logger.info(f"Processing {csv_file.name}...")
        
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            passing = [row for row in reader if int(row.get("marks", 0)) >= 60]
        
        out_file = output_path / f"passing_{csv_file.name}"
        with open(out_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=passing[0].keys() if passing else [])
            writer.writeheader()
            writer.writerows(passing)
        
        logger.info(f"  → {len(passing)} passing students saved to {out_file.name}")

process_csv_files("data/batches", "data/results")
```

---

## Summary

| Tool | Purpose | Key Functions |
|------|---------|---------------|
| `os` | OS operations | `getcwd()`, `listdir()`, `environ` |
| `pathlib.Path` | File paths | `/` operator, `glob()`, `read_text()` |
| `shutil` | Copy/move/delete | `copy()`, `move()`, `rmtree()` |
| `schedule` | Task scheduling | `every().day.at("09:00")` |
| `dotenv` | Environment vars | `load_dotenv()`, `os.getenv()` |
| `logging` | Professional logs | `logger.info()`, `logger.error()` |

---

## Practice Tasks

1. Write a script that organizes a downloads folder by file type
2. Create a `.env` file with API keys and load them in Python
3. Set up a logger that writes to both console and a file
4. Build a file renamer that adds date prefixes to all files in a folder
5. Schedule a task that runs every 5 minutes and logs a message
