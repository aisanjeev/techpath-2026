# Pandas DataFrames

**Module 03 — Python Libraries: Data, Automation & APIs | Topic 2**

---

## What is Pandas?

Pandas is the most important Python library for data analysis. It provides the **DataFrame** — a table (like an Excel spreadsheet) that you can filter, sort, group, merge, and analyze with simple commands.

```bash
pip install pandas
```

```python
import pandas as pd
```

---

## Series — One Column of Data

A Series is a one-dimensional array with labels (index).

```python
marks = pd.Series([85, 92, 78, 88], index=["Rahul", "Priya", "Amit", "Sneha"])
print(marks)
# Rahul    85
# Priya    92
# Amit     78
# Sneha    88

print(marks["Priya"])      # 92
print(marks.mean())        # 85.75
print(marks[marks > 80])   # Only Rahul, Priya, Sneha
```

---

## DataFrame — The Table

A DataFrame is a 2D table with rows and columns — like a spreadsheet.

### Creating DataFrames

```python
# From a dictionary
data = {
    "name": ["Rahul", "Priya", "Amit", "Sneha", "Vikram"],
    "city": ["Bhopal", "Pune", "Delhi", "Bhopal", "Delhi"],
    "course": ["Python FS", "Web Dev", "Python FS", "Data Science", "Python FS"],
    "fee": [25000, 20000, 25000, 30000, 25000],
    "marks": [85, 92, 78, 88, 65],
}
df = pd.DataFrame(data)
print(df)
#      name    city       course    fee  marks
# 0   Rahul  Bhopal    Python FS  25000     85
# 1   Priya    Pune      Web Dev  20000     92
# 2    Amit   Delhi    Python FS  25000     78
# 3   Sneha  Bhopal  Data Science  30000     88
# 4  Vikram   Delhi    Python FS  25000     65
```

### Basic Exploration

```python
print(df.shape)        # (5, 5) — 5 rows, 5 columns
print(df.columns)      # Index(['name', 'city', 'course', 'fee', 'marks'])
print(df.dtypes)       # Data type of each column
print(df.info())       # Summary: columns, types, non-null counts
print(df.describe())   # Stats for numeric columns
print(df.head(3))      # First 3 rows
print(df.tail(2))      # Last 2 rows
print(df.sample(2))    # 2 random rows
```

---

## Reading Data from Files

### CSV Files

```python
# Read CSV
df = pd.read_csv("students.csv")

# With options
df = pd.read_csv(
    "students.csv",
    encoding="utf-8",
    na_values=["N/A", ""],    # Treat as NaN
    parse_dates=["join_date"],
)

# Save to CSV
df.to_csv("output.csv", index=False)
```

### Excel Files

```python
df = pd.read_excel("students.xlsx", sheet_name="Sheet1")
df.to_excel("output.xlsx", index=False)
```

### JSON

```python
df = pd.read_json("students.json")
df.to_json("output.json", orient="records", indent=2)
```

---

## Selecting Data

### Selecting Columns

```python
# Single column (returns Series)
names = df["name"]

# Multiple columns (returns DataFrame)
subset = df[["name", "marks"]]
```

### Selecting Rows

```python
# By index position (iloc)
print(df.iloc[0])       # First row
print(df.iloc[0:3])     # First 3 rows
print(df.iloc[0, 1])    # Row 0, Column 1

# By label (loc)
df.index = ["S1", "S2", "S3", "S4", "S5"]
print(df.loc["S1"])           # Row with label S1
print(df.loc["S1":"S3"])      # Rows S1 to S3 (inclusive!)
print(df.loc["S1", "name"])   # Specific cell
```

---

## Filtering Data

```python
# Single condition
top_students = df[df["marks"] > 80]
print(top_students)

# Multiple conditions (use & for AND, | for OR)
bhopal_toppers = df[(df["city"] == "Bhopal") & (df["marks"] > 80)]
print(bhopal_toppers)

# Using isin()
selected_cities = df[df["city"].isin(["Bhopal", "Pune"])]

# Using query() — more readable
result = df.query("marks > 80 and city == 'Bhopal'")

# String methods
python_courses = df[df["course"].str.contains("Python")]
```

---

## Adding and Modifying Columns

```python
# New column from calculation
df["fee_with_gst"] = df["fee"] * 1.18

# Conditional column
df["result"] = df["marks"].apply(lambda m: "Pass" if m >= 60 else "Fail")

# Using np.where
import numpy as np
df["grade"] = np.where(df["marks"] >= 90, "A+",
              np.where(df["marks"] >= 80, "A",
              np.where(df["marks"] >= 70, "B",
              np.where(df["marks"] >= 60, "C", "F"))))

# Rename columns
df = df.rename(columns={"fee": "base_fee", "marks": "total_marks"})

# Drop columns
df = df.drop(columns=["fee_with_gst"])
```

---

## Sorting

```python
# Sort by one column
df_sorted = df.sort_values("marks", ascending=False)

# Sort by multiple columns
df_sorted = df.sort_values(["city", "marks"], ascending=[True, False])

# Sort by index
df_sorted = df.sort_index()

# Get top N
top_3 = df.nlargest(3, "marks")
bottom_3 = df.nsmallest(3, "marks")
```

---

## GroupBy — Split, Apply, Combine

GroupBy is one of the most powerful Pandas features. It groups rows by a column, applies a function, and combines the results.

```python
# Average marks by city
print(df.groupby("city")["marks"].mean())
# Bhopal    86.5
# Delhi     71.5
# Pune      92.0

# Multiple aggregations
city_stats = df.groupby("city").agg(
    student_count=("name", "count"),
    avg_marks=("marks", "mean"),
    total_fee=("fee", "sum"),
    top_marks=("marks", "max"),
)
print(city_stats)

# Group by multiple columns
course_city = df.groupby(["course", "city"])["marks"].mean()
print(course_city)

# Custom aggregation
df.groupby("city")["marks"].agg(["mean", "min", "max", "count"])
```

---

## Merge — Joining DataFrames

```python
# Students table
students = pd.DataFrame({
    "student_id": [1, 2, 3, 4],
    "name": ["Rahul", "Priya", "Amit", "Sneha"],
    "city": ["Bhopal", "Pune", "Delhi", "Bhopal"],
})

# Enrollment table
enrollments = pd.DataFrame({
    "student_id": [1, 2, 3, 5],
    "course": ["Python FS", "Web Dev", "Python FS", "Data Science"],
    "fee": [25000, 20000, 25000, 30000],
})

# Inner join — only matching rows
inner = pd.merge(students, enrollments, on="student_id", how="inner")
# student_id 4 and 5 are excluded

# Left join — all students, matched enrollments
left = pd.merge(students, enrollments, on="student_id", how="left")
# student_id 4 has NaN for course and fee

# Outer join — all from both
outer = pd.merge(students, enrollments, on="student_id", how="outer")
```

| Join Type | Keeps |
|-----------|-------|
| `inner` | Only matching rows |
| `left` | All from left + matches from right |
| `right` | All from right + matches from left |
| `outer` | All from both |

---

## Pivot Tables

```python
# Sample data
sales = pd.DataFrame({
    "month": ["Jan", "Jan", "Feb", "Feb", "Mar", "Mar"],
    "city": ["Bhopal", "Delhi", "Bhopal", "Delhi", "Bhopal", "Delhi"],
    "revenue": [50000, 75000, 55000, 80000, 60000, 85000],
})

# Pivot — rows=month, columns=city, values=revenue
pivot = sales.pivot_table(
    values="revenue",
    index="month",
    columns="city",
    aggfunc="sum",
)
print(pivot)
# city     Bhopal  Delhi
# month
# Feb      55000  80000
# Jan      50000  75000
# Mar      60000  85000
```

---

## Handling Missing Data

```python
# Check for missing values
print(df.isnull().sum())        # Count NaN per column
print(df.isnull().any())        # Which columns have NaN

# Drop rows with missing values
clean = df.dropna()              # Drop any row with NaN
clean = df.dropna(subset=["marks"])  # Only check 'marks' column

# Fill missing values
df["marks"] = df["marks"].fillna(0)              # Fill with 0
df["city"] = df["city"].fillna("Unknown")        # Fill with text
df["marks"] = df["marks"].fillna(df["marks"].mean())  # Fill with mean
```

---

## Common Operations

```python
# Value counts
print(df["city"].value_counts())
# Bhopal    2
# Delhi     2
# Pune      1

# Unique values
print(df["city"].unique())       # ['Bhopal' 'Pune' 'Delhi']
print(df["city"].nunique())      # 3

# Apply a function
df["name_upper"] = df["name"].apply(str.upper)
df["fee_category"] = df["fee"].apply(
    lambda f: "Premium" if f >= 25000 else "Standard"
)

# Map — replace values
df["city_code"] = df["city"].map({
    "Bhopal": "BPL",
    "Delhi": "DEL",
    "Pune": "PNQ",
})

# String methods
df["name_length"] = df["name"].str.len()
df["first_name"] = df["name"].str.split().str[0]
df["is_python"] = df["course"].str.contains("Python")
```

---

## Summary

| Operation | Syntax |
|-----------|--------|
| Create | `pd.DataFrame(dict)` |
| Read CSV | `pd.read_csv("file.csv")` |
| Select column | `df["col"]` or `df[["col1","col2"]]` |
| Filter rows | `df[df["col"] > value]` |
| Sort | `df.sort_values("col")` |
| Group | `df.groupby("col")["val"].mean()` |
| Merge | `pd.merge(df1, df2, on="key")` |
| Pivot | `df.pivot_table(values, index, columns)` |
| Missing data | `df.fillna(0)`, `df.dropna()` |
| Apply | `df["col"].apply(func)` |
| Value counts | `df["col"].value_counts()` |
| Save | `df.to_csv("out.csv", index=False)` |

---

## Practice Tasks

1. Load a CSV file and display basic info (shape, types, head)
2. Filter students who scored above 80 and are from Bhopal
3. Group by city and calculate average marks and total fee
4. Merge two DataFrames (students and courses) on a common key
5. Create a pivot table showing average marks by course and city
