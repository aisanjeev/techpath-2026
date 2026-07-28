"""
TechPath Institute — Python Libraries: Pandas Data Analysis
==============================================================
Covers NumPy basics, Pandas DataFrames, data filtering, groupby,
merge, pivot tables, and Matplotlib/Seaborn visualization.

Requirements:
    pip install numpy pandas matplotlib seaborn

Run this file:  python code-pandas-data-analysis.py
"""

import numpy as np
import pandas as pd

# We import matplotlib but save figures to files instead of showing them
# (so this script runs without a display/GUI)
try:
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False
    print("Note: matplotlib/seaborn not installed — skipping chart generation")


# ──────────────────────────────────────────────
# 1. NUMPY BASICS
# ──────────────────────────────────────────────

print("=" * 60)
print("1. NUMPY BASICS")
print("=" * 60)

# Creating arrays
marks = np.array([85, 92, 78, 88, 95, 72, 68, 81, 90, 76])
print(f"Marks: {marks}")
print(f"Type: {marks.dtype}")
print(f"Shape: {marks.shape}")

# Vectorized operations (no loops needed!)
print(f"\nScaled marks (+5): {marks + 5}")
print(f"Percentage (/100): {marks / 100}")
print(f"Above 80: {marks[marks > 80]}")

# Statistics
print(f"\nMean: {marks.mean():.1f}")
print(f"Median: {np.median(marks):.1f}")
print(f"Std Dev: {marks.std():.1f}")
print(f"Min: {marks.min()}, Max: {marks.max()}")
print(f"Sum: {marks.sum()}")

# 2D array — student marks matrix
student_marks = np.array([
    [85, 92, 78],   # Rahul:  Python, Web, DBMS
    [90, 88, 95],   # Priya:  Python, Web, DBMS
    [72, 68, 75],   # Amit:   Python, Web, DBMS
    [88, 91, 82],   # Sneha:  Python, Web, DBMS
    [95, 85, 90],   # Vikram: Python, Web, DBMS
])
print(f"\nStudent marks matrix (5 students x 3 subjects):")
print(student_marks)
print(f"Per-student average: {student_marks.mean(axis=1)}")  # Row-wise
print(f"Per-subject average: {student_marks.mean(axis=0)}")  # Column-wise

# Random data generation
np.random.seed(42)
random_fees = np.random.randint(15000, 35000, size=20)
print(f"\nRandom fees (20 students): Mean=₹{random_fees.mean():,.0f}, Std=₹{random_fees.std():,.0f}")


# ──────────────────────────────────────────────
# 2. PANDAS — CREATING DATAFRAMES
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("2. PANDAS — CREATING DATAFRAMES")
print("=" * 60)

# Create a DataFrame from a dictionary
students = pd.DataFrame({
    "Name": ["Rahul Sharma", "Priya Patel", "Amit Kumar", "Sneha Gupta",
             "Vikram Singh", "Ananya Verma", "Deepak Yadav", "Kavita Joshi",
             "Neha Rawat", "Ravi Mishra"],
    "City": ["Bhopal", "Pune", "Delhi", "Mumbai", "Jaipur",
             "Bhopal", "Delhi", "Pune", "Mumbai", "Bhopal"],
    "Course": ["Python", "Python", "Data Science", "Web Dev", "Python",
               "Data Science", "Web Dev", "Python", "Data Science", "Web Dev"],
    "Fee": [25000, 25000, 30000, 20000, 25000,
            30000, 20000, 25000, 30000, 20000],
    "Marks": [85, 92, 78, 88, 72, 95, 65, 81, 70, 58],
})

print(students)
print(f"\nShape: {students.shape} (rows, columns)")
print(f"\nData types:\n{students.dtypes}")
print(f"\nFirst 3 rows:\n{students.head(3)}")
print(f"\nStatistical summary:\n{students.describe()}")


# ──────────────────────────────────────────────
# 3. FILTERING & SELECTING DATA
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("3. FILTERING & SELECTING DATA")
print("=" * 60)

# Select specific columns
names_and_marks = students[["Name", "Marks"]]
print("Names and Marks:")
print(names_and_marks)

# Filter rows
high_scorers = students[students["Marks"] >= 85]
print(f"\nHigh scorers (>= 85 marks):\n{high_scorers[['Name', 'Marks']]}")

python_students = students[students["Course"] == "Python"]
print(f"\nPython course students:\n{python_students[['Name', 'City']]}")

# Multiple conditions
bhopal_high = students[(students["City"] == "Bhopal") & (students["Marks"] >= 80)]
print(f"\nBhopal students with marks >= 80:\n{bhopal_high[['Name', 'Marks']]}")

# Using isin
metro_students = students[students["City"].isin(["Mumbai", "Delhi", "Pune"])]
print(f"\nMetro city students: {metro_students['Name'].tolist()}")


# ──────────────────────────────────────────────
# 4. ADDING & TRANSFORMING COLUMNS
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("4. ADDING & TRANSFORMING COLUMNS")
print("=" * 60)

# Add calculated columns
students["Fee_GST"] = (students["Fee"] * 1.18).round(0).astype(int)
students["Grade"] = students["Marks"].apply(
    lambda m: "A+" if m >= 90 else "A" if m >= 80 else "B" if m >= 70 else "C" if m >= 60 else "Fail"
)
students["Pass"] = students["Marks"] >= 40

print(students[["Name", "Marks", "Grade", "Fee", "Fee_GST"]])

# Value counts
print(f"\nGrade distribution:\n{students['Grade'].value_counts()}")
print(f"\nCity distribution:\n{students['City'].value_counts()}")


# ──────────────────────────────────────────────
# 5. GROUPBY — AGGREGATION
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("5. GROUPBY — AGGREGATION")
print("=" * 60)

# Group by Course
course_stats = students.groupby("Course").agg(
    Students=("Name", "count"),
    Avg_Marks=("Marks", "mean"),
    Max_Marks=("Marks", "max"),
    Total_Fee=("Fee", "sum"),
).round(1)
print("Course-wise statistics:")
print(course_stats)

# Group by City
city_stats = students.groupby("City").agg(
    Count=("Name", "count"),
    Avg_Marks=("Marks", "mean"),
    Total_Fee=("Fee", "sum"),
).round(1)
print(f"\nCity-wise statistics:\n{city_stats}")

# Group by multiple columns
multi_group = students.groupby(["City", "Course"]).agg(
    Count=("Name", "count"),
    Avg_Fee=("Fee", "mean"),
).round(0)
print(f"\nCity + Course breakdown:\n{multi_group}")


# ──────────────────────────────────────────────
# 6. MERGE (JOIN) DATAFRAMES
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("6. MERGE (JOIN) DATAFRAMES")
print("=" * 60)

# Additional student info
contact_info = pd.DataFrame({
    "Name": ["Rahul Sharma", "Priya Patel", "Amit Kumar", "Sneha Gupta", "Vikram Singh"],
    "Email": ["rahul@mail.com", "priya@mail.com", "amit@mail.com", "sneha@mail.com", "vikram@mail.com"],
    "Phone": ["9876543210", "8765432109", "7654321098", "6543210987", "9876501234"],
})

# Left join — keep all students, add contact info where available
merged = pd.merge(students, contact_info, on="Name", how="left")
print("Merged data (first 5):")
print(merged[["Name", "City", "Email", "Phone"]].head())

# Show students without contact info
no_contact = merged[merged["Email"].isna()]
print(f"\nStudents without contact info: {no_contact['Name'].tolist()}")


# ──────────────────────────────────────────────
# 7. PIVOT TABLES
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("7. PIVOT TABLES")
print("=" * 60)

# Fee by City and Course
fee_pivot = students.pivot_table(
    values="Fee",
    index="City",
    columns="Course",
    aggfunc="sum",
    fill_value=0,
    margins=True,  # Add totals
)
print("Fee pivot table (City x Course):")
print(fee_pivot)

# Student count by City and Grade
count_pivot = students.pivot_table(
    values="Name",
    index="City",
    columns="Grade",
    aggfunc="count",
    fill_value=0,
)
print(f"\nStudent count by City and Grade:\n{count_pivot}")


# ──────────────────────────────────────────────
# 8. SORTING & RANKING
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("8. SORTING & RANKING")
print("=" * 60)

# Sort by marks (descending)
ranked = students.sort_values("Marks", ascending=False).reset_index(drop=True)
ranked.index += 1  # Start rank from 1
ranked["Rank"] = range(1, len(ranked) + 1)
print("Student Rankings:")
print(ranked[["Rank", "Name", "City", "Course", "Marks", "Grade"]])


# ──────────────────────────────────────────────
# 9. SAVING DATA
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("9. SAVING DATA")
print("=" * 60)

# Save to CSV
students.to_csv("techpath_analysis.csv", index=False)
print("Saved to techpath_analysis.csv")

# Save to JSON
students.to_json("techpath_analysis.json", orient="records", indent=2, force_ascii=False)
print("Saved to techpath_analysis.json")


# ──────────────────────────────────────────────
# 10. MATPLOTLIB & SEABORN CHARTS
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("10. CHARTS (saved as PNG files)")
print("=" * 60)

if HAS_PLOT:
    sns.set_style("whitegrid")

    # Bar chart — Course-wise enrollment
    fig, ax = plt.subplots(figsize=(8, 5))
    course_counts = students["Course"].value_counts()
    bars = ax.bar(course_counts.index, course_counts.values,
                  color=["#2196F3", "#4CAF50", "#FF9800"])
    ax.set_title("TechPath Institute — Course-wise Enrollment", fontsize=14)
    ax.set_xlabel("Course")
    ax.set_ylabel("Number of Students")
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
                str(int(bar.get_height())), ha="center", fontweight="bold")
    plt.tight_layout()
    plt.savefig("chart_enrollment.png", dpi=150)
    print("Saved: chart_enrollment.png")
    plt.close()

    # Scatter plot — Fee vs Marks
    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {"Python": "#2196F3", "Data Science": "#FF9800", "Web Dev": "#4CAF50"}
    for course in students["Course"].unique():
        subset = students[students["Course"] == course]
        ax.scatter(subset["Fee"], subset["Marks"], label=course,
                   color=colors.get(course, "#999"), s=100, alpha=0.7)
    ax.set_title("Fee vs Marks by Course")
    ax.set_xlabel("Fee (₹)")
    ax.set_ylabel("Marks")
    ax.legend()
    plt.tight_layout()
    plt.savefig("chart_fee_vs_marks.png", dpi=150)
    print("Saved: chart_fee_vs_marks.png")
    plt.close()

    # Heatmap — City x Course student count
    fig, ax = plt.subplots(figsize=(7, 5))
    heatmap_data = students.pivot_table(values="Name", index="City",
                                        columns="Course", aggfunc="count", fill_value=0)
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlOrRd",
                linewidths=0.5, ax=ax)
    ax.set_title("Students per City & Course")
    plt.tight_layout()
    plt.savefig("chart_heatmap.png", dpi=150)
    print("Saved: chart_heatmap.png")
    plt.close()

    # Pie chart — Grade distribution
    fig, ax = plt.subplots(figsize=(7, 7))
    grade_counts = students["Grade"].value_counts()
    ax.pie(grade_counts, labels=grade_counts.index, autopct="%1.0f%%",
           colors=["#4CAF50", "#2196F3", "#FF9800", "#F44336", "#9E9E9E"],
           startangle=90)
    ax.set_title("Grade Distribution")
    plt.tight_layout()
    plt.savefig("chart_grades.png", dpi=150)
    print("Saved: chart_grades.png")
    plt.close()
else:
    print("Skipping charts — install matplotlib and seaborn to generate them")


# ──────────────────────────────────────────────
# SUMMARY
# ──────────────────────────────────────────────

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Total students: {len(students)}")
print(f"Total fee collected: ₹{students['Fee'].sum():,}")
print(f"Average marks: {students['Marks'].mean():.1f}")
print(f"Topper: {students.loc[students['Marks'].idxmax(), 'Name']} ({students['Marks'].max()} marks)")
print(f"Cities represented: {students['City'].nunique()}")
print(f"Courses offered: {students['Course'].nunique()}")

# Clean up generated files
import os
for f in ["techpath_analysis.csv", "techpath_analysis.json",
          "chart_enrollment.png", "chart_fee_vs_marks.png",
          "chart_heatmap.png", "chart_grades.png"]:
    if os.path.exists(f):
        os.remove(f)

print("\nCleaned up generated files.")
print("\n" + "=" * 60)
print("Program complete! You have mastered Pandas data analysis.")
print("=" * 60)
