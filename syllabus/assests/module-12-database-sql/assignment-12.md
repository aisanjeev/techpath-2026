# Module 12 — Assignment: Design and Query a Database

**Deadline:** End of Week 20
**Submission:** SQL file (.sql) + Python file (.py) + screenshots

---

## Task 1: Design an Institute Database — 30 marks

Design a database for a training institute with these tables:

**Tables:**
- `courses` (id, name, duration_months, fee, description)
- `students` (id, name, email, phone, course_id FK, batch, city, enrolled_date)
- `trainers` (id, name, specialization, email)
- `attendance` (id, student_id FK, date, status: present/absent)
- `marks` (id, student_id FK, subject, marks, max_marks)

**Requirements:**
- Write CREATE TABLE statements with proper constraints (PK, FK, NOT NULL, UNIQUE, CHECK, DEFAULT)
- Insert at least 10 students, 3 courses, 2 trainers, 20 attendance records, 30 marks records
- Use realistic Indian data (names, cities, phone numbers)

---

## Task 2: Write SQL Queries — 40 marks

Write queries for each (2 marks each, 20 queries):

1. All students enrolled in ADCA course
2. Students from Bhopal sorted by name
3. Total students per course
4. Average marks per subject
5. Students with attendance below 75%
6. Top 5 students by total marks
7. Students who enrolled in the last 3 months
8. Course-wise revenue (fee * student count)
9. Students who scored above average in Maths
10. Trainer and the courses they teach (JOIN)
11. Students with no attendance records (LEFT JOIN)
12. Monthly enrollment trend (GROUP BY month)
13. Students who passed all subjects (marks >= 33 in every subject)
14. City-wise student distribution with percentages
15. Update marks for a specific student
16. Delete students with 0 attendance
17. Add a new column `grade` to the marks table
18. Create an index on student email
19. Students absent more than 5 times
20. Complete report: name, course, total marks, percentage, attendance %

---

## Task 3: Python + SQLite — 30 marks

Write a Python script that:
- Creates the database and tables
- Inserts sample data programmatically
- Runs 5 of the above queries and prints formatted results
- Exports student results to CSV using Pandas
- Uses parameterized queries (? placeholders) — no f-strings in SQL

---

## Rubric

| Criteria | Excellent (Full) | Good (75%) | Needs Work (50%) |
|----------|-----------------|------------|------------------|
| Schema design | Proper PKs, FKs, constraints | Tables exist but weak constraints | Missing relationships |
| Queries | All 20 correct | 15+ correct | Less than 10 |
| JOINs | Multiple JOIN types used correctly | Basic JOINs work | No JOINs |
| Python integration | CRUD + export + parameterized | Basic CRUD works | Only create/insert |
| Data quality | Realistic, sufficient volume | Some data | Minimal or dummy |
