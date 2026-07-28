# Database Fundamentals

**Module 04 — Database Design, SQL & NoSQL | Topic 1**

---

## What is a Database?

A database is an organized collection of data stored electronically. Think of it like a well-organized library — every book has a fixed shelf, a category, and a unique code. Similarly, every piece of data in a database has a fixed location and can be found quickly.

**Real-world analogy:** Imagine you run a coaching institute in Bhopal. You keep student records in a register — name, phone number, course enrolled, fees paid. That register is your "database." But what happens when you have 10,000 students? You cannot flip through pages fast enough. A computer database solves this — it stores, searches, and updates data in milliseconds.

### Why Not Just Use Files?

| Approach | Problem |
|----------|---------|
| Excel/CSV files | Cannot handle 100 users editing at the same time |
| JSON files | No built-in rules like "email must be unique" |
| Text files | Searching through 1 million records is painfully slow |
| Any flat file | No way to link related data (students ↔ courses) |

A **Database Management System (DBMS)** solves all of these problems.

---

## Types of Databases

| Type | Examples | Best For | Think of It As |
|------|----------|----------|----------------|
| **Relational (SQL)** | PostgreSQL, MySQL, SQLite | Structured data with relationships | Excel spreadsheet with rules |
| **Document (NoSQL)** | MongoDB, CouchDB | Flexible/nested data | JSON files with superpowers |
| **Key-Value** | Redis, Memcached | Caching, sessions | A dictionary (key → value) |
| **Graph** | Neo4j, ArangoDB | Social networks, recommendations | A web of connections |
| **Time-Series** | InfluxDB, TimescaleDB | IoT, monitoring, analytics | Timestamped log entries |

For this course, we focus on **MySQL and SQLite** (relational), **MongoDB** (document), and **Redis** (key-value).

---

## Tables, Rows, and Columns

In a relational database, data lives in **tables** (also called relations).

```
students table:
+----+-----------------+---------------------+----------+--------+
| id | name            | email               | city     | fee    |
+----+-----------------+---------------------+----------+--------+
|  1 | Rahul Sharma    | rahul@email.com     | Bhopal   |  15000 |
|  2 | Priya Patel     | priya@email.com     | Pune     |  18000 |
|  3 | Amit Kumar      | amit@email.com      | Delhi    |  15000 |
+----+-----------------+---------------------+----------+--------+
```

**Key terminology:**

| Term | Also Called | Meaning |
|------|-----------|---------|
| **Table** | Relation | The entire structure (e.g., `students`) |
| **Row** | Record, Tuple | One complete entry (Rahul's data) |
| **Column** | Field, Attribute | One property (name, email, city) |
| **Schema** | Blueprint | The design of a table — column names, types, constraints |
| **Database** | DB | A collection of related tables |

---

## Keys — The Identity System

Keys are the backbone of relational databases. They identify rows and connect tables.

### Primary Key (PK)

A column (or set of columns) that **uniquely identifies** each row. No two rows can have the same primary key value. It can never be NULL.

```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,   -- Auto-incrementing primary key
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL
);
```

### Foreign Key (FK)

A column that **refers to the primary key** of another table. It creates a link between two tables.

```sql
CREATE TABLE enrollments (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(id),  -- Foreign key
    course_id INT REFERENCES courses(id),    -- Foreign key
    enrolled_on DATE DEFAULT CURRENT_DATE
);
```

### Other Key Types

| Key Type | What It Does | Example |
|----------|-------------|---------|
| **Composite Key** | Two or more columns together form a unique identifier | `(student_id, course_id)` in enrollments |
| **Candidate Key** | Any column that *could* be a primary key | `email` in students (unique, not null) |
| **Natural Key** | A real-world value used as PK | Aadhaar number, PAN number |
| **Surrogate Key** | An auto-generated value used as PK | Auto-increment `id` column |

**Best practice:** Always use a **surrogate key** (auto-increment integer or UUID) as the primary key. Natural keys can change — a person might change their email or phone number.

---

## Relationships

Relationships describe how tables connect to each other. There are three types.

### One-to-One (1:1)

Each row in Table A relates to exactly one row in Table B.

```
students              student_profiles
+----+---------+      +----+------------+------------------+
| id | name    |      | id | student_id | bio              |
+----+---------+      +----+------------+------------------+
|  1 | Rahul   |      |  1 |          1 | Loves Python     |
|  2 | Priya   |      |  2 |          2 | Data enthusiast  |
+----+---------+      +----+------------+------------------+
```

**Use case:** Separating rarely-accessed data from the main table (e.g., profile details, addresses).

### One-to-Many (1:M)

One row in Table A relates to many rows in Table B. This is the **most common** relationship.

```
courses                students
+----+----------+      +----+---------+-----------+
| id | name     |      | id | name    | course_id |
+----+----------+      +----+---------+-----------+
|  1 | Python   |      |  1 | Rahul   |         1 |
|  2 | Java     |      |  2 | Priya   |         1 |
+----+----------+      |  3 | Amit    |         2 |
                        +----+---------+-----------+
```

One course has many students. Each student belongs to one course.

### Many-to-Many (M:N)

Many rows in Table A relate to many rows in Table B. This requires a **junction table** (also called a bridge table).

```
students        enrollments (junction)       courses
+----+-------+  +----+-----+-----+--------+  +----+----------+
| id | name  |  | id | s_id| c_id| date   |  | id | name     |
+----+-------+  +----+-----+-----+--------+  +----+----------+
|  1 | Rahul |  |  1 |   1 |   1 | 2026-01|  |  1 | Python   |
|  2 | Priya |  |  2 |   1 |   2 | 2026-01|  |  2 | FastAPI  |
+----+-------+  |  3 |   2 |   1 | 2026-02|  +----+----------+
                 +----+-----+-----+--------+
```

Rahul is enrolled in both Python and FastAPI. Python has both Rahul and Priya.

---

## ACID Properties

ACID is a set of four guarantees that every reliable database transaction must follow.

| Property | Meaning | Real-World Analogy |
|----------|---------|-------------------|
| **Atomicity** | All or nothing — either the entire transaction succeeds, or nothing changes | UPI payment: money leaves your account AND reaches the shopkeeper, or neither happens |
| **Consistency** | The database moves from one valid state to another valid state | Your bank balance can never go negative (if a rule says so) |
| **Isolation** | Concurrent transactions do not interfere with each other | Two people booking the last train ticket — only one gets it |
| **Durability** | Once committed, data survives crashes, power failures | After your UPI payment shows "Success," it stays successful even if the server restarts |

### Example: Bank Transfer

```
Transaction: Transfer ₹5,000 from Rahul to Priya

Step 1: Debit ₹5,000 from Rahul's account
Step 2: Credit ₹5,000 to Priya's account

Atomicity:  If Step 2 fails, Step 1 is rolled back. Rahul keeps his money.
Consistency: Total money before = Total money after.
Isolation:   If Amit also sends money to Priya at the same time, both work correctly.
Durability:  After commit, even if the server crashes, the transfer is permanent.
```

---

## Transactions

A **transaction** is a group of SQL operations that are treated as a single unit.

```sql
BEGIN;                                    -- Start transaction

UPDATE accounts SET balance = balance - 5000 WHERE name = 'Rahul';
UPDATE accounts SET balance = balance + 5000 WHERE name = 'Priya';

COMMIT;                                   -- Make changes permanent
-- or ROLLBACK;                           -- Undo all changes if something went wrong
```

### Key Commands

| Command | What It Does |
|---------|-------------|
| `BEGIN` | Starts a new transaction |
| `COMMIT` | Saves all changes made in the transaction |
| `ROLLBACK` | Undoes all changes made in the transaction |
| `SAVEPOINT name` | Creates a checkpoint you can roll back to |
| `ROLLBACK TO name` | Rolls back to the savepoint (not the entire transaction) |

---

## Normalization — Organizing Data Properly

Normalization is the process of organizing tables to reduce data duplication and improve data integrity.

### First Normal Form (1NF)

**Rule:** Each cell must contain a single value (no lists, no repeating groups).

```
BAD (violates 1NF):
+----+-------+-------------------+
| id | name  | phone_numbers     |
+----+-------+-------------------+
|  1 | Rahul | 9876543210, 91234 |
+----+-------+-------------------+

GOOD (1NF):
+----+-------+------------+
| id | name  | phone      |
+----+-------+------------+
|  1 | Rahul | 9876543210 |
|  1 | Rahul | 9123456789 |
+----+-------+------------+
```

### Second Normal Form (2NF)

**Rule:** Must be in 1NF + every non-key column must depend on the *entire* primary key (no partial dependencies).

### Third Normal Form (3NF)

**Rule:** Must be in 2NF + no non-key column should depend on another non-key column (no transitive dependencies).

```
BAD (violates 3NF):
+----+-------+---------+-----------+
| id | name  | city    | state     |
+----+-------+---------+-----------+
|  1 | Rahul | Bhopal  | MP        |
+----+-------+---------+-----------+
-- "state" depends on "city", not on "id"

GOOD (3NF): Split into two tables
students: (id, name, city_id)
cities: (id, city_name, state)
```

**Practical tip:** For most applications, normalizing to 3NF is sufficient. Over-normalization makes queries complex and slow.

---

## Schema Design Process

When designing a database for a real project, follow these steps:

1. **Identify entities** — What are the main "things"? (Students, Courses, Instructors)
2. **Define attributes** — What properties does each entity have? (name, email, fee)
3. **Choose primary keys** — Use auto-increment `id` for each table
4. **Identify relationships** — How do entities connect? (1:1, 1:M, M:N)
5. **Create junction tables** — For M:N relationships
6. **Apply constraints** — NOT NULL, UNIQUE, CHECK, DEFAULT
7. **Normalize** — Remove duplicates, fix dependencies (aim for 3NF)
8. **Add indexes** — On columns you search or filter frequently

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| Database | Organized data storage with rules and fast searching |
| DBMS | Software that manages the database (PostgreSQL, MySQL) |
| Primary Key | Uniquely identifies each row — never NULL, never duplicate |
| Foreign Key | Links one table to another |
| ACID | Guarantees reliable transactions |
| Normalization | Removes data duplication, keeps data consistent |
| 1NF / 2NF / 3NF | Progressive levels of table organization |

---

*TechPath Institute — Python Full Stack Development*
