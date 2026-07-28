"""
TechPath Institute — Python Libraries: API Calls & Web Scraping
=================================================================
Covers requests, httpx (async), BeautifulSoup, and automation
with os/pathlib/shutil/logging.

Requirements:
    pip install requests httpx beautifulsoup4 lxml python-dotenv

Run this file:  python code-api-and-scraping.py
"""

import asyncio
import json
import logging
import os
import shutil
import time
from datetime import datetime
from pathlib import Path

# ──────────────────────────────────────────────
# 1. REQUESTS — HTTP API CALLS
# ──────────────────────────────────────────────

print("=" * 60)
print("1. REQUESTS — HTTP API CALLS")
print("=" * 60)

try:
    import requests

    # GET request — fetch users from a public API
    print("Fetching users from JSONPlaceholder API...")
    response = requests.get(
        "https://jsonplaceholder.typicode.com/users",
        timeout=10,
    )

    print(f"Status code: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type')}")

    if response.status_code == 200:
        users = response.json()
        print(f"Total users: {len(users)}")
        print("\nFirst 3 users:")
        for user in users[:3]:
            print(f"  {user['name']} — {user['email']} ({user['address']['city']})")

    # POST request — create a resource
    print("\nCreating a new post...")
    new_post = {
        "title": "Learning Python at TechPath Institute",
        "body": "Python is a great language for beginners and professionals alike.",
        "userId": 1,
    }

    post_response = requests.post(
        "https://jsonplaceholder.typicode.com/posts",
        json=new_post,
        headers={"Content-Type": "application/json"},
        timeout=10,
    )

    if post_response.status_code == 201:
        created = post_response.json()
        print(f"Created post with ID: {created.get('id')}")
        print(f"Title: {created.get('title')}")

    # GET with query parameters
    print("\nFetching posts by user 1...")
    filtered = requests.get(
        "https://jsonplaceholder.typicode.com/posts",
        params={"userId": 1, "_limit": 3},
        timeout=10,
    )
    posts = filtered.json()
    for post in posts:
        print(f"  Post {post['id']}: {post['title'][:50]}...")

except requests.exceptions.ConnectionError:
    print("Could not connect — you may be offline. Skipping API examples.")
except Exception as e:
    print(f"Request failed: {e}")


# ──────────────────────────────────────────────
# 2. ERROR HANDLING FOR API CALLS
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("2. ERROR HANDLING FOR API CALLS")
print("=" * 60)

try:
    import requests

    def safe_api_call(url, method="GET", **kwargs):
        """Make an API call with proper error handling."""
        try:
            kwargs.setdefault("timeout", 10)
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()  # Raises for 4xx/5xx
            return {"success": True, "data": response.json(), "status": response.status_code}
        except requests.exceptions.ConnectionError:
            return {"success": False, "error": "Cannot connect to server"}
        except requests.exceptions.Timeout:
            return {"success": False, "error": "Request timed out"}
        except requests.exceptions.HTTPError as e:
            return {"success": False, "error": f"HTTP {response.status_code}: {e}"}
        except requests.exceptions.JSONDecodeError:
            return {"success": False, "error": "Response is not valid JSON"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # Test with valid URL
    result = safe_api_call("https://jsonplaceholder.typicode.com/users/1")
    if result["success"]:
        print(f"User: {result['data']['name']}")
    else:
        print(f"Error: {result['error']}")

    # Test with invalid URL (404)
    result = safe_api_call("https://jsonplaceholder.typicode.com/users/999")
    if result["success"]:
        print(f"User: {result['data']}")
    else:
        print(f"Error: {result['error']}")

except ImportError:
    print("requests not installed — run: pip install requests")


# ──────────────────────────────────────────────
# 3. ASYNC HTTP WITH httpx
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("3. ASYNC HTTP WITH httpx")
print("=" * 60)

try:
    import httpx

    async def fetch_user(client, user_id):
        """Fetch a single user asynchronously."""
        response = await client.get(
            f"https://jsonplaceholder.typicode.com/users/{user_id}",
            timeout=10,
        )
        return response.json()

    async def fetch_multiple_users():
        """Fetch multiple users concurrently."""
        async with httpx.AsyncClient() as client:
            # Sequential (slow)
            start = time.perf_counter()
            sequential_results = []
            for uid in range(1, 4):
                user = await fetch_user(client, uid)
                sequential_results.append(user)
            seq_time = time.perf_counter() - start

            # Concurrent (fast)
            start = time.perf_counter()
            tasks = [fetch_user(client, uid) for uid in range(1, 4)]
            concurrent_results = await asyncio.gather(*tasks)
            conc_time = time.perf_counter() - start

            print(f"Sequential: {seq_time:.2f}s for {len(sequential_results)} users")
            print(f"Concurrent: {conc_time:.2f}s for {len(concurrent_results)} users")
            print(f"Speedup: {seq_time / conc_time:.1f}x faster")

            for user in concurrent_results:
                print(f"  {user['name']} — {user['email']}")

    asyncio.run(fetch_multiple_users())

except ImportError:
    print("httpx not installed — run: pip install httpx")
except Exception as e:
    print(f"Async fetch failed: {e}")


# ──────────────────────────────────────────────
# 4. WEB SCRAPING WITH BEAUTIFULSOUP
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("4. WEB SCRAPING WITH BEAUTIFULSOUP")
print("=" * 60)

try:
    from bs4 import BeautifulSoup

    # Parse a sample HTML string (no network needed)
    sample_html = """
    <html>
    <head><title>TechPath Institute — Courses</title></head>
    <body>
        <h1>Our Courses</h1>
        <table id="courses">
            <tr><th>Course</th><th>Duration</th><th>Fee</th></tr>
            <tr><td>Python Full Stack</td><td>6 months</td><td>₹25,000</td></tr>
            <tr><td>Web Development</td><td>4 months</td><td>₹20,000</td></tr>
            <tr><td>Data Science</td><td>8 months</td><td>₹30,000</td></tr>
            <tr><td>Digital Marketing</td><td>3 months</td><td>₹15,000</td></tr>
        </table>
        <div class="contact">
            <p>Email: <a href="mailto:info@techpath.biz">info@techpath.biz</a></p>
            <p>Phone: <a href="tel:0755-2556789">0755-2556789</a></p>
        </div>
        <ul class="cities">
            <li>Bhopal</li>
            <li>Delhi</li>
            <li>Pune</li>
            <li>Mumbai</li>
        </ul>
    </body>
    </html>
    """

    soup = BeautifulSoup(sample_html, "html.parser")

    # Extract title
    title = soup.find("title").text
    print(f"Page title: {title}")

    # Extract table data
    table = soup.find("table", id="courses")
    rows = table.find_all("tr")
    headers = [th.text for th in rows[0].find_all("th")]

    print(f"\nCourses ({len(rows) - 1} found):")
    courses = []
    for row in rows[1:]:
        cells = [td.text for td in row.find_all("td")]
        course = dict(zip(headers, cells))
        courses.append(course)
        print(f"  {course['Course']:25s} {course['Duration']:10s} {course['Fee']}")

    # Extract links
    print("\nLinks found:")
    for link in soup.find_all("a"):
        print(f"  {link.text} → {link.get('href')}")

    # Extract list items
    cities = [li.text for li in soup.select("ul.cities li")]
    print(f"\nCities: {cities}")

    # CSS selectors
    contact_links = soup.select("div.contact a")
    print(f"Contact links: {[a.text for a in contact_links]}")

except ImportError:
    print("beautifulsoup4 not installed — run: pip install beautifulsoup4")

# Live scraping example (commented out to avoid network dependency)
# To try this yourself, uncomment and run:
"""
try:
    response = requests.get("https://quotes.toscrape.com/", timeout=10)
    soup = BeautifulSoup(response.text, "lxml")

    quotes = soup.find_all("div", class_="quote")
    for quote in quotes[:5]:
        text = quote.find("span", class_="text").text
        author = quote.find("small", class_="author").text
        tags = [tag.text for tag in quote.find_all("a", class_="tag")]
        print(f"  {author}: {text[:60]}... [tags: {', '.join(tags)}]")
except Exception as e:
    print(f"Scraping failed: {e}")
"""


# ──────────────────────────────────────────────
# 5. PATHLIB — MODERN FILE OPERATIONS
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("5. PATHLIB — MODERN FILE OPERATIONS")
print("=" * 60)

# Create a project structure
project_dir = Path("techpath_demo_project")
project_dir.mkdir(exist_ok=True)

# Create subdirectories
for subdir in ["data", "output", "logs"]:
    (project_dir / subdir).mkdir(exist_ok=True)

# Create sample files
(project_dir / "data" / "students.csv").write_text(
    "Name,City,Fee\nRahul,Bhopal,25000\nPriya,Pune,20000\n",
    encoding="utf-8",
)
(project_dir / "data" / "config.json").write_text(
    json.dumps({"institute": "TechPath", "debug": False}, indent=2),
    encoding="utf-8",
)
(project_dir / "README.md").write_text(
    "# TechPath Demo Project\nCreated for learning pathlib.\n",
    encoding="utf-8",
)

print(f"Project directory: {project_dir.resolve()}")

# List all files recursively
print("\nProject structure:")
for path in sorted(project_dir.rglob("*")):
    if path.is_file():
        relative = path.relative_to(project_dir)
        size = path.stat().st_size
        print(f"  {relative} ({size} bytes)")

# Read a file
config_path = project_dir / "data" / "config.json"
config = json.loads(config_path.read_text(encoding="utf-8"))
print(f"\nConfig: {config}")

# File info
csv_path = project_dir / "data" / "students.csv"
print(f"\nCSV file info:")
print(f"  Name: {csv_path.name}")
print(f"  Extension: {csv_path.suffix}")
print(f"  Parent: {csv_path.parent}")
print(f"  Exists: {csv_path.exists()}")

# Find files by pattern
print(f"\nAll .csv files: {[p.name for p in project_dir.rglob('*.csv')]}")
print(f"All .json files: {[p.name for p in project_dir.rglob('*.json')]}")


# ──────────────────────────────────────────────
# 6. LOGGING
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("6. LOGGING")
print("=" * 60)

# Configure logging
log_file = project_dir / "logs" / "app.log"
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(),
    ],
    force=True,  # Reset any existing config
)

logger = logging.getLogger("techpath")

logger.info("TechPath application started")
logger.info(f"Project directory: {project_dir.resolve()}")
logger.debug("Debug mode is enabled for this demo")
logger.warning("This is a demo — no real data is being processed")

# Simulate an operation with logging
def process_student(name, fee):
    logger.info(f"Processing student: {name}")
    if fee < 0:
        logger.error(f"Invalid fee for {name}: ₹{fee}")
        return False
    logger.info(f"Fee ₹{fee:,} recorded for {name}")
    return True

process_student("Rahul", 25000)
process_student("Priya", -500)
process_student("Amit", 30000)

print(f"\nLog file saved to: {log_file}")
print(f"Log contents:")
print(log_file.read_text(encoding="utf-8"))


# ──────────────────────────────────────────────
# 7. SHUTIL — BULK FILE OPERATIONS
# ──────────────────────────────────────────────

print("=" * 60)
print("7. SHUTIL — BULK FILE OPERATIONS")
print("=" * 60)

# Copy a file
src = project_dir / "data" / "students.csv"
dst = project_dir / "output" / "students_backup.csv"
shutil.copy2(src, dst)
print(f"Copied {src.name} → {dst.name}")

# Get directory size
total_size = sum(f.stat().st_size for f in project_dir.rglob("*") if f.is_file())
print(f"Project size: {total_size} bytes")

# Get disk usage
total, used, free = shutil.disk_usage(".")
print(f"Disk usage: {used // (1024**3)} GB used, {free // (1024**3)} GB free")


# ──────────────────────────────────────────────
# 8. ENVIRONMENT VARIABLES
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("8. ENVIRONMENT VARIABLES")
print("=" * 60)

# Create a .env file
env_file = project_dir / ".env"
env_file.write_text(
    "API_KEY=demo-key-12345\nDEBUG=true\nINSTITUTE=TechPath Institute\n",
    encoding="utf-8",
)

# Read .env manually (python-dotenv does this automatically)
env_vars = {}
for line in env_file.read_text(encoding="utf-8").strip().split("\n"):
    if "=" in line and not line.startswith("#"):
        key, value = line.split("=", 1)
        env_vars[key.strip()] = value.strip()

print(f"Environment variables from .env:")
for key, value in env_vars.items():
    # Mask API keys
    display = value[:5] + "..." if "KEY" in key else value
    print(f"  {key} = {display}")

# With python-dotenv (if installed)
try:
    from dotenv import load_dotenv
    load_dotenv(env_file)
    print(f"\nLoaded with dotenv — INSTITUTE: {os.getenv('INSTITUTE', 'not set')}")
except ImportError:
    print("\npython-dotenv not installed — run: pip install python-dotenv")


# ──────────────────────────────────────────────
# CLEANUP
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("CLEANUP")
print("=" * 60)

# Remove the demo project directory
if project_dir.exists():
    shutil.rmtree(project_dir)
    print(f"Removed {project_dir}")

print("\n" + "=" * 60)
print("Program complete! You have mastered APIs & Automation.")
print("=" * 60)
