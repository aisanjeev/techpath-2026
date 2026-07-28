# Matplotlib & Seaborn — Data Visualization

**Module 03 — Python Libraries: Data, Automation & APIs | Topic 3**

---

## Why Visualize Data?

Numbers in a table are hard to understand quickly. A chart tells the story at a glance.

```bash
pip install matplotlib seaborn
```

```python
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
```

---

## Matplotlib Basics

### Line Chart

```python
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
revenue = [45000, 52000, 48000, 61000, 58000, 72000]

plt.figure(figsize=(8, 5))
plt.plot(months, revenue, marker="o", color="#3498db", linewidth=2)
plt.title("TechPath Monthly Revenue — 2026")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("revenue.png", dpi=150)
plt.show()
```

### Bar Chart

```python
courses = ["Python FS", "Web Dev", "Data Science", "AI/ML"]
students = [45, 30, 25, 20]

plt.figure(figsize=(8, 5))
bars = plt.bar(courses, students, color=["#3498db", "#2ecc71", "#e74c3c", "#f39c12"])
plt.title("Students per Course — TechPath Institute")
plt.xlabel("Course")
plt.ylabel("Number of Students")

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             str(int(height)), ha='center', fontweight='bold')

plt.tight_layout()
plt.show()
```

### Horizontal Bar Chart

```python
cities = ["Bhopal", "Delhi", "Pune", "Mumbai", "Bangalore"]
count = [35, 28, 22, 18, 15]

plt.figure(figsize=(8, 5))
plt.barh(cities, count, color="#3498db")
plt.title("Students by City")
plt.xlabel("Number of Students")
plt.tight_layout()
plt.show()
```

### Scatter Plot

```python
study_hours = [2, 3, 5, 1, 7, 4, 6, 8, 3, 5]
marks = [45, 55, 78, 35, 92, 65, 85, 95, 50, 72]

plt.figure(figsize=(8, 5))
plt.scatter(study_hours, marks, c=marks, cmap="RdYlGn", s=100, edgecolors="black")
plt.colorbar(label="Marks")
plt.title("Study Hours vs Marks")
plt.xlabel("Study Hours per Day")
plt.ylabel("Marks Obtained")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

### Pie Chart

```python
courses = ["Python FS", "Web Dev", "Data Science", "AI/ML"]
students = [45, 30, 25, 20]
colors = ["#3498db", "#2ecc71", "#e74c3c", "#f39c12"]
explode = (0.05, 0, 0, 0)    # Slightly separate the first slice

plt.figure(figsize=(7, 7))
plt.pie(students, labels=courses, colors=colors, explode=explode,
        autopct="%1.1f%%", startangle=90, shadow=True)
plt.title("Course Distribution — TechPath Institute")
plt.tight_layout()
plt.show()
```

### Histogram

```python
marks = np.random.normal(70, 15, 200)    # 200 students, mean 70, std 15

plt.figure(figsize=(8, 5))
plt.hist(marks, bins=15, color="#3498db", edgecolor="black", alpha=0.7)
plt.axvline(marks.mean(), color="red", linestyle="--", label=f"Mean: {marks.mean():.1f}")
plt.title("Marks Distribution")
plt.xlabel("Marks")
plt.ylabel("Number of Students")
plt.legend()
plt.tight_layout()
plt.show()
```

---

## Subplots — Multiple Charts

```python
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Chart 1: Bar
axes[0].bar(["Python", "Web Dev", "DS"], [45, 30, 25], color="#3498db")
axes[0].set_title("Students per Course")

# Chart 2: Line
months = ["Jan", "Feb", "Mar", "Apr"]
axes[1].plot(months, [45, 52, 48, 61], marker="o", color="#2ecc71")
axes[1].set_title("Monthly Revenue")

# Chart 3: Pie
axes[2].pie([45, 30, 25], labels=["Python", "Web", "DS"], autopct="%1.0f%%")
axes[2].set_title("Distribution")

plt.suptitle("TechPath Dashboard", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()
```

---

## Seaborn — Beautiful Statistical Charts

Seaborn builds on Matplotlib and makes statistical visualizations easier and prettier.

```python
import seaborn as sns
sns.set_theme(style="whitegrid")    # Set the visual style
```

### Bar Plot with Seaborn

```python
df = pd.DataFrame({
    "course": ["Python", "Python", "Web Dev", "Web Dev", "DS", "DS"],
    "city": ["Bhopal", "Delhi", "Bhopal", "Delhi", "Bhopal", "Delhi"],
    "students": [25, 20, 18, 12, 15, 10],
})

plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="course", y="students", hue="city", palette="Set2")
plt.title("Students by Course & City")
plt.tight_layout()
plt.show()
```

### Heatmap

```python
# Correlation heatmap
data = pd.DataFrame({
    "Python": [85, 92, 78, 88, 65],
    "Django": [80, 90, 72, 85, 60],
    "React": [75, 88, 70, 82, 58],
    "SQL": [90, 85, 80, 88, 70],
})

plt.figure(figsize=(8, 6))
sns.heatmap(data.corr(), annot=True, cmap="coolwarm", center=0,
            fmt=".2f", linewidths=0.5)
plt.title("Subject Correlation Heatmap")
plt.tight_layout()
plt.show()
```

### Box Plot

```python
df = pd.DataFrame({
    "marks": [85, 92, 78, 88, 65, 45, 72, 90, 55, 82, 68, 95],
    "course": ["Python"]*4 + ["Web Dev"]*4 + ["DS"]*4,
})

plt.figure(figsize=(8, 5))
sns.boxplot(data=df, x="course", y="marks", palette="Set3")
plt.title("Marks Distribution by Course")
plt.tight_layout()
plt.show()
```

### Distribution Plot

```python
marks = np.random.normal(70, 12, 300)

plt.figure(figsize=(8, 5))
sns.histplot(marks, bins=20, kde=True, color="#3498db")
plt.title("Marks Distribution with KDE")
plt.xlabel("Marks")
plt.tight_layout()
plt.show()
```

### Pair Plot

```python
# Quick overview of relationships between all numeric columns
df = pd.DataFrame({
    "python_marks": np.random.randint(40, 100, 50),
    "django_marks": np.random.randint(40, 100, 50),
    "react_marks": np.random.randint(40, 100, 50),
    "study_hours": np.random.randint(1, 10, 50),
})

sns.pairplot(df, corner=True)
plt.suptitle("Subject Correlation", y=1.02)
plt.show()
```

---

## Customization Tips

```python
# Figure size
plt.figure(figsize=(10, 6))

# Colors
# Named: "red", "blue", "green"
# Hex: "#3498db", "#e74c3c"
# Palettes: "Set2", "viridis", "coolwarm"

# Axis labels and title
plt.title("Title", fontsize=14, fontweight="bold")
plt.xlabel("X Label", fontsize=12)
plt.ylabel("Y Label", fontsize=12)

# Grid
plt.grid(True, alpha=0.3)

# Legend
plt.legend(loc="upper right")

# Rotate x-axis labels
plt.xticks(rotation=45)

# Save
plt.savefig("chart.png", dpi=150, bbox_inches="tight")
```

---

## Summary

| Chart Type | Use When | Library |
|------------|----------|---------|
| Line | Trends over time | matplotlib |
| Bar | Compare categories | matplotlib / seaborn |
| Scatter | Relationship between 2 variables | matplotlib |
| Pie | Parts of a whole | matplotlib |
| Histogram | Distribution of values | matplotlib / seaborn |
| Heatmap | Correlation between variables | seaborn |
| Box plot | Spread and outliers | seaborn |

---

## Practice Tasks

1. Create a bar chart comparing student enrollment across 5 courses
2. Create a line chart showing monthly revenue with markers and grid
3. Create a pie chart showing course distribution
4. Create a heatmap showing correlation between subject marks
5. Create a dashboard with 4 subplots (bar, line, scatter, pie) using subplots
