# Cheat Sheet — Database Design, SQL & NoSQL

**Module 04 | Quick Reference Card**

---

## SQL Data Types (MySQL / SQLite)

| Type | Use | MySQL | SQLite |
|------|-----|-------|--------|
| Auto-increment PK | Primary key | `INT AUTO_INCREMENT PRIMARY KEY` | `INTEGER PRIMARY KEY` |
| Integer | Whole numbers | `INT` | `INTEGER` |
| Decimal | Money/precise | `DECIMAL(10,2)` | `REAL` |
| Text (fixed max) | Short text | `VARCHAR(100)` | `TEXT` |
| Text (unlimited) | Long text | `TEXT` | `TEXT` |
| Boolean | True/False | `BOOLEAN` | `INTEGER` (0/1) |
| Date | Date | `DATE` | `TEXT` |
| Date + time | Timestamp | `DATETIME` | `TEXT` |
| JSON | Structured data | `JSON` | `TEXT` (use json functions) |

## DDL Quick Reference

```sql
-- Create (MySQL)
CREATE TABLE t (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) NOT NULL);
-- Create (SQLite)
-- CREATE TABLE t (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL);

-- Add column
ALTER TABLE t ADD COLUMN email VARCHAR(150) UNIQUE;

-- Drop column
ALTER TABLE t DROP COLUMN email;

-- Rename column (MySQL 8.0+)
ALTER TABLE t RENAME COLUMN name TO full_name;

-- Drop table
DROP TABLE IF EXISTS t;

-- Truncate (delete all rows, reset IDs) -- MySQL only
TRUNCATE TABLE t;
-- SQLite: DELETE FROM t;
```

## DML Quick Reference

```sql
-- Insert
INSERT INTO t (name, email) VALUES ('Rahul', 'r@e.com');

-- Insert multiple
INSERT INTO t (name) VALUES ('Priya'), ('Amit'), ('Sneha');

-- Update (always use WHERE!)
UPDATE t SET city = 'Pune' WHERE id = 1;

-- Delete (always use WHERE!)
DELETE FROM t WHERE id = 5;

-- Upsert (MySQL)
INSERT INTO t (email, name) VALUES ('r@e.com', 'Rahul')
ON DUPLICATE KEY UPDATE name = VALUES(name);
-- Upsert (SQLite)
-- INSERT OR REPLACE INTO t (email, name) VALUES ('r@e.com', 'Rahul');
```

## SELECT Patterns

```sql
-- Basic
SELECT name, city FROM students WHERE city = 'Bhopal';

-- Sorting + Pagination
SELECT * FROM students ORDER BY name LIMIT 10 OFFSET 20;

-- Aggregation
SELECT city, COUNT(*) AS cnt FROM students GROUP BY city HAVING cnt > 3;

-- Subquery
SELECT * FROM students WHERE fee > (SELECT AVG(fee) FROM students);

-- CTE
WITH top AS (SELECT * FROM students WHERE fee > 20000)
SELECT city, COUNT(*) FROM top GROUP BY city;
```

## JOIN Types

| JOIN | Returns |
|------|---------|
| `INNER JOIN` | Matching rows only |
| `LEFT JOIN` | All left + matching right (NULL if no match) |
| `RIGHT JOIN` | All right + matching left |
| `FULL OUTER JOIN` | All rows from both |
| `CROSS JOIN` | Every combination |

```sql
SELECT s.name, c.title
FROM students s
INNER JOIN enrollments e ON s.id = e.student_id
INNER JOIN courses c ON e.course_id = c.id;
```

## Constraints

| Constraint | Syntax |
|-----------|--------|
| Primary Key | `id INT AUTO_INCREMENT PRIMARY KEY` |
| Not Null | `name VARCHAR(100) NOT NULL` |
| Unique | `email VARCHAR(150) UNIQUE` |
| Default | `city VARCHAR(50) DEFAULT 'Bhopal'` |
| Check | `CHECK (price >= 0)` |
| Foreign Key | `REFERENCES table(col) ON DELETE CASCADE` |

## MySQL JSON

```sql
-- Access key (quoted / unquoted text)
SELECT details->'$.brand', details->>'$.brand' FROM products;

-- Filter
SELECT * FROM products WHERE details->>'$.brand' = 'HP';

-- Contains
SELECT * FROM products WHERE JSON_CONTAINS(details, '"16GB"', '$.ram');

-- Key exists
SELECT * FROM products WHERE JSON_CONTAINS_PATH(details, 'one', '$.features');
```

## SQLite JSON

```sql
SELECT json_extract(details, '$.brand') FROM products;
SELECT * FROM products WHERE json_extract(details, '$.brand') = 'HP';
```

## Indexes

```sql
CREATE INDEX idx_name ON students(city);
CREATE UNIQUE INDEX idx_email ON students(email);
CREATE INDEX idx_composite ON students(city, name);
```

## SQLAlchemy 2.0

```python
# Model
class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

# Create
db.add(Student(name="Rahul")); await db.flush()

# Read
stmt = select(Student).where(Student.city == "Bhopal")
result = await db.execute(stmt)
students = result.scalars().all()

# Update
student = await db.get(Student, 1)
student.city = "Pune"
await db.commit()

# Delete
await db.delete(student); await db.commit()
```

## Alembic

```bash
alembic revision --autogenerate -m "add column"
alembic upgrade head
alembic downgrade -1
alembic current
```

## MongoDB (PyMongo)

```python
# Insert
db.students.insert_one({"name": "Rahul", "city": "Bhopal"})

# Find
db.students.find({"city": "Bhopal"})
db.students.find_one({"email": "r@e.com"})

# Update
db.students.update_one({"_id": id}, {"$set": {"city": "Pune"}})

# Delete
db.students.delete_one({"_id": id})

# Aggregation
db.students.aggregate([
    {"$match": {"is_active": True}},
    {"$group": {"_id": "$city", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
])
```

## MongoDB Operators

| Operator | Example |
|----------|---------|
| `$gt/$gte` | `{"fee": {"$gt": 15000}}` |
| `$lt/$lte` | `{"age": {"$lt": 25}}` |
| `$in` | `{"city": {"$in": ["Bhopal","Pune"]}}` |
| `$or` | `{"$or": [{...}, {...}]}` |
| `$set` | `{"$set": {"name": "New"}}` |
| `$inc` | `{"$inc": {"fee": 5000}}` |
| `$push` | `{"$push": {"tags": "new"}}` |

## Redis

```python
r = redis.Redis(decode_responses=True)

# Strings
r.set("key", "value", ex=300)   # 5 min expiry
r.get("key")
r.incr("counter")

# Hash
r.hset("user:1", mapping={"name": "Rahul", "city": "Bhopal"})
r.hgetall("user:1")

# List
r.rpush("queue", "task1", "task2")
r.lpop("queue")

# Set
r.sadd("online", "rahul", "priya")
r.sismember("online", "rahul")

# Sorted Set
r.zadd("scores", {"Rahul": 850, "Priya": 920})
r.zrevrange("scores", 0, 2, withscores=True)

# Key management
r.exists("key"); r.delete("key"); r.ttl("key")
```

## ACID Properties

| Property | Meaning |
|----------|---------|
| **A**tomicity | All or nothing |
| **C**onsistency | Valid state to valid state |
| **I**solation | No interference between transactions |
| **D**urability | Committed = permanent |

---

*TechPath Institute — Python Full Stack Development*
