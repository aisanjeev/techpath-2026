# Quiz: Database Design & SQL

**Module 12 | 12 Questions | Pass Mark: 60%**

---

## Q1. What does SQL stand for?
- A) Simple Query Language
- B) Structured Query Language ✅
- C) System Query Logic
- D) Standard Question Language

> **Explanation:** SQL = Structured Query Language — used to manage relational databases.

---

## Q2. What is a Primary Key?
- A) The first column in a table
- B) A unique identifier for each row ✅
- C) A password for the database
- D) The most important data

> **Explanation:** A Primary Key uniquely identifies each row. Cannot be NULL or duplicated.

---

## Q3. Which SQL command retrieves data?
- A) GET
- B) FETCH
- C) SELECT ✅
- D) READ

> **Explanation:** `SELECT * FROM students;` gets all rows and columns.

---

## Q4. What does WHERE do?
- A) Sorts results
- B) Filters rows based on a condition ✅
- C) Groups results
- D) Limits output

> **Explanation:** WHERE filters rows: `SELECT * FROM students WHERE marks > 80;`

---

## Q5. Difference between DELETE and DROP?
- A) No difference
- B) DELETE removes rows, DROP removes entire table ✅
- C) DELETE is faster
- D) DROP removes rows

> **Explanation:** DELETE removes specific rows. DROP removes the table itself permanently.

---

## Q6. What does COUNT(*) do?
- A) Counts columns
- B) Counts the number of rows ✅
- C) Counts characters
- D) Counts tables

> **Explanation:** `COUNT(*)` counts rows. `SELECT COUNT(*) FROM students;` returns total students.

---

## Q7. What is a Foreign Key?
- A) A key from another country
- B) A column that links to another table's Primary Key ✅
- C) An encrypted key
- D) A backup key

> **Explanation:** Foreign Keys link tables together. `course_id` in students references courses table.

---

## Q8. What does INNER JOIN return?
- A) All rows from both tables
- B) Only rows that match in both tables ✅
- C) All from left table
- D) All from right table

> **Explanation:** INNER JOIN returns only rows with matching values in both tables.

---

## Q9. Which clause sorts results?
- A) SORT BY
- B) ORDER BY ✅
- C) ARRANGE BY
- D) GROUP BY

> **Explanation:** `ORDER BY marks DESC` sorts highest first. `ASC` for ascending (A-Z).

---

## Q10. What is normalization?
- A) Making data normal
- B) Organizing data to reduce duplication ✅
- C) Converting data types
- D) Encrypting data

> **Explanation:** Store data once, reference with Foreign Keys. Avoids update anomalies.

---

## Q11. What does GROUP BY do?
- A) Groups columns together
- B) Groups rows by a column value for aggregate calculations ✅
- C) Sorts data into groups
- D) Creates new tables

> **Explanation:** `SELECT course, AVG(marks) FROM students GROUP BY course;` gets average per course.

---

## Q12. Why always use WHERE with UPDATE/DELETE?
- A) It runs faster
- B) Without it, ALL rows get affected ✅
- C) It's required syntax
- D) It prevents errors

> **Explanation:** `UPDATE students SET marks = 0;` without WHERE changes ALL students' marks to 0!

---

## Answer Key

| Q  | Answer | Q  | Answer |
|----|--------|----|--------|
| 1  | B      | 7  | B      |
| 2  | B      | 8  | B      |
| 3  | C      | 9  | B      |
| 4  | B      | 10 | B      |
| 5  | B      | 11 | B      |
| 6  | B      | 12 | B      |
