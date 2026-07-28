# Database Fundamentals

**Module 12 — Database Design & SQL | Topic 1**

---

## What is a Database?

A **database** is an organized collection of data stored so it can be easily accessed, managed, and updated.

| Without Database | With Database |
|-----------------|---------------|
| Data in scattered Excel files | All data in one organized place |
| Hard to search | Instant search (SQL queries) |
| No security | User roles and permissions |
| Can't handle many users | Thousands of users at once |
| Data gets duplicated | No duplicates (normalization) |

> **Think of a database like a smart filing cabinet** — organized drawers (tables), labeled folders (rows), with an index to find anything instantly.

---

## Types of Databases

| Type | How Data is Stored | Examples | Best For |
|------|-------------------|----------|----------|
| **Relational (SQL)** | Tables with rows and columns | MySQL, PostgreSQL, SQLite | Structured data, transactions |
| **NoSQL** | Documents, key-value, graphs | MongoDB, Redis, Firebase | Flexible data, real-time apps |

> **For beginners:** Start with relational databases (SQL). They're used in 80%+ of applications.

---

## Key Concepts

| Term | What It Means | Example |
|------|-------------|---------|
| **Database** | Collection of related tables | `school_db` |
| **Table** | Rows and columns (like Excel sheet) | `students` table |
| **Row (Record)** | One entry in a table | One student's data |
| **Column (Field)** | One attribute | `name`, `age`, `email` |
| **Primary Key (PK)** | Unique identifier for each row | `student_id` (1, 2, 3...) |
| **Foreign Key (FK)** | Links to another table's PK | `course_id` in students table |
| **Schema** | Structure/design of database | Tables, columns, types |
| **Query** | Question you ask the database | "Show all students above 20" |

---

## Database Design — Tables

### Example: School Database

**Students Table:**

| student_id (PK) | name | age | email | course_id (FK) |
|-----------------|------|-----|-------|----------------|
| 1 | Rahul | 20 | rahul@email.com | 101 |
| 2 | Priya | 22 | priya@email.com | 102 |
| 3 | Amit | 21 | amit@email.com | 101 |

**Courses Table:**

| course_id (PK) | course_name | duration | fee |
|----------------|-------------|----------|-----|
| 101 | ADCA | 12 months | 25000 |
| 102 | BCA | 36 months | 150000 |
| 103 | Web Dev | 6 months | 15000 |

> **Foreign Key:** `course_id` in Students table links to `course_id` in Courses table. This is called a **relationship**.

---

## Relationships Between Tables

| Type | Meaning | Example |
|------|---------|---------|
| **One-to-One** | One row in Table A links to exactly one in Table B | One student has one profile |
| **One-to-Many** | One row in Table A links to many in Table B | One course has many students |
| **Many-to-Many** | Many in Table A link to many in Table B | Students enroll in multiple courses, courses have multiple students |

> **Many-to-Many** needs a junction/bridge table:
> - `students` table + `courses` table + `enrollments` table (student_id, course_id)

---

## Data Types

| SQL Type | What It Stores | Example |
|----------|---------------|---------|
| `INT` | Whole numbers | 1, 42, -5 |
| `FLOAT` / `DECIMAL` | Decimal numbers | 3.14, 99.99 |
| `VARCHAR(n)` | Text (variable length, max n) | "Rahul" |
| `TEXT` | Long text | Paragraphs |
| `DATE` | Date | 2026-07-22 |
| `DATETIME` | Date + Time | 2026-07-22 14:30:00 |
| `BOOLEAN` | True/False | TRUE |

---

## Normalization — Organizing Data

**Normalization** = structuring data to reduce duplication.

### Without Normalization (Bad)

| student | course | teacher |
|---------|--------|---------|
| Rahul | ADCA | Mr. Sharma |
| Priya | ADCA | Mr. Sharma |
| Amit | BCA | Ms. Gupta |

> "Mr. Sharma" and "ADCA" are duplicated. If teacher changes, must update every row.

### With Normalization (Good)

**Students:** student_id, name, course_id
**Courses:** course_id, course_name, teacher_id
**Teachers:** teacher_id, teacher_name

> Now "Mr. Sharma" is stored once. Change in one place updates everywhere.

---

## CRUD Operations

| Operation | SQL Command | What It Does |
|-----------|------------|-------------|
| **C**reate | `INSERT` | Add new data |
| **R**ead | `SELECT` | Retrieve data |
| **U**pdate | `UPDATE` | Modify existing data |
| **D**elete | `DELETE` | Remove data |

---

## Summary

- **Database** = organized collection of data in tables
- **Relational databases** use tables with relationships (SQL)
- **Primary Key** = unique ID for each row
- **Foreign Key** = links to another table
- **Normalization** = reduce data duplication
- **CRUD** = Create, Read, Update, Delete
- Start with **MySQL** or **SQLite** for learning
