# Cheat Sheet: Database Design & SQL

**Module 12 — Quick Reference**

---

## CRUD Commands

| Operation | SQL | Example |
|-----------|-----|---------|
| Create | INSERT | `INSERT INTO t (col) VALUES ('val');` |
| Read | SELECT | `SELECT * FROM t WHERE col > 5;` |
| Update | UPDATE | `UPDATE t SET col = 'val' WHERE id = 1;` |
| Delete | DELETE | `DELETE FROM t WHERE id = 1;` |

---

## SELECT Clauses

```sql
SELECT columns
FROM table
WHERE condition
GROUP BY column
HAVING group_condition
ORDER BY column DESC
LIMIT 10;
```

---

## WHERE Operators

| Operator | Example |
|----------|---------|
| `=`, `!=` | `WHERE age = 20` |
| `>`, `<`, `>=`, `<=` | `WHERE marks > 80` |
| `AND`, `OR` | `WHERE a > 5 AND b < 10` |
| `IN` | `WHERE age IN (20, 21, 22)` |
| `BETWEEN` | `WHERE marks BETWEEN 80 AND 90` |
| `LIKE` | `WHERE name LIKE 'R%'` |
| `IS NULL` | `WHERE email IS NULL` |

---

## Aggregate Functions

| Function | What |
|----------|------|
| `COUNT(*)` | Number of rows |
| `SUM(col)` | Total |
| `AVG(col)` | Average |
| `MAX(col)` | Highest |
| `MIN(col)` | Lowest |

---

## JOINs

| Type | Returns |
|------|---------|
| INNER | Matches in both |
| LEFT | All left + matches |
| RIGHT | All right + matches |

```sql
SELECT s.name, c.course_name
FROM students s
INNER JOIN courses c ON s.course_id = c.course_id;
```

---

## Keys

| Key | Purpose |
|-----|---------|
| PRIMARY KEY | Unique row ID |
| FOREIGN KEY | Links to another table |
| UNIQUE | No duplicates |

---

## Data Types

| Type | For |
|------|-----|
| INT | Whole numbers |
| DECIMAL | Money/precise |
| VARCHAR(n) | Text (max n) |
| TEXT | Long text |
| DATE | Dates |
| BOOLEAN | True/False |
