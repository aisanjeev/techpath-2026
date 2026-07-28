# Module 03: Python Libraries — Data, Automation & APIs

## 1. NumPy — Numerical Computing

### What is NumPy?
NumPy (Numerical Python) is the foundation library for data science in Python. It provides fast array operations.

```bash
pip install numpy
```

### Arrays
```python
import numpy as np

# Creating arrays
marks = np.array([85, 92, 78, 88, 95])
print(marks)           # [85 92 78 88 95]
print(type(marks))     # <class 'numpy.ndarray'>
print(marks.dtype)     # int64

# 2D array (matrix)
student_marks = np.array([
    [85, 92, 78],   # Rahul
    [90, 88, 95],   # Priya
    [72, 68, 75],   # Amit
])
print(student_marks.shape)  # (3, 3) — 3 students, 3 subjects
```

### Vectorized Operations
NumPy operations work on the entire array at once — no loops needed:
```python
marks = np.array([85, 92, 78, 88, 95])

# Operations on entire array
print(marks + 5)        # [90 97 83 93 100] — add 5 to all
print(marks * 1.1)      # Scale by 1.1
print(marks > 80)       # [True True False True True]

# Statistics
print(f"Mean: {marks.mean():.1f}")
print(f"Std Dev: {marks.std():.1f}")
print(f"Max: {marks.max()}, Min: {marks.min()}")
print(f"Sum: {marks.sum()}")
```

### Broadcasting
NumPy automatically handles operations between arrays of different shapes:
```python
# Student marks in 3 subjects, scale each subject differently
marks = np.array([[85, 92, 78], [90, 88, 95]])
weights = np.array([0.3, 0.3, 0.4])  # Subject weights

weighted = marks * weights  # Broadcasting!
print(weighted.sum(axis=1))  # Weighted total per student
```

### Random Module
```python
# Random numbers
np.random.seed(42)  # For reproducibility
random_marks = np.random.randint(40, 100, size=10)
print(f"Random marks: {random_marks}")

# Random choice
students = ["Rahul", "Priya", "Amit", "Sneha", "Vikram"]
selected = np.random.choice(students, size=3, replace=False)
print(f"Selected: {selected}")

# Normal distribution
heights = np.random.normal(loc=165, scale=10, size=100)  # Mean 165, SD 10
print(f"Heights — Mean: {heights.mean():.1f}, Std: {heights.std():.1f}")
```

### Useful Array Operations
```python
# Reshaping
a = np.arange(12)      # [0, 1, 2, ..., 11]
b = a.reshape(3, 4)    # 3x4 matrix

# Filtering
marks = np.array([85, 42, 92, 35, 78, 88])
passed = marks[marks >= 40]
print(f"Passed: {passed}")

# Sorting
print(f"Sorted: {np.sort(marks)}")

# Unique values
cities = np.array(["Bhopal", "Delhi", "Bhopal", "Pune", "Delhi"])
print(f"Unique: {np.unique(cities)}")
```

---

## 2. Pandas — Data Analysis

### What is Pandas?
Pandas provides DataFrames — spreadsheet-like tables in Python. It is the most important library for data analysis.

```bash
pip install pandas
```

### Creating DataFrames
```python
import pandas as pd

# From a dictionary
students = pd.DataFrame({
    "Name": ["Rahul", "Priya", "Amit", "Sneha", "Vikram"],
    "City": ["Bhopal", "Pune", "Delhi", "Mumbai", "Jaipur"],
    "Course": ["Python", "Python", "Data Science", "Web Dev", "Python"],
    "Fee": [25000, 25000, 30000, 20000, 25000],
    "Marks": [85, 92, 78, 88, 72],
})

print(students)
print(students.info())     # Column types and memory
print(students.describe()) # Statistical summary
```

### Reading Files
```python
# Read CSV
df = pd.read_csv("students.csv")

# Read Excel
df = pd.read_excel("students.xlsx")

# Read with options
df = pd.read_csv("data.csv", encoding="utf-8", na_values=["N/A", ""])
```

### Selecting & Filtering
```python
# Select columns
print(students["Name"])              # Single column (Series)
print(students[["Name", "City"]])    # Multiple columns (DataFrame)

# Filter rows
python_students = students[students["Course"] == "Python"]
high_scorers = students[students["Marks"] >= 85]
bhopal_python = students[(students["City"] == "Bhopal") & (students["Course"] == "Python")]

# loc (label-based) and iloc (index-based)
print(students.loc[0, "Name"])       # "Rahul"
print(students.iloc[0:3, 0:2])      # First 3 rows, first 2 columns
```

### Adding & Modifying Columns
```python
# New column
students["Fee_with_GST"] = students["Fee"] * 1.18
students["Grade"] = students["Marks"].apply(
    lambda m: "A" if m >= 85 else "B" if m >= 70 else "C"
)

# Rename columns
students = students.rename(columns={"Fee": "Base_Fee"})
```

### GroupBy — Split-Apply-Combine
```python
# Group by course
course_stats = students.groupby("Course").agg({
    "Name": "count",
    "Fee": ["sum", "mean"],
    "Marks": ["mean", "max"],
})
print(course_stats)

# Group by city, get average marks
city_avg = students.groupby("City")["Marks"].mean()
print(city_avg)
```

### Merge (Join) DataFrames
```python
# Student info
info = pd.DataFrame({
    "Name": ["Rahul", "Priya", "Amit"],
    "Email": ["rahul@mail.com", "priya@mail.com", "amit@mail.com"],
})

# Merge on Name
merged = pd.merge(students, info, on="Name", how="left")
print(merged)
```

### Pivot Tables
```python
pivot = students.pivot_table(
    values="Fee",
    index="City",
    columns="Course",
    aggfunc="sum",
    fill_value=0,
)
print(pivot)
```

### Saving Data
```python
students.to_csv("output.csv", index=False)
students.to_excel("output.xlsx", index=False)
students.to_json("output.json", orient="records", indent=2)
```

---

## 3. Matplotlib & Seaborn — Data Visualization

### Basic Matplotlib
```bash
pip install matplotlib seaborn
```

```python
import matplotlib.pyplot as plt

# Line chart
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
enrollments = [12, 18, 25, 30, 28, 35]

plt.figure(figsize=(8, 5))
plt.plot(months, enrollments, marker="o", color="blue", linewidth=2)
plt.title("TechPath Monthly Enrollments")
plt.xlabel("Month")
plt.ylabel("Students")
plt.grid(True, alpha=0.3)
plt.savefig("enrollments.png", dpi=150, bbox_inches="tight")
plt.show()
```

### Bar Chart
```python
courses = ["Python", "Web Dev", "Data Science", "ADCA"]
students = [45, 32, 28, 20]

plt.figure(figsize=(8, 5))
plt.bar(courses, students, color=["#2196F3", "#4CAF50", "#FF9800", "#9C27B0"])
plt.title("Course-wise Enrollment at TechPath")
plt.xlabel("Course")
plt.ylabel("Number of Students")
for i, v in enumerate(students):
    plt.text(i, v + 1, str(v), ha="center", fontweight="bold")
plt.tight_layout()
plt.show()
```

### Pie Chart
```python
labels = ["Bhopal", "Delhi", "Pune", "Mumbai", "Other"]
sizes = [35, 25, 20, 12, 8]

plt.figure(figsize=(7, 7))
plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90,
        colors=["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"])
plt.title("Students by City")
plt.show()
```

### Seaborn — Beautiful Statistical Plots
```python
import seaborn as sns

# Heatmap of correlations
data = pd.DataFrame({
    "Python": [85, 92, 78, 88, 72],
    "Web Dev": [80, 88, 72, 90, 68],
    "DBMS": [90, 85, 82, 78, 75],
})

plt.figure(figsize=(6, 5))
sns.heatmap(data.corr(), annot=True, cmap="YlOrRd", fmt=".2f")
plt.title("Subject Correlation")
plt.show()
```

---

## 4. Requests & httpx — Working with APIs

### GET Requests
```python
import requests

# Simple GET request
response = requests.get("https://jsonplaceholder.typicode.com/users")
print(f"Status: {response.status_code}")
users = response.json()

for user in users[:3]:
    print(f"  {user['name']} — {user['email']}")
```

### POST Requests
```python
# Create a new resource
new_student = {
    "name": "Rahul Sharma",
    "email": "rahul@techpath.biz",
    "city": "Bhopal",
}

response = requests.post(
    "https://jsonplaceholder.typicode.com/users",
    json=new_student,
    headers={"Content-Type": "application/json"},
)
print(f"Status: {response.status_code}")
print(f"Created: {response.json()}")
```

### Auth Headers
```python
# API with authentication
headers = {
    "Authorization": "Bearer your-api-token-here",
    "Content-Type": "application/json",
}

response = requests.get("https://api.example.com/data", headers=headers)
```

### httpx — Async HTTP
```python
import httpx
import asyncio

async def fetch_users():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/users")
        return response.json()

users = asyncio.run(fetch_users())
print(f"Fetched {len(users)} users")
```

### Error Handling
```python
try:
    response = requests.get("https://api.example.com/data", timeout=5)
    response.raise_for_status()  # Raise exception for 4xx/5xx
    data = response.json()
except requests.exceptions.ConnectionError:
    print("Could not connect to the server")
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.exceptions.JSONDecodeError:
    print("Response is not valid JSON")
```

---

## 5. Web Scraping — BeautifulSoup

### Parsing HTML
```bash
pip install beautifulsoup4 lxml
```

```python
from bs4 import BeautifulSoup
import requests

# Fetch a webpage
response = requests.get("https://quotes.toscrape.com/")
soup = BeautifulSoup(response.text, "lxml")

# Find elements
title = soup.find("title").text
print(f"Page title: {title}")

# Find all quotes
quotes = soup.find_all("div", class_="quote")
for quote in quotes[:5]:
    text = quote.find("span", class_="text").text
    author = quote.find("small", class_="author").text
    print(f"  {author}: {text[:60]}...")
```

### Common BeautifulSoup Methods

| Method | What it Does |
|--------|-------------|
| `soup.find("tag")` | First matching element |
| `soup.find_all("tag")` | All matching elements |
| `soup.select("css selector")` | CSS selector (like jQuery) |
| `element.text` | Text content |
| `element["href"]` | Get attribute |
| `element.find_parent()` | Parent element |

### Extracting Table Data
```python
# Parse an HTML table into a list of dictionaries
table = soup.find("table")
if table:
    headers = [th.text.strip() for th in table.find_all("th")]
    rows = []
    for tr in table.find_all("tr")[1:]:  # Skip header row
        cells = [td.text.strip() for td in tr.find_all("td")]
        rows.append(dict(zip(headers, cells)))
    print(rows)
```

---

## 6. Automation — os, pathlib, shutil

### pathlib — Modern File Paths
```python
from pathlib import Path

# Current directory
current = Path(".")
print(f"Current: {current.resolve()}")

# Create directories
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# List files
for f in Path(".").glob("*.py"):
    print(f"  Python file: {f.name} ({f.stat().st_size} bytes)")

# Read/write files
config_file = data_dir / "config.json"
config_file.write_text('{"debug": true}', encoding="utf-8")
print(config_file.read_text(encoding="utf-8"))
```

### shutil — File Operations
```python
import shutil

# Copy file
shutil.copy("source.txt", "destination.txt")

# Copy entire directory
shutil.copytree("src_folder", "backup_folder")

# Move/rename
shutil.move("old_name.txt", "new_name.txt")

# Delete directory
shutil.rmtree("temp_folder")

# Get disk usage
total, used, free = shutil.disk_usage("/")
print(f"Disk: {free // (1024**3)} GB free")
```

### os & Environment Variables
```python
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Access environment variables
api_key = os.getenv("API_KEY", "default-key")
debug = os.getenv("DEBUG", "false").lower() == "true"
```

### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger(__name__)

logger.info("Application started")
logger.warning("Low memory")
logger.error("Failed to connect to database")
```

### Scheduling Tasks
```python
# pip install schedule
import schedule
import time

def check_enrollments():
    print("Checking new enrollments...")

schedule.every(10).minutes.do(check_enrollments)
schedule.every().day.at("09:00").do(check_enrollments)

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
```

---

## 7. AI API — Anthropic SDK

### First AI API Call
```bash
pip install anthropic
```

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key-here")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Explain Python decorators in 3 simple sentences for a beginner student."
        }
    ],
)

print(message.content[0].text)
```

### Structured Output
```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a helpful coding tutor at TechPath Institute. Always respond in JSON format.",
    messages=[
        {
            "role": "user",
            "content": "Generate 3 beginner Python practice problems with hints. Return as JSON array."
        }
    ],
)

import json
problems = json.loads(message.content[0].text)
for p in problems:
    print(f"Problem: {p['title']}")
    print(f"Hint: {p['hint']}\n")
```

---

## Quick Reference

| Library | Install | Main Use |
|---------|---------|----------|
| `numpy` | `pip install numpy` | Arrays, math, random |
| `pandas` | `pip install pandas` | DataFrames, CSV, analysis |
| `matplotlib` | `pip install matplotlib` | Charts and plots |
| `seaborn` | `pip install seaborn` | Beautiful statistical charts |
| `requests` | `pip install requests` | HTTP API calls |
| `httpx` | `pip install httpx` | Async HTTP calls |
| `beautifulsoup4` | `pip install beautifulsoup4` | Web scraping |
| `anthropic` | `pip install anthropic` | Claude AI API |
| `python-dotenv` | `pip install python-dotenv` | Load .env files |
| `schedule` | `pip install schedule` | Task scheduling |
