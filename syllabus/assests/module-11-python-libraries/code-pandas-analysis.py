"""
Pandas Data Analysis — Module 11 Code Snap
Run: pip install pandas matplotlib seaborn
     python code-pandas-analysis.py
Creates a sample dataset and performs analysis with charts.
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Create Sample Data ---
data = {
    "name": ["Rahul", "Priya", "Amit", "Sneha", "Vikram", "Ananya", "Karan", "Neha", "Rohit", "Divya",
             "Arjun", "Kavita", "Suresh", "Meera", "Deepak"],
    "course": ["ADCA", "DCA", "ADCA", "ADCA", "DCA", "ADCA", "Tally", "ADCA", "DCA", "ADCA",
               "Tally", "ADCA", "DCA", "ADCA", "Tally"],
    "hindi": [78, 85, 45, 92, 38, 95, 52, 88, 70, 65, 48, 90, 55, 82, 40],
    "english": [82, 90, 50, 88, 42, 98, 60, 75, 68, 72, 55, 85, 62, 78, 45],
    "maths": [70, 88, 35, 85, 30, 92, 48, 80, 60, 68, 42, 78, 58, 90, 38],
    "science": [75, 82, 40, 90, 35, 96, 55, 82, 65, 70, 50, 88, 60, 85, 42],
    "computer": [88, 95, 60, 94, 45, 99, 65, 90, 72, 80, 58, 92, 68, 88, 50],
    "city": ["Bhopal", "Indore", "Delhi", "Bhopal", "Jaipur", "Hyderabad", "Bhopal", "Pune",
             "Delhi", "Mumbai", "Jaipur", "Indore", "Chennai", "Bhopal", "Delhi"],
}

df = pd.DataFrame(data)

# --- Calculate Results ---
subjects = ["hindi", "english", "maths", "science", "computer"]
df["total"] = df[subjects].sum(axis=1)
df["percentage"] = df["total"] / 5
df["grade"] = df["percentage"].apply(
    lambda p: "A+" if p >= 90 else "A" if p >= 75 else "B" if p >= 60 else "C" if p >= 45 else "F"
)
df["status"] = df["percentage"].apply(lambda p: "Pass" if p >= 33 else "Fail")

# --- Print Summary ---
print("=" * 60)
print("STUDENT PERFORMANCE REPORT")
print("=" * 60)
print(f"\nTotal Students: {len(df)}")
print(f"Passed: {len(df[df['status'] == 'Pass'])} | Failed: {len(df[df['status'] == 'Fail'])}")
print(f"\nClass Average: {df['percentage'].mean():.1f}%")
print(f"Topper: {df.loc[df['percentage'].idxmax(), 'name']} ({df['percentage'].max():.1f}%)")

print("\n--- Top 5 Students ---")
top5 = df.nlargest(5, "percentage")[["name", "course", "total", "percentage", "grade"]]
print(top5.to_string(index=False))

print("\n--- Subject Averages ---")
for sub in subjects:
    avg = df[sub].mean()
    print(f"  {sub.capitalize():<10}: {avg:.1f}")

print("\n--- Course-wise Stats ---")
course_stats = df.groupby("course").agg(
    students=("name", "count"),
    avg_marks=("percentage", "mean"),
    topper=("percentage", "max"),
).round(1)
print(course_stats.to_string())

# --- Charts ---
os.makedirs("charts", exist_ok=True)

# Chart 1: Subject averages
fig, ax = plt.subplots(figsize=(8, 5))
avgs = [df[s].mean() for s in subjects]
colors = ["#ef4444", "#f59e0b", "#3b82f6", "#10b981", "#6366f1"]
ax.bar([s.capitalize() for s in subjects], avgs, color=colors)
ax.set_title("Average Marks by Subject", fontsize=14, fontweight="bold")
ax.set_ylabel("Average Marks")
for i, v in enumerate(avgs):
    ax.text(i, v + 1, f"{v:.1f}", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig("charts/subject_averages.png", dpi=150)
print("\nSaved: charts/subject_averages.png")

# Chart 2: Grade distribution (pie)
fig, ax = plt.subplots(figsize=(6, 6))
grade_counts = df["grade"].value_counts()
ax.pie(grade_counts.values, labels=grade_counts.index, autopct="%1.0f%%",
       colors=["#10b981", "#3b82f6", "#f59e0b", "#ef4444", "#94a3b8"])
ax.set_title("Grade Distribution", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/grade_distribution.png", dpi=150)
print("Saved: charts/grade_distribution.png")

# Chart 3: Top 5 students (horizontal bar)
fig, ax = plt.subplots(figsize=(8, 4))
top5_sorted = top5.sort_values("percentage")
ax.barh(top5_sorted["name"], top5_sorted["percentage"], color="#6366f1")
ax.set_xlabel("Percentage")
ax.set_title("Top 5 Students", fontsize=14, fontweight="bold")
for i, v in enumerate(top5_sorted["percentage"]):
    ax.text(v + 0.5, i, f"{v:.1f}%", va="center", fontweight="bold")
plt.tight_layout()
plt.savefig("charts/top_students.png", dpi=150)
print("Saved: charts/top_students.png")

print("\nDone! Check the 'charts' folder for PNG files.")
