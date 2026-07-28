"""
Student Management System — Module 10 Code Snap
Run: python code-student-manager.py
"""
import json
import os

DATA_FILE = "students.json"


def load_students():
    """Load students from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []


def save_students(students):
    """Save students to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(students, f, indent=2)


def add_student(students):
    """Add a new student."""
    print("\n--- Add Student ---")
    name = input("Name: ").strip()
    roll = input("Roll Number: ").strip()

    if any(s["roll"] == roll for s in students):
        print(f"Error: Roll number {roll} already exists!")
        return

    course = input("Course (ADCA/DCA/Tally): ").strip().upper()
    subjects = ["Hindi", "English", "Maths", "Science", "Computer"]
    marks = {}

    for sub in subjects:
        while True:
            try:
                m = int(input(f"  {sub} marks (0-100): "))
                if 0 <= m <= 100:
                    marks[sub] = m
                    break
                print("  Marks must be between 0 and 100")
            except ValueError:
                print("  Please enter a valid number")

    student = {
        "name": name,
        "roll": roll,
        "course": course,
        "marks": marks,
    }
    students.append(student)
    save_students(students)
    print(f"Student {name} added successfully!")


def calculate_result(marks):
    """Calculate total, percentage, and grade."""
    total = sum(marks.values())
    percentage = total / len(marks)
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 75:
        grade = "A"
    elif percentage >= 60:
        grade = "B"
    elif percentage >= 45:
        grade = "C"
    elif percentage >= 33:
        grade = "D"
    else:
        grade = "F"
    return total, percentage, grade


def view_all(students):
    """Display all students in a table."""
    if not students:
        print("\nNo students found.")
        return

    print(f"\n{'Roll':<8} {'Name':<20} {'Course':<8} {'Total':<8} {'%':<8} {'Grade':<6}")
    print("-" * 60)

    for s in students:
        total, pct, grade = calculate_result(s["marks"])
        print(f"{s['roll']:<8} {s['name']:<20} {s['course']:<8} {total:<8} {pct:<8.1f} {grade:<6}")

    print(f"\nTotal students: {len(students)}")


def search_student(students):
    """Search by name or roll number."""
    query = input("\nSearch (name or roll): ").strip().lower()
    found = [
        s for s in students
        if query in s["name"].lower() or query == s["roll"].lower()
    ]

    if not found:
        print("No matching students found.")
        return

    for s in found:
        total, pct, grade = calculate_result(s["marks"])
        print(f"\n  Name: {s['name']}")
        print(f"  Roll: {s['roll']}")
        print(f"  Course: {s['course']}")
        for sub, m in s["marks"].items():
            status = "Pass" if m >= 33 else "FAIL"
            print(f"    {sub}: {m}/100 [{status}]")
        print(f"  Total: {total}/{len(s['marks'])*100} | {pct:.1f}% | Grade: {grade}")


def delete_student(students):
    """Delete by roll number."""
    roll = input("\nRoll number to delete: ").strip()
    for i, s in enumerate(students):
        if s["roll"] == roll:
            confirm = input(f"Delete {s['name']} ({roll})? (y/n): ")
            if confirm.lower() == "y":
                students.pop(i)
                save_students(students)
                print("Deleted.")
            return
    print("Student not found.")


def main():
    students = load_students()
    print("=== Student Management System ===")

    while True:
        print("\n1. Add Student")
        print("2. View All")
        print("3. Search")
        print("4. Delete")
        print("5. Exit")

        choice = input("\nChoice (1-5): ").strip()

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_all(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            delete_student(students)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
