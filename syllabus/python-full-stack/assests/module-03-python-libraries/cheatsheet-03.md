# Cheat Sheet — Python Libraries: Data, Automation & APIs

**Module 03 | Quick Reference Card**

---

## NumPy

```python
import numpy as np

# Create
np.array([1, 2, 3])              np.zeros(5)
np.ones((3, 4))                   np.arange(0, 10, 2)
np.linspace(0, 100, 5)           np.full(5, 42)
np.random.randint(0, 100, 10)    np.eye(3)

# Properties
arr.shape    arr.ndim    arr.size    arr.dtype

# Indexing
arr[0]    arr[-1]    arr[1:4]    arr[::-1]
arr[arr > 5]                     # Boolean filter
arr[[0, 2, 4]]                   # Fancy indexing
data[row, col]                   # 2D indexing
data[:, 0]                       # Entire column

# Math (vectorized — no loops!)
arr + 5    arr * 2    arr ** 2    arr1 + arr2

# Stats
arr.mean()    arr.std()     arr.var()
arr.min()     arr.max()     arr.sum()
arr.argmin()  arr.argmax()  np.median(arr)
np.percentile(arr, 75)
data.mean(axis=0)    # Per column
data.mean(axis=1)    # Per row

# Manipulation
arr.reshape(3, 4)    arr.flatten()    arr.T
np.vstack([a, b])    np.hstack([a, b])
np.concatenate([a, b])
np.where(arr > 5, "Yes", "No")
np.sort(arr)         np.unique(arr)
np.clip(arr, 0, 100)
```

---

## Pandas

```python
import pandas as pd

# Create
df = pd.DataFrame({"col": [1, 2, 3]})
pd.read_csv("f.csv")    pd.read_excel("f.xlsx")    pd.read_json("f.json")

# Explore
df.shape    df.columns    df.dtypes    df.info()    df.describe()
df.head()   df.tail()     df.sample()

# Select
df["col"]                        # Series
df[["col1", "col2"]]             # DataFrame
df.iloc[0]                       # Row by position
df.iloc[0:3]                     # Rows by position range
df.loc["label"]                  # Row by label

# Filter
df[df["marks"] > 80]
df[(df["city"] == "Bhopal") & (df["marks"] > 80)]
df[df["city"].isin(["Bhopal", "Pune"])]
df.query("marks > 80 and city == 'Bhopal'")
df[df["name"].str.contains("Ra")]

# Modify
df["new_col"] = df["fee"] * 1.18
df["grade"] = df["marks"].apply(lambda m: "Pass" if m >= 60 else "Fail")
df = df.rename(columns={"old": "new"})
df = df.drop(columns=["col"])

# Sort
df.sort_values("marks", ascending=False)
df.nlargest(3, "marks")

# Group
df.groupby("city")["marks"].mean()
df.groupby("city").agg(count=("name","count"), avg=("marks","mean"))

# Merge
pd.merge(df1, df2, on="key", how="inner")  # inner/left/right/outer

# Pivot
df.pivot_table(values="marks", index="course", columns="city", aggfunc="mean")

# Missing
df.isnull().sum()    df.dropna()    df.fillna(0)

# Stats
df["col"].value_counts()    df["col"].unique()    df["col"].nunique()

# Save
df.to_csv("out.csv", index=False)
df.to_json("out.json", orient="records")
```

---

## Matplotlib

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))

# Charts
plt.plot(x, y, marker="o")                    # Line
plt.bar(x, y, color="#3498db")                 # Bar
plt.barh(y, x)                                # Horizontal bar
plt.scatter(x, y, c=colors, cmap="RdYlGn")    # Scatter
plt.pie(values, labels=labels, autopct="%1.1f%%")  # Pie
plt.hist(data, bins=20)                        # Histogram

# Customize
plt.title("Title")    plt.xlabel("X")    plt.ylabel("Y")
plt.grid(True, alpha=0.3)    plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

# Subplots
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
axes[0].bar(x, y)

# Save
plt.savefig("chart.png", dpi=150)
plt.show()
```

## Seaborn

```python
import seaborn as sns

sns.barplot(data=df, x="col", y="val", hue="cat")
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
sns.boxplot(data=df, x="cat", y="val")
sns.histplot(data, bins=20, kde=True)
sns.pairplot(df)
sns.set_theme(style="whitegrid")
```

---

## requests / httpx

```python
import requests

# GET
r = requests.get(url)
r = requests.get(url, params={"key": "val"}, headers={"Auth": "Bearer tok"})
r.status_code    r.ok    r.json()    r.text
r.raise_for_status()

# POST
r = requests.post(url, json={"key": "val"})

# PUT / PATCH / DELETE
r = requests.put(url, json=data)
r = requests.patch(url, json=partial)
r = requests.delete(url)

# Auth
headers = {"Authorization": "Bearer token"}
requests.get(url, headers=headers)

# Session
s = requests.Session()
s.headers.update({"Auth": "Bearer tok"})
s.get(url)

# Error handling
try:
    r = requests.get(url, timeout=10)
    r.raise_for_status()
except requests.exceptions.ConnectionError: ...
except requests.exceptions.Timeout: ...
except requests.exceptions.HTTPError: ...

# Async (httpx)
import httpx, asyncio
async with httpx.AsyncClient() as c:
    r = await c.get(url)
    results = await asyncio.gather(c.get(u1), c.get(u2))
```

---

## BeautifulSoup

```python
from bs4 import BeautifulSoup
import requests

soup = BeautifulSoup(html, "html.parser")

# Find
soup.find("tag")                     # First match
soup.find("div", class_="name")      # By class
soup.find("div", id="main")          # By ID
soup.find_all("li")                  # All matches

# CSS selectors
soup.select(".class")                # By class
soup.select("#id")                   # By ID
soup.select("div.class > p")        # Nested
soup.select_one("a[href*='contact']")

# Extract
element.text                         # Text content
element.get_text(strip=True)         # Stripped text
element["href"]                      # Attribute
element.get("class")                 # Attribute (safe)

# Navigate
element.parent    element.children    element.next_sibling
```

---

## Automation

```python
# pathlib (preferred)
from pathlib import Path
p = Path("data") / "file.csv"
p.exists()    p.is_file()    p.is_dir()
p.name    p.stem    p.suffix    p.parent
p.read_text()    p.write_text("hi")
p.mkdir(parents=True, exist_ok=True)
list(Path(".").glob("**/*.py"))

# shutil
import shutil
shutil.copy(src, dst)         shutil.copytree(src, dst)
shutil.move(src, dst)         shutil.rmtree(dir)

# dotenv
from dotenv import load_dotenv
import os
load_dotenv()
os.getenv("KEY", "default")

# logging
import logging
logging.basicConfig(level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s")
logger = logging.getLogger("app")
logger.info("msg")    logger.error("msg")    logger.warning("msg")

# schedule
import schedule
schedule.every(5).minutes.do(func)
schedule.every().day.at("09:00").do(func)
```

---

## AI SDKs

```python
# Anthropic (Claude)
import anthropic
client = anthropic.Anthropic()    # reads ANTHROPIC_API_KEY
msg = client.messages.create(
    model="claude-sonnet-4-20250514", max_tokens=1024,
    system="You are a helpful tutor.",
    messages=[{"role": "user", "content": "Explain X"}],
)
print(msg.content[0].text)

# Streaming
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="")

# OpenAI (GPT)
from openai import OpenAI
client = OpenAI()    # reads OPENAI_API_KEY
r = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."},
    ],
)
print(r.choices[0].message.content)
```

---

## HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | OK | Process response |
| 201 | Created | Resource created |
| 400 | Bad Request | Fix your data |
| 401 | Unauthorized | Check API key |
| 403 | Forbidden | No permission |
| 404 | Not Found | Check URL |
| 429 | Rate Limited | Wait and retry |
| 500 | Server Error | Not your fault |
