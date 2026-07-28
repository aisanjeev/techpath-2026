"""
Python + SQLite Integration — Module 12 Code Snap
Run: python code-python-sqlite.py
No extra packages needed — sqlite3 is built into Python.
"""
import sqlite3
import os

DB_FILE = "school.db"


def create_database():
    """Create tables and insert sample data."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            course TEXT DEFAULT 'ADCA',
            marks INTEGER CHECK(marks >= 0 AND marks <= 100),
            city TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    students = [
        ("Rahul Sharma", "rahul@email.com", "ADCA", 85, "Bhopal"),
        ("Priya Patel", "priya@email.com", "DCA", 92, "Indore"),
        ("Amit Kumar", "amit@email.com", "ADCA", 67, "Delhi"),
        ("Sneha Gupta", "sneha@email.com", "ADCA", 78, "Bhopal"),
        ("Vikram Singh", "vikram@email.com", "DCA", 45, "Jaipur"),
        ("Ananya Reddy", "ananya@email.com", "ADCA", 95, "Hyderabad"),
        ("Karan Verma", "karan@email.com", "Tally", 58, "Bhopal"),
        ("Neha Joshi", "neha@email.com", "ADCA", 88, "Pune"),
    ]

    cursor.executemany(
        "INSERT OR IGNORE INTO students (name, email, course, marks, city) VALUES (?, ?, ?, ?, ?)",
        students
    )

    conn.commit()
    return conn


def query_all(conn):
    """Show all students."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, course, marks, city FROM students ORDER BY name")
    rows = cursor.fetchall()

    print(f"\n{'ID':<4} {'Name':<20} {'Course':<8} {'Marks':<8} {'City':<12}")
    print("-" * 55)
    for row in rows:
        print(f"{row[0]:<4} {row[1]:<20} {row[2]:<8} {row[3]:<8} {row[4]:<12}")
    print(f"\nTotal: {len(rows)} students")


def query_stats(conn):
    """Show aggregate statistics."""
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*), AVG(marks), MAX(marks), MIN(marks) FROM students")
    count, avg, max_m, min_m = cursor.fetchone()
    print(f"\n--- Statistics ---")
    print(f"  Total Students: {count}")
    print(f"  Average Marks:  {avg:.1f}")
    print(f"  Highest Marks:  {max_m}")
    print(f"  Lowest Marks:   {min_m}")

    cursor.execute("SELECT course, COUNT(*), ROUND(AVG(marks), 1) FROM students GROUP BY course")
    print(f"\n--- Course-wise ---")
    for course, cnt, avg in cursor.fetchall():
        print(f"  {course}: {cnt} students, avg {avg}")


def search_student(conn, query):
    """Search by name (using parameterized query)."""
    cursor = conn.cursor()
    cursor.execute("SELECT name, course, marks, city FROM students WHERE name LIKE ?", (f"%{query}%",))
    results = cursor.fetchall()

    if not results:
        print(f"No students matching '{query}'")
        return

    print(f"\nSearch results for '{query}':")
    for r in results:
        print(f"  {r[0]} | {r[1]} | {r[2]} marks | {r[3]}")


def add_student(conn, name, email, course, marks, city):
    """Add a new student."""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (name, email, course, marks, city) VALUES (?, ?, ?, ?, ?)",
            (name, email, course, marks, city)
        )
        conn.commit()
        print(f"Added: {name}")
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    conn = create_database()

    print("=" * 55)
    print("  PYTHON + SQLITE DEMO")
    print("=" * 55)

    query_all(conn)
    query_stats(conn)

    search_student(conn, "Rahul")

    print("\n--- Adding new student ---")
    add_student(conn, "Meera Nair", "meera@email.com", "ADCA", 82, "Kerala")

    query_all(conn)

    conn.close()
    print(f"\nDatabase saved: {DB_FILE}")
