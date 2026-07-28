# Cheat Sheet: Python Libraries

**Module 11 — Quick Reference**

---

## NumPy

```python
import numpy as np
a = np.array([1, 2, 3, 4, 5])
np.mean(a)    # Average
np.sum(a)     # Total
np.max(a)     # Maximum
np.min(a)     # Minimum
np.std(a)     # Standard deviation
```

---

## Pandas

```python
import pandas as pd

# Read data
df = pd.read_csv("file.csv")
df = pd.read_excel("file.xlsx")

# Explore
df.head()       # First 5 rows
df.shape        # (rows, cols)
df.describe()   # Statistics
df.info()       # Data types

# Select
df["Name"]                    # One column
df[["Name", "Age"]]           # Multiple
df[df["Marks"] > 80]          # Filter
df.iloc[0]                    # First row

# Modify
df["Grade"] = "A"             # New column
df.sort_values("Marks")       # Sort
df.groupby("Course").mean()   # Group stats

# Save
df.to_csv("out.csv", index=False)
```

---

## Matplotlib

```python
import matplotlib.pyplot as plt

plt.bar(x, y)        # Bar chart
plt.plot(x, y)       # Line chart
plt.pie(values)      # Pie chart
plt.title("Title")
plt.xlabel("X")
plt.ylabel("Y")
plt.show()
plt.savefig("chart.png")
```

---

## Requests

```python
import requests
r = requests.get("https://api.example.com/data")
data = r.json()          # Parse JSON
r.status_code            # 200 = OK
```

---

## JSON

```python
import json
json.dumps(dict)         # Dict → JSON string
json.loads(string)       # JSON string → Dict
json.load(file)          # Read JSON file
json.dump(data, file)    # Write JSON file
```

---

## BeautifulSoup

```python
from bs4 import BeautifulSoup
soup = BeautifulSoup(html, "html.parser")
soup.find("tag")              # First match
soup.find_all("div", class_="x")  # All matches
element.text                  # Text content
element["href"]               # Attribute
```

---

## Virtual Environment

```bash
python -m venv myenv
myenv\Scripts\activate     # Windows
pip install pandas
pip freeze > requirements.txt
deactivate
```
