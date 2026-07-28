# Web Scraping & Automation with Python

**Module 11 — Python Libraries | Topic 2**

---

## What is Web Scraping?

**Web scraping** = automatically extracting data from websites.

| Use Case | Example |
|----------|---------|
| Price comparison | Scrape product prices from multiple sites |
| News collection | Gather headlines from news websites |
| Data research | Collect public data for analysis |
| Job listings | Extract job postings |

> **Important:** Always check a website's `robots.txt` and Terms of Service before scraping. Don't scrape personal data or overwhelm servers.

---

## BeautifulSoup — HTML Parsing

```bash
pip install beautifulsoup4 requests
```

```python
import requests
from bs4 import BeautifulSoup

# Fetch a webpage
url = "https://quotes.toscrape.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find elements
title = soup.find("title").text
print(f"Page title: {title}")

# Find all quotes
quotes = soup.find_all("div", class_="quote")
for quote in quotes[:5]:
    text = quote.find("span", class_="text").text
    author = quote.find("small", class_="author").text
    print(f'"{text}" — {author}')
```

### Common BeautifulSoup Methods

| Method | What It Does |
|--------|-------------|
| `soup.find("tag")` | First matching element |
| `soup.find_all("tag")` | All matching elements |
| `soup.find("div", class_="name")` | By class name |
| `soup.find("div", id="main")` | By ID |
| `element.text` | Get text content |
| `element["href"]` | Get attribute value |
| `soup.select(".class > a")` | CSS selector |

---

## Python Automation Ideas

### 1. File Organizer

```python
import os
import shutil

def organize_downloads(folder):
    file_types = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
        "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx"],
        "Videos": [".mp4", ".avi", ".mkv", ".mov"],
        "Music": [".mp3", ".wav", ".flac"],
        "Code": [".py", ".js", ".html", ".css", ".json"],
        "Archives": [".zip", ".rar", ".7z", ".tar"]
    }

    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath):
            ext = os.path.splitext(filename)[1].lower()
            for category, extensions in file_types.items():
                if ext in extensions:
                    dest_folder = os.path.join(folder, category)
                    os.makedirs(dest_folder, exist_ok=True)
                    shutil.move(filepath, os.path.join(dest_folder, filename))
                    print(f"Moved {filename} → {category}/")
                    break

# organize_downloads("C:/Users/YourName/Downloads")
```

### 2. CSV Data Processor

```python
import csv

def process_student_csv(input_file, output_file):
    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        students = list(reader)

    for student in students:
        marks = [int(student[f"sub{i}"]) for i in range(1, 6)]
        student["total"] = sum(marks)
        student["average"] = f"{sum(marks)/len(marks):.1f}"
        avg = float(student["average"])
        student["grade"] = "A" if avg >= 90 else "B" if avg >= 75 else "C" if avg >= 60 else "F"

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=students[0].keys())
        writer.writeheader()
        writer.writerows(students)

    print(f"Processed {len(students)} students → {output_file}")
```

### 3. JSON API Data Collector

```python
import requests
import json

def fetch_github_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    repos = response.json()

    print(f"\n{username}'s repositories ({len(repos)} total):\n")
    for repo in sorted(repos, key=lambda r: r["stargazers_count"], reverse=True)[:10]:
        print(f"  {repo['name']:<30} Stars: {repo['stargazers_count']}")

    with open(f"{username}_repos.json", "w") as f:
        json.dump(repos, f, indent=2)
    print(f"\nSaved to {username}_repos.json")

# fetch_github_repos("python")
```

---

## Working with JSON

```python
import json

# Python dict to JSON string
data = {"name": "Rahul", "age": 20, "courses": ["Python", "Web"]}
json_string = json.dumps(data, indent=2)
print(json_string)

# JSON string to Python dict
parsed = json.loads(json_string)
print(parsed["name"])

# Read JSON file
with open("data.json", "r") as f:
    data = json.load(f)

# Write JSON file
with open("output.json", "w") as f:
    json.dump(data, f, indent=2)
```

---

## Working with CSV

```python
import csv

# Read CSV
with open("students.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["marks"])

# Write CSV
data = [
    {"name": "Rahul", "marks": 85},
    {"name": "Priya", "marks": 92}
]
with open("output.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "marks"])
    writer.writeheader()
    writer.writerows(data)
```

> **Pandas is easier for CSV:** `pd.read_csv()` and `df.to_csv()` are simpler than the csv module.

---

## Virtual Environments

Keep project dependencies isolated:

```bash
# Create virtual environment
python -m venv myenv

# Activate (Windows)
myenv\Scripts\activate

# Activate (Mac/Linux)
source myenv/bin/activate

# Install packages
pip install pandas requests

# Save dependencies
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt

# Deactivate
deactivate
```

---

## Summary

- **BeautifulSoup** scrapes data from web pages
- Always respect `robots.txt` and website terms when scraping
- **Automate** repetitive tasks: file organization, data processing, API calls
- **JSON** and **CSV** are the most common data formats
- Use **virtual environments** to manage project dependencies
- `pip install` to add libraries, `pip freeze` to save them
