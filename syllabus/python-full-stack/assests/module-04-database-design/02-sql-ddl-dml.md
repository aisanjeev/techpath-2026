# SQL DDL & DML — Creating and Modifying Data

**Module 04 — Database Design, SQL & NoSQL | Topic 2**

---

## What is SQL?

SQL (Structured Query Language) is the standard language for communicating with relational databases. Every database — PostgreSQL, MySQL, SQLite — understands SQL.

SQL is divided into sub-languages:

| Category | Full Form | Purpose | Key Commands |
|----------|-----------|---------|--------------|
| **DDL** | Data Definition Language | Define structure (tables, columns) | CREATE, ALTER, DROP, TRUNCATE |
| **DML** | Data Manipulation Language | Work with data (rows) | INSERT, UPDATE, DELETE |
| **DQL** | Data Query Language | Read data | SELECT |
| **DCL** | Data Control Language | Permissions | GRANT, REVOKE |
| **TCL** | Transaction Control Language | Transaction management | COMMIT, ROLLBACK, SAVEPOINT |

This topic covers **DDL** (building the structure) and **DML** (adding/changing/removing data).

---

## DDL — Data Definition Language

DDL commands create, modify, and delete database structures.

### CREATE TABLE

Creates a new table with columns, data types, and constraints.

```sql
CREATE TABLE students (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) UNIQUE NOT NULL,
    phone       VARCHAR(15),
    city        VARCHAR(50) DEFAULT 'Bhopal',
    fee_paid    DECIMAL(10, 2) DEFAULT 0.00,
    is_active   BOOLEAN DEFAULT TRUE,
    joined_on   DATE DEFAULT CURRENT_DATE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Common Data Types

| Data Type | Use Case | Example |
|-----------|----------|---------|
| `INT AUTO_INCREMENT` | Auto-incrementing integer (MySQL) | `id INT AUTO_INCREMENT PRIMARY KEY` |
| `INTEGER` / `INT` | Whole numbers | `age INT` |
| `DECIMAL(p, s)` | Precise numbers (money) | `fee DECIMAL(10, 2)` for ₹99,999.99 |
| `VARCHAR(n)` | Variable-length text up to n chars | `name VARCHAR(100)` |
| `TEXT` | Unlimited text | `bio TEXT` |
| `BOOLEAN` | True/False | `is_active BOOLEAN` |
| `DATE` | Date only (YYYY-MM-DD) | `joined_on DATE` |
| `DATETIME` | Date + time (MySQL/SQLite) | `created_at DATETIME` |
| `JSON` | JSON data (MySQL 5.7+) | `metadata JSON` |

### Constraints

Constraints enforce rules on the data:

| Constraint | What It Does | Example |
|-----------|-------------|---------|
| `PRIMARY KEY` | Unique identifier for each row | `id INT AUTO_INCREMENT PRIMARY KEY` |
| `NOT NULL` | Column cannot be empty | `name VARCHAR(100) NOT NULL` |
| `UNIQUE` | No duplicate values allowed | `email VARCHAR(150) UNIQUE` |
| `DEFAULT` | Sets a default value if none is provided | `city VARCHAR(50) DEFAULT 'Bhopal'` |
| `CHECK` | Custom condition that must be true | `CHECK (age >= 18)` |
| `REFERENCES` | Foreign key — links to another table | `student_id INT REFERENCES students(id)` |

**Example with all constraints:**

```sql
CREATE TABLE courses (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(200) NOT NULL,
    slug        VARCHAR(200) UNIQUE NOT NULL,
    price       DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    duration    INT NOT NULL CHECK (duration > 0),
    category    VARCHAR(50) DEFAULT 'General',
    is_published BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Creating Tables with Foreign Keys

```sql
CREATE TABLE enrollments (
    id          SERIAL PRIMARY KEY,
    student_id  INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    course_id   INT NOT NULL REFERENCES courses(id) ON DELETE RESTRICT,
    enrolled_on DATE DEFAULT CURRENT_DATE,
    status      VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'dropped')),
    UNIQUE(student_id, course_id)  -- Prevent duplicate enrollments
);
```

**ON DELETE options:**

| Option | What Happens When Referenced Row Is Deleted |
|--------|---------------------------------------------|
| `CASCADE` | Delete related rows too |
| `RESTRICT` | Prevent deletion if related rows exist |
| `SET NULL` | Set the foreign key to NULL |
| `SET DEFAULT` | Set the foreign key to its default value |

---

### ALTER TABLE

Modifies an existing table — add/drop/rename columns, add constraints.

```sql
-- Add a new column
ALTER TABLE students ADD COLUMN gender VARCHAR(10);

-- Add a column with a default
ALTER TABLE students ADD COLUMN batch VARCHAR(20) DEFAULT '2026-A';

-- Drop a column
ALTER TABLE students DROP COLUMN gender;

-- Rename a column
ALTER TABLE students RENAME COLUMN phone TO mobile;

-- Change data type
ALTER TABLE students ALTER COLUMN mobile TYPE VARCHAR(20);

-- Add NOT NULL constraint
ALTER TABLE students ALTER COLUMN mobile SET NOT NULL;

-- Remove NOT NULL constraint
ALTER TABLE students ALTER COLUMN mobile DROP NOT NULL;

-- Add a unique constraint
ALTER TABLE students ADD CONSTRAINT unique_phone UNIQUE (mobile);

-- Add a check constraint
ALTER TABLE courses ADD CONSTRAINT price_positive CHECK (price >= 0);

-- Rename the table itself
ALTER TABLE students RENAME TO learners;
```

---

### DROP TABLE

Deletes a table and all its data permanently.

```sql
-- Drop a table (error if it does not exist)
DROP TABLE enrollments;

-- Drop only if the table exists (safer)
DROP TABLE IF EXISTS enrollments;

-- Drop a table and all tables that depend on it
DROP TABLE students CASCADE;
```

**Warning:** `DROP TABLE` is irreversible. Always back up before dropping tables in production.

---

### TRUNCATE

Removes all rows from a table but keeps the table structure intact.

```sql
-- Remove all data, reset auto-increment
TRUNCATE TABLE enrollments;

-- Truncate and cascade to dependent tables
TRUNCATE TABLE students CASCADE;
```

**TRUNCATE vs DELETE:**

| Feature | TRUNCATE | DELETE |
|---------|----------|--------|
| Speed | Very fast (does not scan rows) | Slower (scans each row) |
| WHERE clause | Not supported | Supported |
| Rollback | Not possible in some databases | Can be rolled back |
| Auto-increment | Resets to 1 | Does not reset |
| Triggers | Does not fire row-level triggers | Fires row-level triggers |

---

## DML — Data Manipulation Language

DML commands add, update, and remove data (rows) in tables.

### INSERT — Adding Data

```sql
-- Insert a single row
INSERT INTO students (name, email, city, fee_paid)
VALUES ('Rahul Sharma', 'rahul@email.com', 'Bhopal', 15000.00);

-- Insert with all defaults (only required columns)
INSERT INTO students (name, email)
VALUES ('Priya Patel', 'priya@email.com');

-- Insert multiple rows at once
INSERT INTO students (name, email, city, fee_paid) VALUES
    ('Amit Kumar', 'amit@email.com', 'Delhi', 18000.00),
    ('Sneha Gupta', 'sneha@email.com', 'Pune', 15000.00),
    ('Ananya Singh', 'ananya@email.com', 'Bhopal', 20000.00);

-- Insert and get the new row's ID (MySQL)
INSERT INTO students (name, email, city)
VALUES ('Vikram Joshi', 'vikram@email.com', 'Mumbai');
SELECT LAST_INSERT_ID();  -- Returns the auto-generated ID
```

### INSERT with SELECT

Copy data from one table to another:

```sql
-- Copy all active students into an archive table
INSERT INTO student_archive (name, email, city)
SELECT name, email, city FROM students WHERE is_active = FALSE;
```

### Handling Conflicts (UPSERT)

```sql
-- Insert or update if email already exists (MySQL)
INSERT INTO students (name, email, city)
VALUES ('Rahul Sharma', 'rahul@email.com', 'Indore')
ON DUPLICATE KEY UPDATE city = VALUES(city), name = VALUES(name);

-- SQLite equivalent
INSERT OR REPLACE INTO students (name, email, city)
VALUES ('Rahul Sharma', 'rahul@email.com', 'Indore');
```

---

### UPDATE — Modifying Data

```sql
-- Update a single row
UPDATE students SET city = 'Indore' WHERE id = 1;

-- Update multiple columns
UPDATE students
SET city = 'Mumbai', fee_paid = 20000.00, is_active = TRUE
WHERE email = 'rahul@email.com';

-- Update all rows (dangerous without WHERE!)
UPDATE students SET is_active = FALSE;

-- Update using a calculation
UPDATE courses SET price = price * 1.10;  -- Increase all prices by 10%

-- Update and verify (MySQL — no RETURNING, use SELECT after)
UPDATE students SET fee_paid = fee_paid + 5000 WHERE id = 3;
SELECT id, name, fee_paid FROM students WHERE id = 3;
```

**Safety tip:** Always write the `WHERE` clause **first** before writing the `SET` clause. This prevents accidental mass updates.

---

### DELETE — Removing Data

```sql
-- Delete a specific row
DELETE FROM students WHERE id = 5;

-- Delete with a condition
DELETE FROM students WHERE is_active = FALSE AND city = 'Bhopal';

-- Delete all rows (use TRUNCATE instead for better performance)
DELETE FROM students;

-- Delete and verify (MySQL — use SELECT before to check)
SELECT id, name, email FROM students WHERE id = 3;  -- Check first
DELETE FROM students WHERE id = 3;
```

**Safety tip:** Always run a `SELECT` with the same `WHERE` clause first to see which rows will be affected:

```sql
-- Step 1: Check what will be deleted
SELECT * FROM students WHERE is_active = FALSE;

-- Step 2: If the result looks correct, delete
DELETE FROM students WHERE is_active = FALSE;
```

---

## Practical Example: Building a Course Management System

Let us build a small database for TechPath Institute:

```sql
-- Step 1: Create tables
CREATE TABLE instructors (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) UNIQUE NOT NULL,
    speciality  VARCHAR(100),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE courses (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(200) NOT NULL,
    instructor_id   INT REFERENCES instructors(id) ON DELETE SET NULL,
    price           DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    duration_weeks  INT NOT NULL CHECK (duration_weeks > 0),
    is_published    BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE students (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) UNIQUE NOT NULL,
    city        VARCHAR(50) DEFAULT 'Bhopal',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE enrollments (
    id          SERIAL PRIMARY KEY,
    student_id  INT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    course_id   INT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    enrolled_on DATE DEFAULT CURRENT_DATE,
    UNIQUE(student_id, course_id)
);

-- Step 2: Insert sample data
INSERT INTO instructors (name, email, speciality) VALUES
    ('Dr. Anil Verma', 'anil@techpath.biz', 'Python & AI'),
    ('Meera Iyer', 'meera@techpath.biz', 'Web Development');

INSERT INTO courses (title, instructor_id, price, duration_weeks, is_published) VALUES
    ('Python Full Stack', 1, 25000.00, 16, TRUE),
    ('React Masterclass', 2, 20000.00, 12, TRUE),
    ('Data Science with Python', 1, 30000.00, 20, FALSE);

INSERT INTO students (name, email, city) VALUES
    ('Rahul Sharma', 'rahul@email.com', 'Bhopal'),
    ('Priya Patel', 'priya@email.com', 'Pune'),
    ('Amit Kumar', 'amit@email.com', 'Delhi');

INSERT INTO enrollments (student_id, course_id) VALUES
    (1, 1), (1, 2),  -- Rahul enrolled in Python + React
    (2, 1),           -- Priya enrolled in Python
    (3, 2);           -- Amit enrolled in React

-- Step 3: Update data
UPDATE courses SET price = 22000.00 WHERE title = 'React Masterclass';
UPDATE students SET city = 'Indore' WHERE name = 'Rahul Sharma';

-- Step 4: Delete data
DELETE FROM enrollments WHERE student_id = 3 AND course_id = 2;
```

---

## Common Mistakes to Avoid

| Mistake | Problem | Fix |
|---------|---------|-----|
| `UPDATE students SET city = 'Pune'` (no WHERE) | Updates ALL rows | Always add WHERE |
| `DELETE FROM students` (no WHERE) | Deletes ALL rows | Always add WHERE |
| `DROP TABLE students` in production | Permanent data loss | Use backups, use `IF EXISTS` |
| Forgetting `NOT NULL` on required fields | Allows empty data | Always plan constraints |
| Using `VARCHAR(255)` everywhere | Wastes space, no validation | Choose appropriate lengths |

---

## Summary

| Command | Category | What It Does |
|---------|----------|-------------|
| `CREATE TABLE` | DDL | Creates a new table |
| `ALTER TABLE` | DDL | Modifies table structure |
| `DROP TABLE` | DDL | Deletes a table permanently |
| `TRUNCATE` | DDL | Removes all rows, keeps structure |
| `INSERT INTO` | DML | Adds new rows |
| `UPDATE` | DML | Modifies existing rows |
| `DELETE FROM` | DML | Removes specific rows |

---

*TechPath Institute — Python Full Stack Development*
