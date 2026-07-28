# Module 11 — Python Libraries — Quick Revision Notes

---

## What are Libraries?
- Pre-written code packages you install with `pip install library_name`
- Import with `import library` or `from library import function`

## Pandas (Data Analysis)
```python
import pandas as pd

# Read data
df = pd.read_csv("data.csv")
df = pd.read_excel("data.xlsx")

# Explore
df.head()            # first 5 rows
df.shape             # (rows, columns)
df.info()            # column types
df.describe()        # statistics
df.columns           # column names
df.dtypes            # data types

# Select
df["name"]           # one column
df[["name", "age"]]  # multiple columns
df.iloc[0]           # first row by index
df.loc[0, "name"]    # specific cell

# Filter
df[df["age"] > 20]
df[df["city"] == "Bhopal"]
df[(df["marks"] >= 60) & (df["course"] == "ADCA")]

# Modify
df["total"] = df["hindi"] + df["english"] + df["maths"]
df["grade"] = df["percentage"].apply(lambda x: "Pass" if x >= 33 else "Fail")
df.rename(columns={"old_name": "new_name"})
df.drop(columns=["unwanted"])
df.dropna()           # remove rows with missing values
df.fillna(0)          # fill missing with 0

# Group & Aggregate
df.groupby("city")["marks"].mean()
df.groupby("course").agg({"marks": ["mean", "max", "count"]})
df.value_counts("category")

# Sort
df.sort_values("marks", ascending=False)

# Save
df.to_csv("output.csv", index=False)
df.to_excel("output.xlsx", index=False)
```

## Matplotlib (Charts)
```python
import matplotlib.pyplot as plt

# Line chart
plt.plot(x, y)
plt.title("Sales Over Time")
plt.xlabel("Month")
plt.ylabel("Sales (₹)")
plt.show()

# Bar chart
plt.bar(categories, values, color="skyblue")

# Pie chart
plt.pie(values, labels=labels, autopct="%1.1f%%")

# Multiple plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
ax1.bar(x, y)
ax2.plot(x, y)
plt.tight_layout()
plt.savefig("chart.png", dpi=150)
```

## Seaborn (Beautiful Charts)
```python
import seaborn as sns

sns.barplot(data=df, x="course", y="marks")
sns.histplot(df["age"], bins=10)
sns.boxplot(data=df, x="course", y="marks")
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
sns.scatterplot(data=df, x="hours_studied", y="marks", hue="pass_fail")
```

## Requests (HTTP/API)
```python
import requests

response = requests.get("https://api.example.com/data")
data = response.json()
print(response.status_code)  # 200 = OK
```

## OS & Pathlib (File System)
```python
import os
from pathlib import Path

os.listdir(".")                 # list files
os.path.exists("file.txt")     # check if exists
os.makedirs("folder", exist_ok=True)

path = Path("data/output.csv")
path.parent.mkdir(parents=True, exist_ok=True)
path.stem        # "output"
path.suffix      # ".csv"
```

## JSON
```python
import json

# Read
with open("data.json") as f:
    data = json.load(f)

# Write
with open("output.json", "w") as f:
    json.dump(data, f, indent=2)

# String conversion
json_str = json.dumps({"name": "Rahul"})
obj = json.loads(json_str)
```

## datetime
```python
from datetime import datetime, timedelta

now = datetime.now()
today = now.strftime("%d-%m-%Y")      # "23-07-2026"
formatted = now.strftime("%I:%M %p")  # "02:30 PM"
tomorrow = now + timedelta(days=1)
```

## Common pip Commands
```
pip install pandas matplotlib seaborn requests
pip install --upgrade pandas
pip list                 # all installed packages
pip freeze > requirements.txt
pip install -r requirements.txt
```
