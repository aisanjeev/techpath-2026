# Quiz — Database Design, SQL & NoSQL

**Module 04 | 15 Questions**

---

### Q1. What does ACID stand for in database transactions?

- A) Addition, Calculation, Integration, Deletion
- B) Atomicity, Consistency, Isolation, Durability ✅
- C) Automated, Centralized, Independent, Distributed
- D) Access, Control, Identity, Data

> **Explanation:** ACID stands for Atomicity (all or nothing), Consistency (valid state transitions), Isolation (concurrent transactions don't interfere), and Durability (committed data survives crashes).

---

### Q2. Which key type creates a link between two tables in a relational database?

- A) Primary Key
- B) Candidate Key
- C) Foreign Key ✅
- D) Surrogate Key

> **Explanation:** A Foreign Key references the Primary Key of another table, creating a relationship between the two tables.

---

### Q3. What does the SQL command `TRUNCATE TABLE students` do?

- A) Deletes the table structure and all data permanently
- B) Removes all rows but keeps the table structure intact ✅
- C) Deletes only rows where is_active is FALSE
- D) Renames the table to students_backup

> **Explanation:** TRUNCATE removes all rows from a table and resets auto-increment counters, but the table structure (columns, constraints) remains intact. DROP TABLE would remove the structure too.

---

### Q4. Which JOIN type returns ALL rows from the left table, even if there is no matching row in the right table?

- A) INNER JOIN
- B) CROSS JOIN
- C) LEFT JOIN ✅
- D) SELF JOIN

> **Explanation:** LEFT JOIN (LEFT OUTER JOIN) returns all rows from the left table. If there is no matching row in the right table, the right-side columns are filled with NULL.

---

### Q5. In SQL, what is the correct order of clauses in a SELECT statement?

- A) SELECT, WHERE, FROM, ORDER BY, GROUP BY
- B) FROM, SELECT, WHERE, GROUP BY, ORDER BY
- C) SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY ✅
- D) SELECT, FROM, GROUP BY, WHERE, ORDER BY, HAVING

> **Explanation:** The correct order is SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY, LIMIT. The database executes them in a different order (FROM first), but the written syntax follows this sequence.

---

### Q6. What is the purpose of an INDEX in a database?

- A) To enforce unique values in a column
- B) To speed up data retrieval on frequently searched columns ✅
- C) To create a backup of the table
- D) To link two tables together

> **Explanation:** An index creates a data structure that allows the database to find rows quickly without scanning the entire table, similar to an index at the back of a textbook.

---

### Q7. In MySQL, how do you extract a JSON field value as plain text from a column called `details`?

- A) details->'$.brand'
- B) details->>'$.brand' ✅
- C) json_extract(details, 'brand')
- D) details['brand']

> **Explanation:** In MySQL, the ->> operator (or JSON_UNQUOTE(JSON_EXTRACT())) returns the JSON field value as unquoted text. The -> operator returns it as a quoted JSON element. For example, details->>'$.brand' returns HP (text), while details->'$.brand' returns "HP" (JSON).

---

### Q8. In SQLAlchemy 2.0, which is the correct way to query all students from Bhopal?

- A) db.session.query(Student).filter_by(city='Bhopal').all()
- B) select(Student).where(Student.city == 'Bhopal') ✅
- C) Student.objects.filter(city='Bhopal')
- D) db.find({'city': 'Bhopal'})

> **Explanation:** SQLAlchemy 2.0 uses the select() function with .where() for filtering. The session.query() style (option A) is the older 1.x pattern that is now deprecated.

---

### Q9. What does `ON DELETE CASCADE` do when applied to a Foreign Key?

- A) Prevents deletion of the parent row
- B) Sets the foreign key column to NULL when the parent is deleted
- C) Automatically deletes child rows when the parent row is deleted ✅
- D) Logs the deletion in an audit table

> **Explanation:** ON DELETE CASCADE means when the referenced (parent) row is deleted, all rows in the child table that reference it are automatically deleted too.

---

### Q10. Which MongoDB operator is used to add a value to an array field?

- A) $set
- B) $inc
- C) $push ✅
- D) $addField

> **Explanation:** $push adds a value to an array field. $set replaces the entire field value, $inc increments a numeric field, and $addField does not exist in MongoDB.

---

### Q11. What is the purpose of `session.flush()` in SQLAlchemy?

- A) It permanently saves all changes to the database
- B) It sends SQL to the database but does NOT finalize the transaction ✅
- C) It clears all pending changes without saving
- D) It closes the database connection

> **Explanation:** flush() sends pending SQL operations to the database (so auto-generated values like IDs become available) but does not commit the transaction. You can still rollback after a flush. commit() finalizes changes permanently.

---

### Q12. In Redis, what happens to a key when its TTL (Time To Live) expires?

- A) The key's value is set to NULL
- B) The key is automatically deleted from memory ✅
- C) The key is moved to a backup database
- D) An error is raised on the next access

> **Explanation:** When a Redis key's TTL expires, it is automatically removed from memory. Any subsequent GET on that key returns None (null). This is the foundation of Redis caching — data expires and must be re-fetched from the primary database.

---

### Q13. Which Alembic command generates a new migration file by comparing your models to the database?

- A) alembic upgrade head
- B) alembic revision --autogenerate -m "description" ✅
- C) alembic downgrade -1
- D) alembic init migrations

> **Explanation:** alembic revision --autogenerate compares your SQLAlchemy models to the actual database schema and generates a migration file with the differences. alembic upgrade head applies migrations, downgrade -1 rolls back, and init sets up Alembic for the first time.

---

### Q14. In a MongoDB aggregation pipeline, which stage is equivalent to SQL's GROUP BY?

- A) $match
- B) $project
- C) $group ✅
- D) $sort

> **Explanation:** $group groups documents by a specified field and can apply accumulator operations like $sum, $avg, $count. It is the MongoDB equivalent of SQL's GROUP BY clause.

---

### Q15. Which Redis data structure is best suited for implementing a real-time leaderboard?

- A) String
- B) Hash
- C) List
- D) Sorted Set ✅

> **Explanation:** Sorted Sets store members with a numeric score and keep them automatically ordered. This makes them perfect for leaderboards — you can get top N players, find a player's rank, and update scores, all in O(log n) time.

---

**Score Guide:**
- 13-15 correct: Excellent — you have a strong understanding of databases
- 10-12 correct: Good — review the topics you missed
- 7-9 correct: Fair — revisit the notes and practice more SQL queries
- Below 7: Needs improvement — go through each topic again carefully

---

*TechPath Institute — Python Full Stack Development*
