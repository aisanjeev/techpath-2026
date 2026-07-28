# NumPy & Pandas — Data Handling in Python

**Module 11 — Python Libraries | Topic 1**

---

## Why Libraries?

Python alone is great, but **libraries** give it superpowers:

| Library | What It Does |
|---------|-------------|
| **NumPy** | Fast math on arrays/matrices |
| **Pandas** | Work with tables (DataFrames) |
| **Matplotlib** | Create charts and graphs |
| **Seaborn** | Beautiful statistical charts |
| **Requests** | Talk to web APIs |

### Installing

```bash
pip install numpy pandas matplotlib seaborn requests
```

---

## NumPy — Numbers Made Fast

```python
import numpy as np

# Create arrays
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

# Math on entire array (no loops needed!)
print(a + b)         # [11 22 33 44 55]
print(a * 2)         # [ 2  4  6  8 10]
print(a ** 2)        # [ 1  4  9 16 25]

# Statistics
print(np.mean(a))    # 3.0 (average)
print(np.sum(a))     # 15
print(np.max(a))     # 5
print(np.min(a))     # 1
print(np.std(a))     # 1.41 (standard deviation)

# 2D array (matrix)
matrix = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])
print(matrix.shape)     # (3, 3)
print(matrix[0, 1])     # 2 (row 0, col 1)

# Useful functions
zeros = np.zeros((3, 3))       # 3x3 matrix of zeros
ones = np.ones((2, 4))         # 2x4 matrix of ones
rand = np.random.rand(5)       # 5 random numbers 0-1
nums = np.arange(0, 10, 2)    # [0, 2, 4, 6, 8]
space = np.linspace(0, 1, 5)  # [0, 0.25, 0.5, 0.75, 1.0]
```

---

## Pandas — Tables Made Easy

Pandas works with **DataFrames** — think of them as smart Excel spreadsheets in Python.

### Creating a DataFrame

```python
import pandas as pd

# From dictionary
data = {
    "Name": ["Rahul", "Priya", "Amit", "Sneha", "Karan"],
    "Age": [20, 22, 21, 23, 20],
    "Course": ["ADCA", "BCA", "ADCA", "BCA", "ADCA"],
    "Marks": [85, 92, 78, 95, 88]
}
df = pd.DataFrame(data)
print(df)
```

Output:
```
    Name  Age Course  Marks
0  Rahul   20   ADCA     85
1  Priya   22    BCA     92
2   Amit   21   ADCA     78
3  Sneha   23    BCA     95
4  Karan   20   ADCA     88
```

### Reading Files

```python
# Read CSV file
df = pd.read_csv("students.csv")

# Read Excel file
df = pd.read_excel("students.xlsx")

# Save to file
df.to_csv("output.csv", index=False)
df.to_excel("output.xlsx", index=False)
```

### Exploring Data

```python
df.head()           # First 5 rows
df.tail()           # Last 5 rows
df.shape            # (rows, columns)
df.columns          # Column names
df.dtypes           # Data types
df.info()           # Summary info
df.describe()       # Statistics (mean, min, max, etc.)
```

### Selecting Data

```python
# Single column
df["Name"]

# Multiple columns
df[["Name", "Marks"]]

# Single row by index
df.iloc[0]              # First row

# Rows by condition
df[df["Marks"] > 80]           # Students with marks > 80
df[df["Course"] == "ADCA"]     # Only ADCA students
df[(df["Marks"] > 80) & (df["Age"] < 22)]  # Combined
```

### Modifying Data

```python
# Add new column
df["Grade"] = df["Marks"].apply(
    lambda x: "A" if x >= 90 else "B" if x >= 75 else "C"
)

# Rename columns
df.rename(columns={"Marks": "Score"}, inplace=True)

# Sort
df.sort_values("Marks", ascending=False)

# Drop column
df.drop("Grade", axis=1, inplace=True)

# Fill missing values
df["Age"].fillna(df["Age"].mean(), inplace=True)
```

### Grouping & Aggregation

```python
# Average marks by course
df.groupby("Course")["Marks"].mean()

# Multiple stats
df.groupby("Course").agg({
    "Marks": ["mean", "max", "min", "count"],
    "Age": "mean"
})
```

---

## Matplotlib — Charts & Graphs

```python
import matplotlib.pyplot as plt

# Line chart
plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
plt.title("Sales Over Time")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.show()

# Bar chart
courses = ["Python", "Web Dev", "AI", "Data"]
students = [45, 38, 52, 30]
plt.bar(courses, students, color=["blue", "green", "red", "orange"])
plt.title("Students per Course")
plt.show()

# Pie chart
plt.pie(students, labels=courses, autopct="%1.1f%%")
plt.title("Course Distribution")
plt.show()

# Save chart as image
plt.savefig("chart.png", dpi=300)
```

---

## Seaborn — Beautiful Statistical Charts

```python
import seaborn as sns

# Using a Pandas DataFrame
sns.barplot(data=df, x="Course", y="Marks")
plt.title("Average Marks by Course")
plt.show()

# Histogram
sns.histplot(df["Marks"], bins=10)
plt.show()

# Heatmap (for correlation)
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.show()
```

---

## Requests — Talking to APIs

```python
import requests

# GET request
response = requests.get("https://api.github.com/users/python")
data = response.json()
print(data["name"])         # Python
print(data["public_repos"]) # Number of repos

# POST request
response = requests.post("https://api.example.com/data", json={
    "name": "Rahul",
    "email": "rahul@email.com"
})
print(response.status_code)  # 200 = success
```

---

## Summary

- **NumPy** — fast math on arrays: `np.array()`, `np.mean()`, `np.sum()`
- **Pandas** — tables (DataFrames): `pd.read_csv()`, `df.groupby()`, `df.describe()`
- **Matplotlib** — charts: `plt.bar()`, `plt.plot()`, `plt.pie()`
- **Seaborn** — beautiful stats charts built on Matplotlib
- **Requests** — call web APIs: `requests.get()`, `.json()`
- Install with `pip install` — Python's package manager
