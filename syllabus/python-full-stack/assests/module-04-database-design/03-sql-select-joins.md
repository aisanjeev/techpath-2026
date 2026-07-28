# SQL SELECT, JOINs & Advanced Queries

**Module 04 — Database Design, SQL & NoSQL | Topic 3**

---

## The SELECT Statement

SELECT is the most-used SQL command. It retrieves data from one or more tables.

### Basic Syntax

```sql
SELECT columns
FROM table
WHERE condition
ORDER BY column
LIMIT count;
```

### Selecting Columns

```sql
-- Select all columns
SELECT * FROM students;

-- Select specific columns
SELECT name, email, city FROM students;

-- Rename columns with aliases
SELECT name AS student_name, email AS contact_email FROM students;

-- Remove duplicates
SELECT DISTINCT city FROM students;

-- Count rows
SELECT COUNT(*) AS total_students FROM students;
```

---

## WHERE Clause — Filtering Rows

```sql
-- Exact match
SELECT * FROM students WHERE city = 'Bhopal';

-- Not equal
SELECT * FROM students WHERE city != 'Bhopal';
SELECT * FROM students WHERE city <> 'Bhopal';  -- Same thing

-- Comparison
SELECT * FROM courses WHERE price > 20000;
SELECT * FROM courses WHERE price >= 15000 AND price <= 25000;

-- BETWEEN (inclusive on both ends)
SELECT * FROM courses WHERE price BETWEEN 15000 AND 25000;

-- IN (match any value in a list)
SELECT * FROM students WHERE city IN ('Bhopal', 'Pune', 'Delhi');

-- NOT IN
SELECT * FROM students WHERE city NOT IN ('Mumbai', 'Chennai');

-- LIKE (pattern matching)
SELECT * FROM students WHERE name LIKE 'R%';       -- Starts with R
SELECT * FROM students WHERE email LIKE '%@gmail%'; -- Contains @gmail
SELECT * FROM students WHERE name LIKE '_____';     -- Exactly 5 characters

-- IS NULL / IS NOT NULL
SELECT * FROM students WHERE phone IS NULL;
SELECT * FROM students WHERE phone IS NOT NULL;

-- Combining conditions
SELECT * FROM students
WHERE city = 'Bhopal' AND is_active = TRUE;

SELECT * FROM students
WHERE city = 'Bhopal' OR city = 'Pune';

SELECT * FROM students
WHERE NOT (city = 'Delhi');
```

---

## ORDER BY — Sorting Results

```sql
-- Sort ascending (default)
SELECT * FROM students ORDER BY name;
SELECT * FROM students ORDER BY name ASC;

-- Sort descending
SELECT * FROM courses ORDER BY price DESC;

-- Sort by multiple columns
SELECT * FROM students ORDER BY city ASC, name ASC;

-- Sort by column position (not recommended but works)
SELECT name, city, fee_paid FROM students ORDER BY 3 DESC;
```

---

## LIMIT and OFFSET — Pagination

```sql
-- Get first 10 rows
SELECT * FROM students ORDER BY id LIMIT 10;

-- Skip first 10, get next 10 (page 2)
SELECT * FROM students ORDER BY id LIMIT 10 OFFSET 10;

-- Page 3
SELECT * FROM students ORDER BY id LIMIT 10 OFFSET 20;
```

**Pagination formula:** `OFFSET = (page_number - 1) * page_size`

---

## Aggregate Functions

Aggregate functions calculate a single value from a set of rows.

| Function | What It Does | Example |
|----------|-------------|---------|
| `COUNT()` | Number of rows | `COUNT(*)` or `COUNT(name)` |
| `SUM()` | Total of a numeric column | `SUM(fee_paid)` |
| `AVG()` | Average value | `AVG(price)` |
| `MIN()` | Smallest value | `MIN(price)` |
| `MAX()` | Largest value | `MAX(price)` |

```sql
SELECT
    COUNT(*) AS total_students,
    SUM(fee_paid) AS total_fees,
    AVG(fee_paid) AS average_fee,
    MIN(fee_paid) AS lowest_fee,
    MAX(fee_paid) AS highest_fee
FROM students;
```

---

## GROUP BY — Grouping Data

GROUP BY groups rows with the same values and applies aggregate functions to each group.

```sql
-- Count students per city
SELECT city, COUNT(*) AS student_count
FROM students
GROUP BY city;

-- Total fees collected per city
SELECT city, SUM(fee_paid) AS total_fees
FROM students
GROUP BY city
ORDER BY total_fees DESC;

-- Average course price per instructor
SELECT instructor_id, AVG(price) AS avg_price
FROM courses
GROUP BY instructor_id;
```

### HAVING — Filtering Groups

`WHERE` filters rows. `HAVING` filters groups (after GROUP BY).

```sql
-- Cities with more than 5 students
SELECT city, COUNT(*) AS student_count
FROM students
GROUP BY city
HAVING COUNT(*) > 5;

-- Instructors with average course price above ₹20,000
SELECT instructor_id, AVG(price) AS avg_price
FROM courses
GROUP BY instructor_id
HAVING AVG(price) > 20000;
```

**Execution order of a SELECT statement:**

```
1. FROM      -- Which table?
2. WHERE     -- Filter individual rows
3. GROUP BY  -- Group the remaining rows
4. HAVING    -- Filter groups
5. SELECT    -- Choose columns
6. ORDER BY  -- Sort the result
7. LIMIT     -- Restrict output rows
```

---

## JOINs — Combining Tables

JOINs are one of the most powerful features of SQL. They let you combine data from multiple tables.

### Sample Data for Examples

```
students:                          courses:
+----+---------+----------+        +----+---------------+-------+
| id | name    | city     |        | id | title         | price |
+----+---------+----------+        +----+---------------+-------+
|  1 | Rahul   | Bhopal   |        |  1 | Python        | 25000 |
|  2 | Priya   | Pune     |        |  2 | React         | 20000 |
|  3 | Amit    | Delhi    |        |  3 | Data Science  | 30000 |
|  4 | Sneha   | Bhopal   |        +----+---------------+-------+
+----+---------+----------+

enrollments:
+----+------------+-----------+
| id | student_id | course_id |
+----+------------+-----------+
|  1 |          1 |         1 |
|  2 |          1 |         2 |
|  3 |          2 |         1 |
|  4 |          3 |         2 |
+----+------------+-----------+
```

Note: Sneha (id=4) has no enrollments. Data Science (id=3) has no enrollments.

### INNER JOIN

Returns only rows that have matching values in **both** tables.

```sql
SELECT s.name, c.title
FROM students s
INNER JOIN enrollments e ON s.id = e.student_id
INNER JOIN courses c ON e.course_id = c.id;
```

**Result:**

| name  | title  |
|-------|--------|
| Rahul | Python |
| Rahul | React  |
| Priya | Python |
| Amit  | React  |

Sneha is excluded (no enrollment). Data Science is excluded (no student enrolled).

### LEFT JOIN (LEFT OUTER JOIN)

Returns all rows from the **left table**, plus matching rows from the right. If no match, right side is NULL.

```sql
SELECT s.name, c.title
FROM students s
LEFT JOIN enrollments e ON s.id = e.student_id
LEFT JOIN courses c ON e.course_id = c.id;
```

**Result:**

| name  | title  |
|-------|--------|
| Rahul | Python |
| Rahul | React  |
| Priya | Python |
| Amit  | React  |
| Sneha | NULL   |

Sneha appears with NULL for course — she exists in students but has no enrollment.

### RIGHT JOIN (RIGHT OUTER JOIN)

Returns all rows from the **right table**, plus matching rows from the left. If no match, left side is NULL.

```sql
SELECT s.name, c.title
FROM students s
RIGHT JOIN enrollments e ON s.id = e.student_id
RIGHT JOIN courses c ON e.course_id = c.id;
```

### FULL OUTER JOIN

Returns all rows from **both** tables. NULLs where there is no match.

```sql
SELECT s.name, c.title
FROM students s
FULL OUTER JOIN enrollments e ON s.id = e.student_id
FULL OUTER JOIN courses c ON e.course_id = c.id;
```

### CROSS JOIN

Returns the **Cartesian product** — every row of Table A paired with every row of Table B.

```sql
SELECT s.name, c.title
FROM students s
CROSS JOIN courses c;
-- 4 students x 3 courses = 12 rows
```

### SELF JOIN

A table joined with itself. Useful for hierarchical data.

```sql
-- Find employees and their managers
SELECT
    e.name AS employee,
    m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;
```

### JOIN Summary

| JOIN Type | Returns |
|-----------|---------|
| `INNER JOIN` | Only matching rows from both tables |
| `LEFT JOIN` | All rows from left + matches from right |
| `RIGHT JOIN` | All rows from right + matches from left |
| `FULL OUTER JOIN` | All rows from both tables |
| `CROSS JOIN` | Every combination of rows |
| `SELF JOIN` | Table joined with itself |

---

## Subqueries

A subquery is a query nested inside another query.

```sql
-- Students enrolled in the most expensive course
SELECT name FROM students
WHERE id IN (
    SELECT student_id FROM enrollments
    WHERE course_id = (
        SELECT id FROM courses ORDER BY price DESC LIMIT 1
    )
);

-- Courses with above-average price
SELECT title, price FROM courses
WHERE price > (SELECT AVG(price) FROM courses);

-- Using subquery in FROM (derived table)
SELECT city, avg_fee
FROM (
    SELECT city, AVG(fee_paid) AS avg_fee
    FROM students
    GROUP BY city
) AS city_stats
WHERE avg_fee > 15000;
```

---

## Common Table Expressions (CTEs)

CTEs are named temporary result sets that make complex queries readable.

```sql
-- CTE syntax
WITH cte_name AS (
    SELECT ...
)
SELECT * FROM cte_name;
```

**Example: Student enrollment summary**

```sql
WITH enrollment_counts AS (
    SELECT
        s.id,
        s.name,
        s.city,
        COUNT(e.id) AS courses_enrolled
    FROM students s
    LEFT JOIN enrollments e ON s.id = e.student_id
    GROUP BY s.id, s.name, s.city
),
city_stats AS (
    SELECT
        city,
        COUNT(*) AS students_in_city,
        AVG(courses_enrolled) AS avg_courses
    FROM enrollment_counts
    GROUP BY city
)
SELECT * FROM city_stats ORDER BY students_in_city DESC;
```

**Multiple CTEs:** Chain them with commas. Each CTE can reference the ones above it.

---

## Indexes — Making Queries Fast

An index is like the index at the back of a textbook — it helps the database find rows quickly without scanning the entire table.

```sql
-- Create an index on a single column
CREATE INDEX idx_students_city ON students(city);

-- Create a unique index
CREATE UNIQUE INDEX idx_students_email ON students(email);

-- Create a composite index (multiple columns)
CREATE INDEX idx_enrollments_student_course
ON enrollments(student_id, course_id);

-- Drop an index
DROP INDEX idx_students_city;
```

### When to Use Indexes

| Use Index | Do Not Index |
|-----------|-------------|
| Columns in WHERE clauses | Columns you rarely search on |
| Columns in JOIN conditions | Very small tables (< 1000 rows) |
| Columns in ORDER BY | Columns with very few unique values (e.g., boolean) |
| Foreign key columns | Tables with heavy INSERT/UPDATE operations |

**Trade-off:** Indexes speed up reads but slow down writes (because the index must be updated too).

---

## Window Functions (Bonus)

Window functions perform calculations across a set of rows related to the current row — without grouping them.

```sql
-- Rank students by fee paid
SELECT
    name,
    city,
    fee_paid,
    RANK() OVER (ORDER BY fee_paid DESC) AS fee_rank
FROM students;

-- Running total of enrollments by date
SELECT
    enrolled_on,
    COUNT(*) AS daily_enrollments,
    SUM(COUNT(*)) OVER (ORDER BY enrolled_on) AS running_total
FROM enrollments
GROUP BY enrolled_on;

-- Top student per city
SELECT name, city, fee_paid
FROM (
    SELECT
        name, city, fee_paid,
        ROW_NUMBER() OVER (PARTITION BY city ORDER BY fee_paid DESC) AS rn
    FROM students
) ranked
WHERE rn = 1;
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| SELECT | Retrieves data from tables |
| WHERE | Filters individual rows |
| ORDER BY | Sorts results |
| LIMIT/OFFSET | Pagination |
| GROUP BY | Groups rows for aggregation |
| HAVING | Filters grouped results |
| INNER JOIN | Only matching rows |
| LEFT JOIN | All left rows + matching right |
| Subqueries | Queries inside queries |
| CTEs | Named temporary result sets |
| Indexes | Speed up searches on large tables |

---

*TechPath Institute — Python Full Stack Development*
