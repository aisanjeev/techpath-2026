# Web Scraping with BeautifulSoup

**Module 03 — Python Libraries: Data, Automation & APIs | Topic 5**

---

## What is Web Scraping?

Web scraping is extracting data from websites. When a website does not provide an API, you can read its HTML and pull out the data you need.

**Real-world analogy:** Imagine copying data from a website into an Excel sheet manually. Web scraping automates this — your Python script does the copying for you, in seconds.

```bash
pip install beautifulsoup4 requests
```

---

## How the Web Works (For Scraping)

```
1. You send a GET request → Server sends back HTML
2. Python receives the HTML text
3. BeautifulSoup parses the HTML into a tree structure
4. You navigate the tree to find the data you need
```

---

## HTML Basics for Scraping

```html
<html>
  <body>
    <h1 class="title">TechPath Institute</h1>
    <div id="courses">
      <ul>
        <li class="course">Python Full Stack — ₹25,000</li>
        <li class="course">Web Development — ₹20,000</li>
        <li class="course">Data Science — ₹30,000</li>
      </ul>
    </div>
    <a href="/contact">Contact Us</a>
  </body>
</html>
```

Key HTML concepts:
- **Tags:** `<h1>`, `<div>`, `<li>`, `<a>`
- **Attributes:** `class="title"`, `id="courses"`, `href="/contact"`
- **Nesting:** Tags inside tags form a tree

---

## BeautifulSoup Basics

```python
from bs4 import BeautifulSoup
import requests

# Step 1: Get the HTML
html = """
<html>
<body>
    <h1 class="title">TechPath Institute</h1>
    <div id="courses">
        <ul>
            <li class="course">Python Full Stack — ₹25,000</li>
            <li class="course">Web Development — ₹20,000</li>
            <li class="course">Data Science — ₹30,000</li>
        </ul>
    </div>
    <p>Location: <span class="city">Bhopal</span></p>
    <a href="https://techpath.com/contact">Contact Us</a>
</body>
</html>
"""

# Step 2: Parse it
soup = BeautifulSoup(html, "html.parser")

# Step 3: Find elements
print(soup.title)                           # None (no <title> tag in this HTML)
print(soup.h1.text)                         # TechPath Institute
print(soup.find("h1").text)                 # TechPath Institute
print(soup.find("span", class_="city").text)  # Bhopal
```

---

## Finding Elements

### find() — First Match

```python
# By tag name
h1 = soup.find("h1")
print(h1.text)    # TechPath Institute

# By class
city = soup.find("span", class_="city")
print(city.text)    # Bhopal

# By ID
courses_div = soup.find("div", id="courses")
print(courses_div.text.strip())

# By attribute
link = soup.find("a", href=True)
print(link["href"])    # https://techpath.com/contact
print(link.text)       # Contact Us
```

### find_all() — All Matches

```python
# All course items
courses = soup.find_all("li", class_="course")
for course in courses:
    print(course.text)
# Python Full Stack — ₹25,000
# Web Development — ₹20,000
# Data Science — ₹30,000

# All links
links = soup.find_all("a")
for link in links:
    print(f"{link.text} → {link.get('href')}")
```

### CSS Selectors with select()

```python
# By class (.)
courses = soup.select(".course")

# By ID (#)
div = soup.select_one("#courses")

# Nested
items = soup.select("#courses li")

# Multiple classes
soup.select(".course.featured")

# By attribute
soup.select('a[href*="contact"]')
```

---

## Scraping a Real Website

```python
import requests
from bs4 import BeautifulSoup

def scrape_quotes():
    """Scrape quotes from quotes.toscrape.com."""
    url = "https://quotes.toscrape.com/"
    response = requests.get(url)
    
    if not response.ok:
        print(f"Failed: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = []
    
    for quote_div in soup.find_all("div", class_="quote"):
        text = quote_div.find("span", class_="text").text
        author = quote_div.find("small", class_="author").text
        tags = [tag.text for tag in quote_div.find_all("a", class_="tag")]
        
        quotes.append({
            "text": text,
            "author": author,
            "tags": tags,
        })
    
    return quotes

# Usage
quotes = scrape_quotes()
for q in quotes[:3]:
    print(f'"{q["text"]}"')
    print(f"  — {q['author']}")
    print(f"  Tags: {', '.join(q['tags'])}")
    print()
```

---

## Scraping Tables

```python
import pandas as pd
from bs4 import BeautifulSoup

html = """
<table>
    <tr><th>Name</th><th>City</th><th>Marks</th></tr>
    <tr><td>Rahul</td><td>Bhopal</td><td>85</td></tr>
    <tr><td>Priya</td><td>Pune</td><td>92</td></tr>
    <tr><td>Amit</td><td>Delhi</td><td>78</td></tr>
</table>
"""

soup = BeautifulSoup(html, "html.parser")
table = soup.find("table")

# Manual extraction
rows = []
for tr in table.find_all("tr")[1:]:    # Skip header
    cells = [td.text for td in tr.find_all("td")]
    rows.append(cells)

print(rows)
# [['Rahul', 'Bhopal', '85'], ['Priya', 'Pune', '92'], ['Amit', 'Delhi', '78']]

# Easier: Pandas reads tables directly!
dfs = pd.read_html(html)
print(dfs[0])
#     Name    City  Marks
# 0  Rahul  Bhopal     85
# 1  Priya    Pune     92
# 2   Amit   Delhi     78
```

---

## Pagination — Scraping Multiple Pages

```python
import requests
from bs4 import BeautifulSoup
import time

def scrape_all_quotes():
    """Scrape quotes from all pages."""
    all_quotes = []
    page = 1
    
    while True:
        url = f"https://quotes.toscrape.com/page/{page}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        
        quotes = soup.find_all("div", class_="quote")
        if not quotes:
            break    # No more quotes — stop
        
        for q in quotes:
            all_quotes.append({
                "text": q.find("span", class_="text").text,
                "author": q.find("small", class_="author").text,
            })
        
        print(f"Page {page}: {len(quotes)} quotes")
        page += 1
        time.sleep(1)    # Be polite — wait between requests
    
    return all_quotes

quotes = scrape_all_quotes()
print(f"Total quotes scraped: {len(quotes)}")
```

---

## Ethical Scraping Rules

| Rule | Why |
|------|-----|
| Check `robots.txt` | The website tells you what you can/cannot scrape |
| Add delays between requests | Don't overload the server |
| Set a User-Agent header | Identify yourself |
| Don't scrape personal data | Privacy and legal issues |
| Use APIs when available | Faster, more reliable, approved by the site |
| Respect rate limits | Follow the website's rules |
| Cache responses | Don't re-download the same page |

```python
headers = {
    "User-Agent": "TechPath Student Bot (educational purposes)"
}
response = requests.get(url, headers=headers)

# Check robots.txt
# Visit: https://example.com/robots.txt
```

---

## Saving Scraped Data

```python
import json
import csv

# Save as JSON
with open("quotes.json", "w") as f:
    json.dump(quotes, f, indent=2, ensure_ascii=False)

# Save as CSV
with open("quotes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "author"])
    writer.writeheader()
    writer.writerows(quotes)

# Save as DataFrame
import pandas as pd
df = pd.DataFrame(quotes)
df.to_csv("quotes.csv", index=False)
```

---

## Common Scraping Patterns

```python
# Get text content
element.text                 # Text inside the tag
element.get_text(strip=True)  # Stripped text

# Get attribute
element["href"]              # Link URL
element.get("class")         # Class (returns list or None)
element.get("data-id")       # Any attribute

# Navigate the tree
element.parent               # Parent element
element.children             # Direct children
element.next_sibling         # Next sibling
element.find_next("p")       # Next <p> anywhere after

# Check if element exists
if soup.find("h2"):
    print(soup.find("h2").text)
```

---

## Summary

| Concept | Syntax | Purpose |
|---------|--------|---------|
| Parse HTML | `BeautifulSoup(html, "html.parser")` | Create soup object |
| Find one | `soup.find("tag", class_="name")` | First matching element |
| Find all | `soup.find_all("tag")` | All matching elements |
| CSS select | `soup.select(".class #id tag")` | CSS selector syntax |
| Get text | `element.text` | Text content |
| Get attribute | `element["href"]` | HTML attribute value |
| Save data | `json.dump()` / `pd.DataFrame()` | Export scraped data |

---

## Practice Tasks

1. Scrape quotes from `quotes.toscrape.com` and save as JSON
2. Scrape a table from any website and convert to a Pandas DataFrame
3. Build a function that scrapes all pages (pagination) with polite delays
4. Extract all links from a webpage and categorize them (internal vs external)
5. Scrape product prices from a sample e-commerce page and find the cheapest item
