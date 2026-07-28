# NumPy Arrays

**Module 03 — Python Libraries: Data, Automation & APIs | Topic 1**

---

## What is NumPy?

NumPy (Numerical Python) is the foundation library for scientific computing in Python. It provides fast, memory-efficient arrays and mathematical operations.

**Why not just use Python lists?**

| Feature | Python List | NumPy Array |
|---------|------------|-------------|
| Speed | Slow for math | 10-100x faster |
| Memory | Uses more | Uses less |
| Operations | Loop through each item | Operate on entire array |
| Data type | Can mix types | All same type |
| Math support | Basic | Advanced (linear algebra, stats) |

```bash
pip install numpy
```

---

## Creating Arrays

```python
import numpy as np

# From a Python list
marks = np.array([85, 92, 78, 88, 95])
print(marks)           # [85 92 78 88 95]
print(type(marks))     # <class 'numpy.ndarray'>
print(marks.dtype)     # int64

# With specific type
prices = np.array([99.5, 149.0, 299.9], dtype=np.float32)

# 2D array (matrix)
student_marks = np.array([
    [85, 92, 78],    # Rahul: Python, Django, React
    [90, 88, 95],    # Priya
    [72, 68, 75],    # Amit
])
print(student_marks.shape)    # (3, 3) — 3 students, 3 subjects
print(student_marks.ndim)     # 2 — dimensions
print(student_marks.size)     # 9 — total elements
```

### Array Creation Functions

```python
# Zeros
empty_marks = np.zeros(5)                # [0. 0. 0. 0. 0.]
grid = np.zeros((3, 4))                  # 3x4 matrix of zeros

# Ones
weights = np.ones(5)                     # [1. 1. 1. 1. 1.]

# Full — fill with a value
defaults = np.full(5, 60)               # [60 60 60 60 60]

# Range
indices = np.arange(0, 10, 2)           # [0 2 4 6 8]

# Evenly spaced
percentages = np.linspace(0, 100, 5)    # [  0.  25.  50.  75. 100.]

# Identity matrix
identity = np.eye(3)
# [[1. 0. 0.]
#  [0. 1. 0.]
#  [0. 0. 1.]]
```

---

## Indexing and Slicing

```python
marks = np.array([85, 92, 78, 88, 95, 72, 60])

# Basic indexing
print(marks[0])      # 85 (first)
print(marks[-1])     # 60 (last)
print(marks[2:5])    # [78 88 95]

# 2D indexing
data = np.array([
    [85, 92, 78],
    [90, 88, 95],
    [72, 68, 75],
])

print(data[0, 1])      # 92 (row 0, col 1)
print(data[1])          # [90 88 95] (entire row 1)
print(data[:, 0])       # [85 90 72] (entire column 0)
print(data[0:2, 1:3])   # [[92 78] [88 95]] (sub-matrix)

# Boolean indexing (filtering)
marks = np.array([85, 42, 91, 58, 73, 36, 88])
passing = marks[marks >= 60]
print(passing)    # [85 91 73 88]

# Fancy indexing
print(marks[[0, 2, 4]])    # [85 91 73] — pick specific indices
```

---

## Vectorized Operations

NumPy operations work on the entire array at once — no loops needed. This is called **vectorization**.

```python
marks = np.array([85, 92, 78, 88, 95])

# Arithmetic on entire array
print(marks + 5)         # [90 97 83 93 100]
print(marks * 1.1)       # [93.5 101.2  85.8  96.8 104.5]
print(marks / 100)       # [0.85 0.92 0.78 0.88 0.95]
print(marks ** 2)        # [7225 8464 6084 7744 9025]

# Comparison
print(marks > 80)        # [True True False True True]
print(marks == 92)       # [False True False False False]

# Between arrays
midterm = np.array([78, 85, 72, 90, 88])
final = np.array([85, 92, 78, 88, 95])

average = (midterm + final) / 2
print(average)    # [81.5 88.5 75.  89.  91.5]

improvement = final - midterm
print(improvement)    # [ 7  7  6 -2  7]
```

### Real-World Example: Fee Calculation

```python
base_fees = np.array([25000, 20000, 15000, 30000, 18000])

# Apply 18% GST
gst = base_fees * 0.18
total = base_fees + gst
print(f"Total fees: {total}")
# [29500. 23600. 17700. 35400. 21240.]

# Apply 10% discount to fees above ₹20,000
discounted = np.where(base_fees > 20000, base_fees * 0.9, base_fees)
print(f"After discount: {discounted}")
# [22500. 20000. 15000. 27000. 18000.]
```

---

## Statistics

```python
marks = np.array([85, 92, 78, 88, 95, 72, 60, 45])

print(f"Mean:     {marks.mean():.1f}")       # 76.9
print(f"Median:   {np.median(marks):.1f}")   # 81.5
print(f"Std Dev:  {marks.std():.1f}")        # 15.8
print(f"Variance: {marks.var():.1f}")        # 249.9
print(f"Max:      {marks.max()}")            # 95
print(f"Min:      {marks.min()}")            # 45
print(f"Sum:      {marks.sum()}")            # 615
print(f"Argmax:   {marks.argmax()}")         # 4 (index of max)
print(f"Argmin:   {marks.argmin()}")         # 7 (index of min)

# Percentile
print(f"25th percentile: {np.percentile(marks, 25)}")
print(f"75th percentile: {np.percentile(marks, 75)}")

# Per-column stats (axis=0) or per-row (axis=1)
data = np.array([
    [85, 92, 78],    # Rahul
    [90, 88, 95],    # Priya
    [72, 68, 75],    # Amit
])
print("Subject averages:", data.mean(axis=0))    # [82.33 82.67 82.67]
print("Student averages:", data.mean(axis=1))    # [85.   91.   71.67]
```

---

## Broadcasting

Broadcasting lets NumPy handle operations between arrays of different shapes:

```python
# Marks scaled by subject weights
marks = np.array([
    [85, 92, 78],    # Rahul: Python, Django, React
    [90, 88, 95],    # Priya
])
weights = np.array([0.4, 0.35, 0.25])    # Subject weights

# Broadcasting: (2,3) * (3,) → (2,3)
weighted = marks * weights
print(weighted)
# [[34.   32.2  19.5 ]
#  [36.   30.8  23.75]]

weighted_total = weighted.sum(axis=1)
print(f"Weighted totals: {weighted_total}")    # [85.7  90.55]
```

---

## Reshaping and Manipulation

```python
# Reshape
a = np.arange(12)            # [ 0  1  2 ... 11]
b = a.reshape(3, 4)          # 3 rows, 4 columns
c = a.reshape(2, 2, 3)       # 3D array

# Flatten
flat = b.flatten()            # Back to 1D

# Transpose
print(b.T)                    # Swap rows and columns

# Stack arrays
batch_a = np.array([85, 92, 78])
batch_b = np.array([90, 88, 95])

vertical = np.vstack([batch_a, batch_b])      # Stack vertically (2,3)
horizontal = np.hstack([batch_a, batch_b])    # Join side by side (6,)
print(vertical)
# [[85 92 78]
#  [90 88 95]]

# Concatenate
combined = np.concatenate([batch_a, batch_b])
print(combined)    # [85 92 78 90 88 95]

# Split
first, second = np.split(combined, 2)
print(first)     # [85 92 78]
```

---

## Random Module

```python
np.random.seed(42)    # For reproducible results

# Random integers
marks = np.random.randint(40, 100, size=10)
print(marks)    # [91 71 60 56 44 88 89 95 44 79]

# Random floats (0 to 1)
probs = np.random.random(5)

# Random choice
students = ["Rahul", "Priya", "Amit", "Sneha", "Vikram"]
selected = np.random.choice(students, size=3, replace=False)
print(f"Selected: {selected}")

# Normal distribution
heights = np.random.normal(loc=165, scale=10, size=1000)
print(f"Mean: {heights.mean():.1f}, Std: {heights.std():.1f}")

# Shuffle
arr = np.array([1, 2, 3, 4, 5])
np.random.shuffle(arr)
print(arr)    # [3 1 5 2 4] (random order)
```

---

## Useful Operations

```python
# Where — conditional replacement
marks = np.array([85, 42, 91, 58, 73])
result = np.where(marks >= 60, "Pass", "Fail")
print(result)    # ['Pass' 'Fail' 'Pass' 'Fail' 'Pass']

# Unique values
cities = np.array(["Bhopal", "Delhi", "Bhopal", "Pune", "Delhi"])
print(np.unique(cities))                          # ['Bhopal' 'Delhi' 'Pune']
values, counts = np.unique(cities, return_counts=True)
print(dict(zip(values, counts)))                  # {'Bhopal': 2, 'Delhi': 2, 'Pune': 1}

# Sort
marks = np.array([78, 92, 45, 88, 65])
print(np.sort(marks))              # [45 65 78 88 92]
print(np.argsort(marks))           # [2 4 0 3 1] — indices of sorted order

# Clip — limit values
marks = np.array([105, 92, -5, 78, 88])
clipped = np.clip(marks, 0, 100)
print(clipped)    # [100  92   0  78  88]
```

---

## Summary

| Concept | Syntax | Purpose |
|---------|--------|---------|
| Create | `np.array([1,2,3])` | Make an array |
| Zeros/Ones | `np.zeros(5)`, `np.ones(5)` | Pre-filled arrays |
| Range | `np.arange(0,10,2)` | Like range() but array |
| Indexing | `arr[0]`, `arr[1:3]` | Access elements |
| Boolean filter | `arr[arr > 5]` | Filter by condition |
| Stats | `.mean()`, `.std()`, `.max()` | Quick statistics |
| Broadcasting | `arr * [1, 2, 3]` | Operations on different shapes |
| Reshape | `.reshape(3, 4)` | Change array shape |
| Random | `np.random.randint()` | Generate random data |
| Where | `np.where(cond, a, b)` | Conditional values |

---

## Practice Tasks

1. Create a NumPy array of 10 student marks and calculate mean, median, and standard deviation
2. Create a 2D array (5 students x 3 subjects) and find the topper in each subject
3. Generate 1000 random heights (normal distribution) and find how many are above 180 cm
4. Use boolean indexing to filter all marks below 60 (failing marks)
5. Calculate weighted average marks using broadcasting
