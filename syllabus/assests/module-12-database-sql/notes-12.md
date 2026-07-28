# Module 12 — Database & SQL — Quick Revision Notes

---

## Database Basics
- **Database** = organized collection of data stored electronically
- **RDBMS** = Relational Database Management System (tables with rows & columns)
- **SQL** = Structured Query Language (the language to talk to databases)
- Popular RDBMS: MySQL, PostgreSQL, SQLite, SQL Server, Oracle

## Key Concepts
| Term | Meaning |
|------|---------|
| Table | Collection of related data (like Excel sheet) |
| Row/Record | One entry (one student, one order) |
| Column/Field | One attribute (name, age, email) |
| Primary Key | Unique identifier for each row (id) |
| Foreign Key | Links to another table's primary key |
| Schema | Structure/design of the database |
| Index | Speeds up searching (like a book's index) |

## Data Types
| Type | Use | Example |
|------|-----|---------|
| `INTEGER` | Whole numbers | id, age, quantity |
| `TEXT`/`VARCHAR` | Strings | name, email, city |
| `REAL`/`FLOAT` | Decimals | price, percentage |
| `BOOLEAN` | True/False | is_active, is_paid |
| `DATE` | Dates | birth_date, created_at |
| `DATETIME` | Date + Time | order_time |

## CRUD Operations

### CREATE
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    course TEXT DEFAULT 'ADCA',
    marks INTEGER CHECK(marks >= 0 AND marks <= 100),
    city TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### INSERT
```sql
INSERT INTO students (name, email, course, marks, city)
VALUES ('Rahul Sharma', 'rahul@email.com', 'ADCA', 85, 'Bhopal');

-- Multiple rows
INSERT INTO students (name, email, course, marks, city) VALUES
    ('Priya Patel', 'priya@email.com', 'DCA', 92, 'Indore'),
    ('Amit Kumar', 'amit@email.com', 'ADCA', 67, 'Delhi');
```

### SELECT (Read)
```sql
SELECT * FROM students;                     -- all columns
SELECT name, marks FROM students;           -- specific columns
SELECT * FROM students WHERE course = 'ADCA';
SELECT * FROM students WHERE marks >= 60 AND city = 'Bhopal';
SELECT * FROM students WHERE city IN ('Bhopal', 'Indore', 'Delhi');
SELECT * FROM students WHERE name LIKE 'R%';  -- starts with R
SELECT * FROM students ORDER BY marks DESC;
SELECT * FROM students LIMIT 5;
SELECT DISTINCT city FROM students;
```

### UPDATE
```sql
UPDATE students SET marks = 90 WHERE id = 1;
UPDATE students SET course = 'DCA', city = 'Mumbai' WHERE name = 'Amit Kumar';
```

### DELETE
```sql
DELETE FROM students WHERE id = 5;
DELETE FROM students WHERE marks < 33;
```

## Aggregate Functions
```sql
SELECT COUNT(*) FROM students;                    -- total rows
SELECT AVG(marks) FROM students;                  -- average
SELECT SUM(marks) FROM students;                  -- total
SELECT MAX(marks), MIN(marks) FROM students;      -- highest, lowest
SELECT course, COUNT(*) AS total, AVG(marks) AS avg_marks
    FROM students GROUP BY course;
SELECT city, COUNT(*) FROM students
    GROUP BY city HAVING COUNT(*) > 2;            -- filter groups
```

## JOINs
```sql
-- INNER JOIN: only matching rows
SELECT s.name, c.course_name
FROM students s
INNER JOIN courses c ON s.course_id = c.id;

-- LEFT JOIN: all from left + matching from right
SELECT s.name, e.amount
FROM students s
LEFT JOIN enrollments e ON s.id = e.student_id;
```

## Subqueries
```sql
-- Students with above-average marks
SELECT name, marks FROM students
WHERE marks > (SELECT AVG(marks) FROM students);

-- Topper from each course
SELECT * FROM students s
WHERE marks = (SELECT MAX(marks) FROM students WHERE course = s.course);
```

## SQLite with Python
```python
import sqlite3

conn = sqlite3.connect("school.db")
cursor = conn.cursor()

# Create table
cursor.execute("CREATE TABLE IF NOT EXISTS students (...)")

# Insert
cursor.execute("INSERT INTO students (name, marks) VALUES (?, ?)", ("Rahul", 85))

# Select
cursor.execute("SELECT * FROM students WHERE marks > ?", (60,))
rows = cursor.fetchall()

conn.commit()
conn.close()
```

## Constraints Summary
| Constraint | Rule |
|-----------|------|
| `PRIMARY KEY` | Unique + NOT NULL identifier |
| `NOT NULL` | Cannot be empty |
| `UNIQUE` | No duplicates allowed |
| `DEFAULT` | Auto-fill if not provided |
| `CHECK` | Must satisfy condition |
| `FOREIGN KEY` | Must exist in referenced table |
