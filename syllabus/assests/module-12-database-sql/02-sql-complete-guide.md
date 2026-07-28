# SQL — Complete Beginner Guide

**Module 12 — Database Design & SQL | Topic 2**

---

## What is SQL?

**SQL** = Structured Query Language — the language used to talk to relational databases.

```
You: "Show me all students who scored above 80"
SQL: SELECT * FROM students WHERE marks > 80;
```

---

## Creating a Database and Table

```sql
-- Create database
CREATE DATABASE school_db;
USE school_db;

-- Create students table
CREATE TABLE students (
    student_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    age INT,
    email VARCHAR(150) UNIQUE,
    course VARCHAR(50) DEFAULT 'ADCA',
    marks DECIMAL(5,2),
    enrolled_date DATE,
    is_active BOOLEAN DEFAULT TRUE
);
```

### Column Constraints

| Constraint | What It Does |
|-----------|-------------|
| `PRIMARY KEY` | Unique identifier, can't be NULL |
| `NOT NULL` | Must have a value |
| `UNIQUE` | No duplicates allowed |
| `DEFAULT value` | Default value if none given |
| `AUTO_INCREMENT` | Auto-generates numbers (1, 2, 3...) |
| `FOREIGN KEY` | Links to another table |
| `CHECK` | Validates data (e.g., age > 0) |

---

## INSERT — Adding Data

```sql
-- Insert single row
INSERT INTO students (name, age, email, marks, enrolled_date)
VALUES ('Rahul', 20, 'rahul@email.com', 85.5, '2026-01-15');

-- Insert multiple rows
INSERT INTO students (name, age, email, marks, enrolled_date)
VALUES
    ('Priya', 22, 'priya@email.com', 92.0, '2026-01-15'),
    ('Amit', 21, 'amit@email.com', 78.3, '2026-02-01'),
    ('Sneha', 23, 'sneha@email.com', 95.7, '2026-01-15'),
    ('Karan', 20, 'karan@email.com', 88.0, '2026-02-01');
```

---

## SELECT — Reading Data

```sql
-- All columns, all rows
SELECT * FROM students;

-- Specific columns
SELECT name, marks FROM students;

-- With condition
SELECT * FROM students WHERE marks > 80;

-- Multiple conditions
SELECT * FROM students WHERE age >= 20 AND marks > 85;
SELECT * FROM students WHERE course = 'ADCA' OR course = 'BCA';

-- Sort results
SELECT * FROM students ORDER BY marks DESC;        -- Highest first
SELECT * FROM students ORDER BY name ASC;           -- A to Z

-- Limit results
SELECT * FROM students LIMIT 5;                     -- First 5 rows
SELECT * FROM students ORDER BY marks DESC LIMIT 3; -- Top 3

-- Distinct (unique values only)
SELECT DISTINCT course FROM students;

-- Like (pattern matching)
SELECT * FROM students WHERE name LIKE 'R%';    -- Starts with R
SELECT * FROM students WHERE email LIKE '%@gmail%'; -- Contains gmail

-- IN (multiple values)
SELECT * FROM students WHERE age IN (20, 21, 22);

-- BETWEEN (range)
SELECT * FROM students WHERE marks BETWEEN 80 AND 90;

-- IS NULL
SELECT * FROM students WHERE email IS NULL;
```

---

## UPDATE — Modifying Data

```sql
-- Update one row
UPDATE students SET marks = 90.0 WHERE student_id = 1;

-- Update multiple columns
UPDATE students SET age = 21, course = 'BCA' WHERE name = 'Rahul';

-- Update many rows
UPDATE students SET is_active = FALSE WHERE marks < 40;
```

> **Always use WHERE!** Without it, ALL rows get updated.

---

## DELETE — Removing Data

```sql
-- Delete specific rows
DELETE FROM students WHERE student_id = 3;

-- Delete with condition
DELETE FROM students WHERE marks < 30 AND is_active = FALSE;

-- Delete ALL rows (careful!)
DELETE FROM students;

-- Drop entire table
DROP TABLE students;
```

> **Always use WHERE with DELETE!** Without it, ALL rows get deleted.

---

## Aggregate Functions

| Function | What It Does | Example |
|----------|-------------|---------|
| `COUNT()` | Count rows | `SELECT COUNT(*) FROM students;` |
| `SUM()` | Add up values | `SELECT SUM(marks) FROM students;` |
| `AVG()` | Average | `SELECT AVG(marks) FROM students;` |
| `MAX()` | Highest value | `SELECT MAX(marks) FROM students;` |
| `MIN()` | Lowest value | `SELECT MIN(marks) FROM students;` |

```sql
-- Combined example
SELECT
    COUNT(*) AS total_students,
    AVG(marks) AS average_marks,
    MAX(marks) AS highest_marks,
    MIN(marks) AS lowest_marks
FROM students;
```

---

## GROUP BY — Statistics by Category

```sql
-- Average marks per course
SELECT course, AVG(marks) AS avg_marks
FROM students
GROUP BY course;

-- Count students per course
SELECT course, COUNT(*) AS student_count
FROM students
GROUP BY course;

-- Filter groups with HAVING
SELECT course, AVG(marks) AS avg_marks
FROM students
GROUP BY course
HAVING AVG(marks) > 80;
```

> **WHERE** filters rows BEFORE grouping. **HAVING** filters groups AFTER grouping.

---

## JOINs — Combining Tables

```sql
-- Create courses table
CREATE TABLE courses (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(50),
    fee DECIMAL(10,2)
);

-- INNER JOIN (only matching rows)
SELECT s.name, s.marks, c.course_name, c.fee
FROM students s
INNER JOIN courses c ON s.course_id = c.course_id;

-- LEFT JOIN (all from left + matching from right)
SELECT s.name, c.course_name
FROM students s
LEFT JOIN courses c ON s.course_id = c.course_id;
```

| Join Type | What It Returns |
|-----------|----------------|
| `INNER JOIN` | Only rows that match in BOTH tables |
| `LEFT JOIN` | All from left table + matches from right |
| `RIGHT JOIN` | All from right table + matches from left |
| `FULL JOIN` | All rows from both tables |

---

## Aliases & Subqueries

```sql
-- Aliases (short names)
SELECT s.name AS student_name, s.marks AS score
FROM students AS s
WHERE s.marks > 80;

-- Subquery (query inside query)
SELECT name, marks
FROM students
WHERE marks > (SELECT AVG(marks) FROM students);
-- Returns students above average
```

---

## ALTER TABLE — Modifying Structure

```sql
-- Add column
ALTER TABLE students ADD phone VARCHAR(15);

-- Remove column
ALTER TABLE students DROP COLUMN phone;

-- Rename column
ALTER TABLE students RENAME COLUMN marks TO score;

-- Change data type
ALTER TABLE students MODIFY age SMALLINT;
```

---

## Indexes — Speed Up Queries

```sql
-- Create index
CREATE INDEX idx_name ON students(name);

-- Unique index
CREATE UNIQUE INDEX idx_email ON students(email);

-- Drop index
DROP INDEX idx_name ON students;
```

> **Use indexes on columns you search/filter often.** Don't over-index — it slows down INSERT/UPDATE.

---

## Summary

- **SQL** = language to talk to relational databases
- **CRUD:** INSERT, SELECT, UPDATE, DELETE
- **SELECT** is the most used command — learn its clauses well
- **WHERE** filters rows, **HAVING** filters groups
- **JOIN** combines data from multiple tables
- **GROUP BY** + aggregate functions for statistics
- **Always use WHERE** with UPDATE and DELETE
- Practice with **SQLite** (no installation needed) or **MySQL**
