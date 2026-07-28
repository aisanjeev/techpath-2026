# Module 04: Database Design, SQL & NoSQL

## 1. Database Fundamentals

### What is a Database?
A database is an organized collection of data that can be easily accessed, managed, and updated. Think of it as a digital filing cabinet where data is stored in a structured way.

**Why not just use files (CSV, JSON)?**
- Files cannot handle multiple users reading/writing at the same time
- No built-in way to enforce data rules (e.g., "email must be unique")
- Searching through large files is very slow
- No relationships between different data files

### Types of Databases

| Type | Examples | Best For |
|------|----------|----------|
| Relational (SQL) | MySQL, SQLite, PostgreSQL | Structured data with relationships |
| Document (NoSQL) | MongoDB, CouchDB | Flexible/nested data, rapid prototyping |
| Key-Value | Redis, Memcached | Caching, sessions, real-time counters |
| Graph | Neo4j, ArangoDB | Social networks, recommendation engines |
| Time-Series | InfluxDB, TimescaleDB | IoT data, monitoring, analytics |

### Tables, Rows, and Columns
In a relational database, data is stored in **tables** (also called relations).

```
students table:
+----+-----------------+---------------------+----------+
| id | name            | email               | city     |
+----+-----------------+---------------------+----------+
|  1 | Rahul Sharma    | rahul@email.com     | Bhopal   |
|  2 | Priya Patel     | priya@email.com     | Pune     |
|  3 | Amit Kumar      | amit@email.com      | Delhi    |
+----+-----------------+---------------------+----------+
```

- **Table** = the entire structure (students)
- **Row** (record/tuple) = one entry (Rahul's data)
- **Column** (field/attribute) = one property (name, email)
- **Schema** = the design/blueprint of a table (column names, types, constraints)

### Keys

Keys uniquely identify rows and create links between tables.

| Key Type | Purpose | Example |
|----------|---------|---------|
| **Primary Key (PK)** | Uniquely identifies each row in a table | `students.id` |
| **Foreign Key (FK)** | Links to a primary key in another table | `enrollments.student_id` references `students.id` |
| **Composite Key** | Two or more columns together form a unique identifier | `(student_id, course_id)` in enrollments |
| **Candidate Key** | Any column (or set) that could be a primary key | `email` in students (unique, not null) |
| **Natural Key** | A real-world value used as PK | Aadhaar number, PAN number |
| **Surrogate Key** | An auto-generated value used as PK | Auto-increment `id` column |

**Best practice:** Always use a surrogate key (auto-increment integer or UUID) as the primary key. Natural keys can change (a person might change their email).

### Relationships

Relationships describe how tables connect to each other.

**One-to-One (1:1)** -- Each row in Table A relates to exactly one row in Table B.
```
students         student_profiles
+----+--------+  +----+------------+--------+
| id | name   |  | id | student_id | bio    |
+----+--------+  +----+------------+--------+
|  1 | Rahul  |  |  1 |          1 | ...    |
|  2 | Priya  |  |  2 |          2 | ...    |
+----+--------+  +----+------------+--------+
```
Each student has exactly one profile.

**One-to-Many (1:M)** -- One row in Table A relates to many rows in Table B.
```
courses          students
+----+--------+  +----+--------+-----------+
| id | name   |  | id | name   | course_id |
+----+--------+  +----+--------+-----------+
|  1 | Python |  |  1 | Rahul  |         1 |
|  2 | Java   |  |  2 | Priya  |         1 |
+----+--------+  |  3 | Amit   |         2 |
                 +----+--------+-----------+
```
One course has many students. This is the most common relationship.

**Many-to-Many (M:M)** -- Many rows in Table A relate to many rows in Table B. Requires a **junction table** (also called bridge/link table).
```
students         enrollments (junction)   courses
+----+--------+  +----+------+------+     +----+--------+
| id | name   |  | id | s_id | c_id |     | id | name   |
+----+--------+  +----+------+------+     +----+--------+
|  1 | Rahul  |  |  1 |    1 |    1 |     |  1 | Python |
|  2 | Priya  |  |  2 |    1 |    2 |     |  2 | SQL    |
+----+--------+  |  3 |    2 |    1 |     +----+--------+
                 +----+------+------+
```
Rahul is enrolled in Python AND SQL. Priya is enrolled in Python. One student can take many courses, and one course can have many students.

### ACID Properties

ACID guarantees that database transactions are reliable. A **transaction** is a group of operations that must all succeed or all fail.

| Property | Meaning | Example |
|----------|---------|---------|
| **Atomicity** | All operations in a transaction succeed, or none do | Transferring Rs. 5000 from Rahul to Priya -- both debit and credit must happen, or neither |
| **Consistency** | The database moves from one valid state to another | After transfer, total money in the system stays the same |
| **Isolation** | Concurrent transactions don't interfere with each other | Two people booking the last seat -- only one succeeds |
| **Durability** | Once committed, data survives crashes or power failures | After "Payment Successful", the record is permanently saved |

```sql
-- Example transaction
BEGIN TRANSACTION;
    UPDATE accounts SET balance = balance - 5000 WHERE name = 'Rahul';
    UPDATE accounts SET balance = balance + 5000 WHERE name = 'Priya';
COMMIT;  -- both happen together

-- If anything fails:
ROLLBACK;  -- undo everything
```

---

## 2. SQL Mastery

SQL (Structured Query Language) is the standard language for working with relational databases. It has several sub-languages:

| Category | Commands | Purpose |
|----------|----------|---------|
| **DDL** (Data Definition) | CREATE, ALTER, DROP, TRUNCATE | Define/modify table structure |
| **DML** (Data Manipulation) | INSERT, UPDATE, DELETE | Add/change/remove data |
| **DQL** (Data Query) | SELECT | Read/retrieve data |
| **DCL** (Data Control) | GRANT, REVOKE | Manage permissions |
| **TCL** (Transaction Control) | BEGIN, COMMIT, ROLLBACK | Manage transactions |

### DDL -- Data Definition Language

**CREATE TABLE**
```sql
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,     -- auto-increment integer (SQLite: INTEGER PRIMARY KEY)
    name VARCHAR(100) NOT NULL,           -- required text, max 100 chars
    email VARCHAR(150) UNIQUE NOT NULL,   -- must be unique and required
    phone VARCHAR(15),                    -- optional
    city VARCHAR(50) DEFAULT 'Bhopal',   -- default value
    fee_paid DECIMAL(10, 2) DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    enrolled_date DATE DEFAULT (CURRENT_DATE),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Common constraints:**
| Constraint | Purpose |
|------------|---------|
| `PRIMARY KEY` | Unique identifier for each row |
| `NOT NULL` | Column cannot be empty |
| `UNIQUE` | No duplicate values allowed |
| `DEFAULT` | Fallback value if none provided |
| `CHECK` | Validate data against a condition |
| `FOREIGN KEY` | Reference to another table's primary key |

**ALTER TABLE**
```sql
-- Add a column
ALTER TABLE students ADD COLUMN batch VARCHAR(20);

-- Change column type (MySQL)
ALTER TABLE students MODIFY COLUMN phone VARCHAR(20);

-- Add a constraint
ALTER TABLE students ADD CONSTRAINT chk_fee CHECK (fee_paid >= 0);

-- Rename a column (MySQL 8.0+)
ALTER TABLE students RENAME COLUMN city TO location;

-- Drop a column
ALTER TABLE students DROP COLUMN batch;
```

**DROP and TRUNCATE**
```sql
-- Delete the entire table (structure + data)
DROP TABLE IF EXISTS students;

-- Delete all data but keep the table structure
TRUNCATE TABLE students;
```

### DML -- Data Manipulation Language

**INSERT**
```sql
-- Insert one row
INSERT INTO students (name, email, phone, city)
VALUES ('Rahul Sharma', 'rahul@techpath.in', '9876543210', 'Bhopal');

-- Insert multiple rows
INSERT INTO students (name, email, phone, city) VALUES
    ('Priya Patel', 'priya@techpath.in', '9876543211', 'Pune'),
    ('Amit Kumar', 'amit@techpath.in', '9876543212', 'Delhi'),
    ('Sneha Gupta', 'sneha@techpath.in', '9876543213', 'Indore');
```

**UPDATE**
```sql
-- Update one row
UPDATE students SET city = 'Hyderabad' WHERE id = 3;

-- Update multiple columns
UPDATE students SET fee_paid = 25000, is_active = TRUE WHERE name = 'Rahul Sharma';

-- Update with calculation
UPDATE students SET fee_paid = fee_paid + 5000 WHERE city = 'Bhopal';
```

**DELETE**
```sql
-- Delete specific rows
DELETE FROM students WHERE is_active = FALSE;

-- Delete with condition
DELETE FROM students WHERE enrolled_date < '2025-01-01';

-- DANGER: Delete all rows (use TRUNCATE instead)
DELETE FROM students;
```

### SELECT -- Querying Data

**Basic SELECT**
```sql
-- All columns, all rows
SELECT * FROM students;

-- Specific columns
SELECT name, email, city FROM students;

-- With alias
SELECT name AS student_name, city AS location FROM students;
```

**WHERE -- Filtering**
```sql
-- Comparison operators
SELECT * FROM students WHERE city = 'Bhopal';
SELECT * FROM students WHERE fee_paid > 20000;
SELECT * FROM students WHERE fee_paid BETWEEN 15000 AND 30000;

-- Logical operators
SELECT * FROM students WHERE city = 'Bhopal' AND is_active = TRUE;
SELECT * FROM students WHERE city = 'Delhi' OR city = 'Pune';
SELECT * FROM students WHERE NOT is_active;

-- IN operator
SELECT * FROM students WHERE city IN ('Bhopal', 'Delhi', 'Pune');

-- LIKE for pattern matching
SELECT * FROM students WHERE name LIKE 'R%';       -- starts with R
SELECT * FROM students WHERE email LIKE '%@gmail%'; -- contains @gmail
SELECT * FROM students WHERE name LIKE '_a%';       -- second letter is 'a'

-- NULL checks
SELECT * FROM students WHERE phone IS NULL;
SELECT * FROM students WHERE phone IS NOT NULL;
```

**ORDER BY and LIMIT**
```sql
-- Sort ascending (default)
SELECT * FROM students ORDER BY name;

-- Sort descending
SELECT * FROM students ORDER BY fee_paid DESC;

-- Multiple sort columns
SELECT * FROM students ORDER BY city ASC, name DESC;

-- Limit results
SELECT * FROM students ORDER BY fee_paid DESC LIMIT 5;

-- Skip rows (pagination)
SELECT * FROM students ORDER BY id LIMIT 10 OFFSET 20;  -- page 3
```

**Aggregate Functions**
```sql
SELECT COUNT(*) AS total_students FROM students;
SELECT SUM(fee_paid) AS total_revenue FROM students;
SELECT AVG(fee_paid) AS avg_fee FROM students;
SELECT MAX(fee_paid) AS highest_fee FROM students;
SELECT MIN(fee_paid) AS lowest_fee FROM students;
```

**GROUP BY and HAVING**
```sql
-- Count students per city
SELECT city, COUNT(*) AS total
FROM students
GROUP BY city
ORDER BY total DESC;

-- Average fee per city (only cities with 3+ students)
SELECT city, AVG(fee_paid) AS avg_fee, COUNT(*) AS total
FROM students
GROUP BY city
HAVING COUNT(*) >= 3
ORDER BY avg_fee DESC;
```

### JOINs

JOINs combine rows from two or more tables based on a related column.

**Setup for examples:**
```
students:                    courses:
+----+--------+-----------+  +----+---------+--------+
| id | name   | course_id |  | id | name    | fee    |
+----+--------+-----------+  +----+---------+--------+
|  1 | Rahul  |         1 |  |  1 | Python  | 25000  |
|  2 | Priya  |         2 |  |  2 | Java    | 22000  |
|  3 | Amit   |         1 |  |  3 | DevOps  | 30000  |
|  4 | Sneha  |      NULL |  +----+---------+--------+
+----+--------+-----------+
```

**INNER JOIN** -- Only matching rows from both tables
```sql
SELECT s.name, c.name AS course
FROM students s
INNER JOIN courses c ON s.course_id = c.id;

-- Result: Rahul-Python, Priya-Java, Amit-Python
-- Sneha is excluded (no course_id)
-- DevOps is excluded (no students)
```

**LEFT JOIN** -- All rows from left table + matching from right
```sql
SELECT s.name, c.name AS course
FROM students s
LEFT JOIN courses c ON s.course_id = c.id;

-- Result: Rahul-Python, Priya-Java, Amit-Python, Sneha-NULL
-- Sneha is included with NULL for course
```

**RIGHT JOIN** -- All rows from right table + matching from left
```sql
SELECT s.name, c.name AS course
FROM students s
RIGHT JOIN courses c ON s.course_id = c.id;

-- Result: Rahul-Python, Priya-Java, Amit-Python, NULL-DevOps
-- DevOps is included with NULL for student name
```

**FULL OUTER JOIN** -- All rows from both tables
```sql
SELECT s.name, c.name AS course
FROM students s
FULL OUTER JOIN courses c ON s.course_id = c.id;

-- Result: all 5 rows -- Sneha-NULL and NULL-DevOps both included
```

**CROSS JOIN** -- Every row from A paired with every row from B (Cartesian product)
```sql
SELECT s.name, c.name AS course
FROM students s
CROSS JOIN courses c;

-- Result: 4 students x 3 courses = 12 rows
```

**SELF JOIN** -- A table joined with itself
```sql
-- Find students in the same city
SELECT a.name AS student_1, b.name AS student_2, a.city
FROM students a
JOIN students b ON a.city = b.city AND a.id < b.id;
```

### Subqueries

A subquery is a SELECT inside another SQL statement.

```sql
-- Students who paid more than the average fee
SELECT name, fee_paid
FROM students
WHERE fee_paid > (SELECT AVG(fee_paid) FROM students);

-- Students enrolled in the 'Python' course
SELECT name FROM students
WHERE course_id = (SELECT id FROM courses WHERE name = 'Python');

-- Students with the highest fee in each city
SELECT name, city, fee_paid FROM students
WHERE fee_paid IN (
    SELECT MAX(fee_paid) FROM students GROUP BY city
);
```

### CTEs (Common Table Expressions) -- WITH Clause

CTEs make complex queries more readable by creating temporary named result sets.

```sql
-- Calculate student rankings
WITH student_totals AS (
    SELECT
        s.id,
        s.name,
        s.city,
        SUM(p.amount) AS total_paid
    FROM students s
    JOIN payments p ON s.id = p.student_id
    GROUP BY s.id, s.name, s.city
)
SELECT
    name,
    city,
    total_paid,
    RANK() OVER (ORDER BY total_paid DESC) AS rank
FROM student_totals;
```

```sql
-- Multiple CTEs
WITH
active_students AS (
    SELECT * FROM students WHERE is_active = TRUE
),
city_counts AS (
    SELECT city, COUNT(*) AS total FROM active_students GROUP BY city
)
SELECT * FROM city_counts WHERE total >= 2 ORDER BY total DESC;
```

### CASE Expressions

```sql
SELECT
    name,
    fee_paid,
    CASE
        WHEN fee_paid >= 30000 THEN 'Premium'
        WHEN fee_paid >= 20000 THEN 'Standard'
        WHEN fee_paid >= 10000 THEN 'Basic'
        ELSE 'Pending'
    END AS fee_category
FROM students;
```

### Indexes

Indexes speed up searches on specific columns, like a book's index.

```sql
-- Create an index
CREATE INDEX idx_students_email ON students(email);
CREATE INDEX idx_students_city ON students(city);

-- Composite index (multiple columns)
CREATE INDEX idx_students_city_name ON students(city, name);

-- Unique index
CREATE UNIQUE INDEX idx_students_phone ON students(phone);

-- Drop an index
DROP INDEX idx_students_city;
```

**When to use indexes:**
- Columns used frequently in WHERE clauses
- Columns used in JOIN conditions
- Columns used in ORDER BY

**When NOT to use indexes:**
- Small tables (full scan is faster)
- Columns with very few unique values (e.g., boolean)
- Tables with heavy INSERT/UPDATE operations (indexes slow writes)

---

## 3. MySQL & SQLite Specifics

### MySQL vs SQLite -- When to Use Which?

| Feature | SQLite | MySQL |
|---------|--------|-------|
| Type | File-based (no server) | Server-based |
| Setup | No install needed (built into Python) | Install server + set password |
| Best for | Learning, prototyping, small apps | Production web apps, Indian IT industry |
| Concurrent writes | Poor (file locking) | Good |
| JSON support | JSON functions on TEXT | Native JSON type |
| GUI Tool | DB Browser for SQLite | MySQL Workbench |

**In this course:** SQLite for local development and labs, MySQL for production-ready projects.

### SQLite Setup

SQLite comes built into Python -- nothing to install:

```python
import sqlite3
conn = sqlite3.connect("techpath.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)")
conn.close()
```

Download **DB Browser for SQLite** (free GUI): https://sqlitebrowser.org/dl/

### MySQL Installation

**Windows:**
1. Download MySQL Installer from https://dev.mysql.com/downloads/installer/
2. Run the installer -- set a **root password** (remember it!)
3. Include **MySQL Workbench** during installation
4. Default port is **3306**

**Verify installation:**
```bash
mysql --version
# mysql  Ver 8.0.x
```

**Connect via command line:**
```bash
mysql -u root -p
# Enter your password

# Create a database
CREATE DATABASE techpath_db;

# Switch to it
USE techpath_db;

# List tables
SHOW TABLES;

# Quit
EXIT;
```

### MySQL Workbench
MySQL Workbench is the official visual GUI for MySQL.
1. Open MySQL Workbench from Start Menu
2. Click your local connection (localhost:3306)
3. Right-click in Schemas panel > Create Schema > Name: `techpath_db`
4. Open a new Query Tab (Ctrl+T) to run SQL

### Data Types Comparison

| Category | MySQL | SQLite |
|----------|-------|--------|
| Auto-increment PK | `INT AUTO_INCREMENT PRIMARY KEY` | `INTEGER PRIMARY KEY AUTOINCREMENT` |
| Integer | `INT`, `BIGINT` | `INTEGER` |
| Decimal | `DECIMAL(10,2)` | `REAL` |
| Text | `VARCHAR(n)`, `TEXT` | `TEXT` |
| Boolean | `BOOLEAN` (alias for TINYINT) | `INTEGER` (0 or 1) |
| Date | `DATE`, `DATETIME` | `TEXT` (stored as string) |
| JSON | `JSON` (native type) | `TEXT` (with JSON functions) |

### JSON Support

**MySQL** has a native JSON type with operators:
```sql
CREATE TABLE student_profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT REFERENCES students(id),
    profile JSON NOT NULL
);

-- Insert JSON data
INSERT INTO student_profiles (student_id, profile) VALUES
(1, '{"hobbies": ["cricket", "coding"], "gpa": 8.5, "address": {"city": "Bhopal", "pin": "462001"}}'),
(2, '{"hobbies": ["reading", "music"], "gpa": 9.2, "address": {"city": "Pune", "pin": "411001"}}');

-- Query JSON fields (MySQL syntax)
SELECT profile->>'$.gpa' AS gpa FROM student_profiles;
SELECT profile->>'$.address.city' AS city FROM student_profiles;

-- Filter by JSON value
SELECT * FROM student_profiles WHERE profile->>'$.gpa' > '8.0';

-- Check if key path exists
SELECT * FROM student_profiles WHERE JSON_CONTAINS_PATH(profile, 'one', '$.hobbies');

-- Check if array contains a value
SELECT * FROM student_profiles WHERE JSON_CONTAINS(profile->'$.hobbies', '"cricket"');
```

**SQLite** uses JSON functions:
```sql
-- SQLite JSON queries
SELECT json_extract(profile, '$.gpa') AS gpa FROM student_profiles;
SELECT json_extract(profile, '$.address.city') AS city FROM student_profiles;
SELECT * FROM student_profiles WHERE json_extract(profile, '$.gpa') > 8.0;
```

### Stored Procedures (MySQL Only)

SQLite does not support stored procedures. MySQL does:

```sql
-- Create a function to get student count by city (MySQL)
DELIMITER //
CREATE FUNCTION get_city_count(city_name VARCHAR(50))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE student_count INT;
    SELECT COUNT(*) INTO student_count
    FROM students WHERE city = city_name;
    RETURN student_count;
END //
DELIMITER ;

-- Use the function
SELECT get_city_count('Bhopal');
```

```sql
-- Stored procedure to enroll a student (MySQL)
DELIMITER //
CREATE PROCEDURE enroll_student(
    IN p_name VARCHAR(100),
    IN p_email VARCHAR(150),
    IN p_course_id INT
)
BEGIN
    INSERT INTO students (name, email, course_id, enrolled_date)
    VALUES (p_name, p_email, p_course_id, CURRENT_DATE);

    INSERT INTO enrollments (student_id, course_id, enrolled_date)
    VALUES (LAST_INSERT_ID(), p_course_id, CURRENT_DATE);

    SELECT CONCAT('Student ', p_name, ' enrolled successfully') AS message;
END //
DELIMITER ;

-- Call the procedure
CALL enroll_student('Vikram Singh', 'vikram@techpath.in', 1);
```

### Triggers

Triggers work in both MySQL and SQLite, but with different syntax.

**MySQL trigger:**
```sql
-- Create a log table
CREATE TABLE audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(50),
    action VARCHAR(10),
    old_data JSON,
    new_data JSON,
    changed_at DATETIME DEFAULT NOW()
);

-- MySQL trigger for INSERT audit
DELIMITER //
CREATE TRIGGER trg_student_insert_audit
AFTER INSERT ON students
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, action, new_data)
    VALUES ('students', 'INSERT', JSON_OBJECT(
        'id', NEW.id, 'name', NEW.name, 'email', NEW.email, 'city', NEW.city
    ));
END //
DELIMITER ;
```

**SQLite trigger:**
```sql
-- SQLite trigger (simpler syntax)
CREATE TRIGGER trg_student_insert_audit
AFTER INSERT ON students
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, action, new_data)
    VALUES ('students', 'INSERT', json_object(
        'id', NEW.id, 'name', NEW.name, 'email', NEW.email, 'city', NEW.city
    ));
END;
```

---

## 4. SQLAlchemy ORM

### What is an ORM?
ORM (Object-Relational Mapping) lets you interact with a database using Python classes instead of writing raw SQL.

| Without ORM (raw SQL) | With ORM (SQLAlchemy) |
|----------------------|----------------------|
| `SELECT * FROM students WHERE city='Bhopal'` | `session.query(Student).filter_by(city='Bhopal').all()` |
| You write SQL strings | You write Python code |
| Must handle SQL injection yourself | Automatically safe from injection |
| Database-specific syntax | Works with PostgreSQL, MySQL, SQLite |

### Installation

```bash
pip install sqlalchemy                    # ORM (works with MySQL, SQLite, etc.)
pip install pymysql                       # MySQL driver
pip install aiosqlite                     # SQLite async driver
pip install alembic                       # Migrations
```

### Defining Models

```python
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    duration_months = Column(Integer, nullable=False)
    fee = Column(Float, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: one course has many students
    students = relationship("Student", back_populates="course")

    def __repr__(self):
        return f"<Course(name='{self.name}', fee={self.fee})>"


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(15))
    city = Column(String(50), default="Bhopal")
    is_active = Column(Boolean, default=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    enrolled_date = Column(DateTime, default=datetime.utcnow)

    # Relationship: each student belongs to one course
    course = relationship("Course", back_populates="students")

    def __repr__(self):
        return f"<Student(name='{self.name}', city='{self.city}')>"
```

### Database Setup

```python
# SQLite (for development -- no server needed)
engine = create_engine("sqlite:///techpath.db", echo=True)

# MySQL (for production)
# engine = create_engine("mysql+pymysql://user:password@localhost:3306/techpath_db")

# Create all tables
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()
```

### CRUD Operations

**Create**
```python
# Create a course
python_course = Course(name="Python Full Stack", duration_months=6, fee=35000)
session.add(python_course)
session.commit()

# Create a student
rahul = Student(name="Rahul Sharma", email="rahul@techpath.in", city="Bhopal", course=python_course)
session.add(rahul)
session.commit()

# Create multiple students
students = [
    Student(name="Priya Patel", email="priya@techpath.in", city="Pune", course=python_course),
    Student(name="Amit Kumar", email="amit@techpath.in", city="Delhi", course=python_course),
]
session.add_all(students)
session.commit()
```

**Read**
```python
# Get all students
all_students = session.query(Student).all()
for s in all_students:
    print(f"{s.name} - {s.city}")

# Filter
bhopal_students = session.query(Student).filter_by(city="Bhopal").all()

# Filter with conditions
active_students = session.query(Student).filter(
    Student.is_active == True,
    Student.city.in_(["Bhopal", "Delhi"])
).all()

# Get one record
student = session.query(Student).filter_by(email="rahul@techpath.in").first()

# Count
total = session.query(Student).count()

# Order and limit
top_students = session.query(Student).order_by(Student.name).limit(5).all()
```

**Update**
```python
student = session.query(Student).filter_by(email="rahul@techpath.in").first()
student.city = "Hyderabad"
student.phone = "9988776655"
session.commit()
```

**Delete**
```python
student = session.query(Student).filter_by(email="amit@techpath.in").first()
session.delete(student)
session.commit()
```

### Relationships in Action

```python
# Access related objects
student = session.query(Student).filter_by(name="Rahul Sharma").first()
print(f"{student.name} is enrolled in {student.course.name}")  # Navigate to course

# Access from the other side
course = session.query(Course).filter_by(name="Python Full Stack").first()
for student in course.students:
    print(f"  - {student.name} from {student.city}")
```

### Many-to-Many Relationships

```python
from sqlalchemy import Table

# Junction table
student_skills = Table(
    "student_skills",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("skill_id", Integer, ForeignKey("skills.id"), primary_key=True),
)

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    students = relationship("Student", secondary=student_skills, back_populates="skills")

# Add to Student class:
# skills = relationship("Skill", secondary=student_skills, back_populates="students")
```

### Migrations with Alembic

Alembic tracks database changes over time, like Git for your database schema.

```bash
# Initialize Alembic
alembic init alembic

# Edit alembic.ini -- set the database URL
# sqlalchemy.url = sqlite:///techpath.db

# Generate a migration
alembic revision --autogenerate -m "create students and courses tables"

# Apply the migration
alembic upgrade head

# See migration history
alembic history

# Rollback one step
alembic downgrade -1
```

**Typical workflow:**
1. Change your SQLAlchemy model (add a column, change a type)
2. Run `alembic revision --autogenerate -m "description"`
3. Review the generated migration file in `alembic/versions/`
4. Run `alembic upgrade head` to apply

---

## 5. MongoDB Basics

### What is MongoDB?
MongoDB is a **document database** (NoSQL). Instead of tables with rows and columns, it stores data as **documents** -- flexible JSON-like objects.

**SQL vs MongoDB terminology:**

| SQL | MongoDB |
|-----|---------|
| Database | Database |
| Table | Collection |
| Row | Document |
| Column | Field |
| Primary Key | `_id` (auto-generated) |
| JOIN | Embedding / `$lookup` |
| Schema | Schema-less (flexible) |

### When to Use MongoDB
- Rapidly changing requirements (no fixed schema)
- Nested/hierarchical data (e.g., blog posts with comments)
- High-volume, low-complexity reads
- Real-time analytics and logging

### Installation

1. Download MongoDB Community Server from https://www.mongodb.com/try/download/community
2. Install **MongoDB Compass** (GUI) -- it comes bundled
3. Start the MongoDB service

```bash
# Verify installation
mongosh --version

# Connect
mongosh
```

### Documents vs Tables

**SQL table row:**
```sql
INSERT INTO students (name, email, city, courses)
VALUES ('Rahul Sharma', 'rahul@techpath.in', 'Bhopal', ???);
-- Cannot easily store an array of courses in SQL
```

**MongoDB document:**
```json
{
    "_id": "ObjectId('...')",
    "name": "Rahul Sharma",
    "email": "rahul@techpath.in",
    "city": "Bhopal",
    "courses": ["Python Full Stack", "Data Science"],
    "address": {
        "street": "123 MP Nagar",
        "city": "Bhopal",
        "pin": "462001"
    },
    "marks": [
        {"subject": "Python", "score": 88},
        {"subject": "SQL", "score": 92}
    ]
}
```

Notice how MongoDB can store arrays and nested objects directly -- no need for separate tables or JOINs.

### PyMongo -- Python + MongoDB

```bash
pip install pymongo
```

**Connect and create a database:**
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["techpath_db"]
students = db["students"]  # collection (like a table)
```

**Create (Insert)**
```python
# Insert one document
student = {
    "name": "Rahul Sharma",
    "email": "rahul@techpath.in",
    "city": "Bhopal",
    "course": "Python Full Stack",
    "fee_paid": 25000,
    "is_active": True
}
result = students.insert_one(student)
print(f"Inserted ID: {result.inserted_id}")

# Insert many documents
many_students = [
    {"name": "Priya Patel", "email": "priya@techpath.in", "city": "Pune", "course": "Python Full Stack", "fee_paid": 30000},
    {"name": "Amit Kumar", "email": "amit@techpath.in", "city": "Delhi", "course": "Data Science", "fee_paid": 20000},
    {"name": "Sneha Gupta", "email": "sneha@techpath.in", "city": "Indore", "course": "Python Full Stack", "fee_paid": 35000},
]
result = students.insert_many(many_students)
print(f"Inserted {len(result.inserted_ids)} documents")
```

**Read (Find)**
```python
# Find all
for student in students.find():
    print(student["name"], student["city"])

# Find with filter
for student in students.find({"city": "Bhopal"}):
    print(student["name"])

# Find one
student = students.find_one({"email": "rahul@techpath.in"})

# Projection (select specific fields)
for student in students.find({}, {"name": 1, "city": 1, "_id": 0}):
    print(student)

# Sorting and limiting
for student in students.find().sort("name", 1).limit(5):
    print(student["name"])

# Count
total = students.count_documents({"city": "Bhopal"})
```

**Update**
```python
# Update one
students.update_one(
    {"email": "rahul@techpath.in"},
    {"$set": {"city": "Hyderabad", "fee_paid": 30000}}
)

# Update many
students.update_many(
    {"course": "Python Full Stack"},
    {"$set": {"is_active": True}}
)

# Increment a value
students.update_one(
    {"email": "rahul@techpath.in"},
    {"$inc": {"fee_paid": 5000}}
)
```

**Delete**
```python
# Delete one
students.delete_one({"email": "amit@techpath.in"})

# Delete many
students.delete_many({"is_active": False})
```

### Aggregation Pipeline

The aggregation pipeline processes documents through stages, like a factory assembly line.

```python
# Average fee per city
pipeline = [
    {"$group": {
        "_id": "$city",
        "avg_fee": {"$avg": "$fee_paid"},
        "total_students": {"$sum": 1}
    }},
    {"$sort": {"total_students": -1}}
]

for result in students.aggregate(pipeline):
    print(f"{result['_id']}: Avg Fee = Rs. {result['avg_fee']:.0f}, Students = {result['total_students']}")
```

```python
# Students grouped by course with details
pipeline = [
    {"$match": {"is_active": True}},          # Stage 1: Filter
    {"$group": {                               # Stage 2: Group
        "_id": "$course",
        "students": {"$push": "$name"},
        "total_fee": {"$sum": "$fee_paid"},
        "count": {"$sum": 1}
    }},
    {"$project": {                             # Stage 3: Reshape output
        "course": "$_id",
        "students": 1,
        "total_fee": 1,
        "count": 1,
        "_id": 0
    }},
    {"$sort": {"count": -1}}                   # Stage 4: Sort
]
```

---

## 6. Redis Basics

### What is Redis?
Redis is an **in-memory key-value store**. It keeps data in RAM, making it extremely fast (sub-millisecond reads). It is used for caching, session storage, real-time leaderboards, and message queuing.

### Installation

**Windows:** Download from https://github.com/microsoftarchive/redis/releases or use Docker:
```bash
docker run -d --name redis -p 6379:6379 redis
```

**Verify:**
```bash
redis-cli ping
# PONG
```

### Python + Redis

```bash
pip install redis
```

```python
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# Test connection
print(r.ping())  # True
```

### Key-Value Operations

```python
# SET and GET
r.set("student:1:name", "Rahul Sharma")
print(r.get("student:1:name"))  # "Rahul Sharma"

# Set with expiry (TTL in seconds)
r.setex("otp:9876543210", 300, "482901")  # expires in 5 minutes

# Check TTL
print(r.ttl("otp:9876543210"))  # seconds remaining

# Delete a key
r.delete("student:1:name")

# Check if key exists
print(r.exists("student:1:name"))  # 0 (False)
```

### Data Structures in Redis

**Hash (like a Python dictionary)**
```python
# Store student data as a hash
r.hset("student:1", mapping={
    "name": "Rahul Sharma",
    "email": "rahul@techpath.in",
    "city": "Bhopal",
    "course": "Python Full Stack"
})

# Get one field
print(r.hget("student:1", "name"))  # "Rahul Sharma"

# Get all fields
print(r.hgetall("student:1"))  # {'name': 'Rahul Sharma', ...}
```

**List (ordered collection)**
```python
# Push items
r.rpush("notifications:rahul", "Assignment 1 due tomorrow")
r.rpush("notifications:rahul", "New lab posted: SQLAlchemy")
r.lpush("notifications:rahul", "URGENT: Fee payment reminder")  # add to front

# Get items
print(r.lrange("notifications:rahul", 0, -1))  # all notifications

# Pop (remove and return)
print(r.lpop("notifications:rahul"))  # remove from front
```

**Set (unique values, no duplicates)**
```python
# Add to set
r.sadd("online_users", "rahul", "priya", "amit")
r.sadd("online_users", "rahul")  # ignored, already exists

# Get all members
print(r.smembers("online_users"))  # {'rahul', 'priya', 'amit'}

# Check membership
print(r.sismember("online_users", "rahul"))  # True
```

**Sorted Set (set with scores, auto-sorted)**
```python
# Leaderboard
r.zadd("leaderboard", {"Rahul": 88, "Priya": 95, "Amit": 72, "Sneha": 91})

# Get top 3 (highest scores first)
print(r.zrevrange("leaderboard", 0, 2, withscores=True))
# [('Priya', 95.0), ('Sneha', 91.0), ('Rahul', 88.0)]

# Get rank
print(r.zrevrank("leaderboard", "Rahul"))  # 2 (0-indexed)
```

### Caching Pattern

A common pattern: check Redis cache first, then query the database if not found.

```python
import json

def get_student(student_id):
    # 1. Check cache
    cache_key = f"student:{student_id}"
    cached = r.get(cache_key)
    if cached:
        print("Cache HIT")
        return json.loads(cached)

    # 2. Query database (slow)
    print("Cache MISS - querying database...")
    student = db.query(Student).get(student_id)
    if student:
        student_data = {"name": student.name, "email": student.email, "city": student.city}
        # 3. Store in cache for 1 hour
        r.setex(cache_key, 3600, json.dumps(student_data))
        return student_data

    return None
```

### Session Management

```python
import uuid

def create_session(user_id):
    session_id = str(uuid.uuid4())
    r.hset(f"session:{session_id}", mapping={
        "user_id": user_id,
        "login_time": str(datetime.now()),
        "ip": "192.168.1.1"
    })
    r.expire(f"session:{session_id}", 1800)  # 30 min timeout
    return session_id

def get_session(session_id):
    return r.hgetall(f"session:{session_id}")

def destroy_session(session_id):
    r.delete(f"session:{session_id}")
```

### Pub/Sub (Publish/Subscribe)

Pub/Sub allows real-time messaging between different parts of your application.

```python
# Publisher (sender)
r.publish("notifications", "New course added: AI with Python")

# Subscriber (receiver) -- run in a separate process
pubsub = r.pubsub()
pubsub.subscribe("notifications")

for message in pubsub.listen():
    if message["type"] == "message":
        print(f"Received: {message['data']}")
```

---

## 7. Database Normalization

Normalization is the process of organizing data to reduce duplication and improve integrity.

### Unnormalized Data (Problems)

```
| student | email           | course       | trainer       | trainer_phone |
|---------|-----------------|--------------|---------------|---------------|
| Rahul   | rahul@email.com | Python       | Ananya Reddy  | 9876543210    |
| Rahul   | rahul@email.com | SQL          | Vikram Singh  | 9876543211    |
| Priya   | priya@email.com | Python       | Ananya Reddy  | 9876543210    |
```

**Problems:**
- Rahul's email is stored twice (redundancy)
- If Ananya changes her phone, we must update multiple rows (update anomaly)
- If we delete Priya, we lose the fact that she took Python (delete anomaly)
- We cannot add a new course without a student (insert anomaly)

### First Normal Form (1NF)

**Rules:**
- Each cell contains a single value (no lists or arrays)
- Each row is unique (has a primary key)
- All entries in a column are of the same type

**Before (violates 1NF):**
```
| id | name  | courses          |
|----|-------|------------------|
|  1 | Rahul | Python, SQL, JS  |
```

**After (1NF):**
```
| id | name  | course |
|----|-------|--------|
|  1 | Rahul | Python |
|  1 | Rahul | SQL    |
|  1 | Rahul | JS     |
```

### Second Normal Form (2NF)

**Rules:**
- Must be in 1NF
- Every non-key column must depend on the **entire** primary key (no partial dependencies)

**Before (violates 2NF) -- composite key (student_id, course_id):**
```
| student_id | course_id | student_name | course_name | fee   |
|------------|-----------|--------------|-------------|-------|
|          1 |         1 | Rahul        | Python      | 25000 |
```
`student_name` depends only on `student_id`, not on the full key.

**After (2NF) -- split into separate tables:**
```
students:                 courses:               enrollments:
| id | name  |           | id | name   | fee |  | student_id | course_id |
|----|-------|           |----|--------|-----|  |------------|-----------|
|  1 | Rahul |           |  1 | Python | 25K |  |          1 |         1 |
```

### Third Normal Form (3NF)

**Rules:**
- Must be in 2NF
- No transitive dependencies (non-key column should not depend on another non-key column)

**Before (violates 3NF):**
```
| id | name  | city    | state            |
|----|-------|---------|------------------|
|  1 | Rahul | Bhopal  | Madhya Pradesh   |
|  2 | Priya | Indore  | Madhya Pradesh   |
```
`state` depends on `city`, not directly on the primary key.

**After (3NF):**
```
students:                     cities:
| id | name  | city_id |     | id | city   | state          |
|----|-------|---------|     |----|--------|----------------|
|  1 | Rahul |       1 |     |  1 | Bhopal | Madhya Pradesh |
|  2 | Priya |       2 |     |  2 | Indore | Madhya Pradesh |
```

### When to Denormalize
Sometimes, for performance, you intentionally add redundancy:
- Reporting tables that need fast reads
- Caching frequently computed values
- Reducing complex JOINs on read-heavy tables

---

## 8. ERD Design Principles

An Entity-Relationship Diagram (ERD) is a visual representation of your database structure.

### ERD Components

| Symbol | Meaning |
|--------|---------|
| Rectangle | Entity (table) |
| Oval | Attribute (column) |
| Diamond | Relationship |
| Line | Connection |
| PK | Primary Key |
| FK | Foreign Key |

### Sample ERD for TechPath Institute

```
+----------------+       +------------------+       +----------------+
|   courses      |       |   enrollments    |       |   students     |
+----------------+       +------------------+       +----------------+
| PK id          |<----->| PK id            |<----->| PK id          |
|    name        |       | FK student_id    |       |    name        |
|    duration     |       | FK course_id     |       |    email       |
|    fee          |       |    enrolled_date |       |    phone       |
|    description  |       |    status        |       |    city        |
+----------------+       +------------------+       +----------------+
                                                           |
                                                           v
                                                    +----------------+
                                                    |   payments     |
                                                    +----------------+
                                                    | PK id          |
                                                    | FK student_id  |
                                                    |    amount      |
                                                    |    date        |
                                                    |    method      |
                                                    +----------------+
```

### Design Best Practices

1. **Always use surrogate keys** (auto-increment `id`) as primary keys
2. **Name tables as plural nouns** (students, courses, not student, course)
3. **Name foreign keys as `table_id`** (student_id, course_id)
4. **Add timestamps** (created_at, updated_at) to every table
5. **Use appropriate data types** -- do not store numbers as text
6. **Add indexes** on columns used in WHERE, JOIN, and ORDER BY
7. **Use constraints** (NOT NULL, UNIQUE, CHECK, FK) to enforce data integrity
8. **Normalize to 3NF** by default, denormalize only when performance requires it
9. **Document your schema** with comments and ERD diagrams
10. **Plan for growth** -- use BIGINT for IDs if you expect millions of rows

---

## 9. Performance & Query Optimization

### EXPLAIN -- Understanding Query Execution

`EXPLAIN` shows how the database executes a query.

**MySQL:**
```sql
EXPLAIN SELECT * FROM students WHERE city = 'Bhopal';
```

Output shows columns like `type`, `possible_keys`, `key`, `rows`, `Extra`:
- **ALL** = full table scan (reads every row) -- slow on large tables
- **ref** or **index** = uses an index (much faster)
- **rows** = estimated number of rows to scan

**SQLite:**
```sql
EXPLAIN QUERY PLAN SELECT * FROM students WHERE city = 'Bhopal';
```

Output shows `SCAN students` (full scan) or `SEARCH students USING INDEX` (indexed).

```sql
-- After creating an index
CREATE INDEX idx_students_city ON students(city);

-- MySQL
EXPLAIN SELECT * FROM students WHERE city = 'Bhopal';
-- Now shows key = idx_students_city

-- SQLite
EXPLAIN QUERY PLAN SELECT * FROM students WHERE city = 'Bhopal';
-- Now shows: SEARCH students USING INDEX idx_students_city
```

### Query Optimization Strategies

| Problem | Solution |
|---------|----------|
| Slow WHERE clause | Add an index on the filtered column |
| SELECT * | Select only the columns you need |
| No LIMIT on large tables | Always add LIMIT for display queries |
| Repeated subquery | Use CTE or JOIN instead |
| N+1 query problem | Use eager loading (JOIN or subquery load) |
| Large table scans | Partition the table by date or category |
| Slow JOIN | Ensure JOIN columns are indexed |
| Complex calculations per row | Pre-compute and store in a column |

### Indexing Strategies

```sql
-- B-tree index (default, good for =, <, >, BETWEEN) -- works in MySQL and SQLite
CREATE INDEX idx_student_name ON students(name);

-- Unique index
CREATE UNIQUE INDEX idx_student_email ON students(email);

-- Composite index (multiple columns)
CREATE INDEX idx_student_city_name ON students(city, name);

-- Prefix index (MySQL only -- index first N characters of a text column)
CREATE INDEX idx_student_name_prefix ON students(name(20));
```

### Key Performance Rules

1. **Index columns used in WHERE, JOIN, and ORDER BY**
2. **Avoid SELECT * in production code** -- fetch only needed columns
3. **Use LIMIT for pagination** -- never fetch all rows at once
4. **Use EXPLAIN ANALYZE** to check query plans
5. **Batch INSERT statements** -- insert 100 rows at once, not one at a time
6. **Use connection pooling** -- do not open/close connections for every query
7. **Cache hot queries** with Redis
8. **Monitor slow queries** -- MySQL can log queries slower than a threshold (`slow_query_log`)
