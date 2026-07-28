# Module 04 — Assignment: Database Design, SQL & NoSQL

**Deadline:** End of Module 04
**Total Marks:** 100
**Submission:** SQL file (.sql) + Python files (.py) + screenshots + MongoDB export

---

## Task 1: Design and Build a TechPath Institute Database — 30 marks

Design and implement a MySQL (or SQLite) database for TechPath Institute's student management system.

**Required Tables:**
- `courses` (id, name, duration_months, fee, category, description, is_active, created_at)
- `trainers` (id, name, email, phone, specialization, city, experience_years, created_at)
- `students` (id, name, email, phone, city, date_of_birth, batch, is_active, enrolled_date, created_at)
- `enrollments` (id, student_id FK, course_id FK, trainer_id FK, enrolled_date, status, grade)
- `payments` (id, student_id FK, course_id FK, amount, payment_date, payment_method, receipt_number)

**Requirements:**

1. **Schema Design (10 marks)**
   - Write CREATE TABLE statements with proper data types
   - Add all constraints: PRIMARY KEY, FOREIGN KEY, NOT NULL, UNIQUE, CHECK, DEFAULT
   - Use ON DELETE CASCADE or SET NULL where appropriate
   - Add a composite UNIQUE constraint on enrollments (student_id, course_id)

2. **Sample Data (10 marks)**
   - Insert at least 5 courses (Python Full Stack, Data Science, Java, Web Dev, DevOps)
   - Insert at least 4 trainers with Indian names and cities
   - Insert at least 12 students from cities like Bhopal, Delhi, Pune, Indore, Hyderabad
   - Insert at least 15 enrollments (some students in multiple courses)
   - Insert at least 15 payment records with different payment methods (UPI, Cash, Card, Net Banking)

3. **ERD Diagram (10 marks)**
   - Draw an Entity-Relationship Diagram showing all tables, columns, and relationships
   - Use dbdiagram.io, draw.io, or paper sketch (photograph)
   - Clearly mark PK, FK, and relationship types (1:1, 1:M, M:M)

---

## Task 2: Write SQL Queries — 25 marks

Write **at least 15 SQL queries** covering the following categories. Each query must include a comment explaining what it does.

**Basic Queries (5 marks)**
1. All students sorted by name
2. Students from a specific city
3. Active courses with fee above Rs. 20,000
4. Students enrolled in the last 3 months
5. Top 5 most recently enrolled students

**Aggregate & GROUP BY (5 marks)**
6. Total number of students per city
7. Average course fee by category
8. Total revenue collected per payment method
9. Course with the highest number of enrollments
10. Cities with more than 2 students (use HAVING)

**JOINs (5 marks)**
11. Student name with course name and trainer name (3-table JOIN)
12. All courses with enrollment count (include courses with zero enrollments using LEFT JOIN)
13. Students from the same city (SELF JOIN)
14. Complete student report: name, city, course, trainer, amount paid, balance

**Subqueries & CTEs (5 marks)**
15. Students enrolled in courses costing above average
16. Student who has paid the most overall
17. Courses with no enrollments (use NOT IN or NOT EXISTS)
18. Revenue summary per course using a CTE (enrolled count, total collected, outstanding)

**CASE Expressions (5 marks)**
19. Categorize each student's payment status as "Fully Paid", "Partially Paid", or "Unpaid"
20. Classify courses into fee tiers: "Premium" (30K+), "Standard" (20K+), "Value" (below 20K)

---

## Task 3: Python CRUD App with SQLAlchemy ORM — 25 marks

Build a command-line Python application using SQLAlchemy ORM.

**Requirements:**

1. **Models (8 marks)**
   - Define at least 3 models: `Student`, `Course`, `Enrollment`
   - Set up proper relationships (one-to-many, many-to-many through Enrollment)
   - Use appropriate column types and constraints

2. **CRUD Operations (10 marks)**
   - **Create:** Add new students, courses, and enrollments
   - **Read:** List all students, filter by city, show student with enrolled courses
   - **Update:** Update student city, mark enrollment as completed with a grade
   - **Delete:** Remove a student (with cascade delete of enrollments)

3. **Alembic Migrations (7 marks)**
   - Initialize Alembic in your project
   - Generate an initial migration from your models
   - Apply the migration with `alembic upgrade head`
   - Add a new column (e.g., `batch` to students), generate and apply a second migration
   - Take a screenshot of `alembic history` output

**Deliverables:** Python files, `alembic/` folder, screenshots of the CLI app running

---

## Task 4: MongoDB Document Design & PyMongo CRUD — 20 marks

Build a student feedback system using MongoDB and PyMongo.

**Requirements:**

1. **Document Design (5 marks)**
   - Design a `feedbacks` collection with this structure:
     ```json
     {
       "student_name": "Rahul Sharma",
       "student_email": "rahul@techpath.in",
       "course": "Python Full Stack",
       "trainer": "Ananya Reddy",
       "rating": 4,
       "comments": "Very helpful practical sessions",
       "topics_covered": ["Python basics", "Django", "REST APIs"],
       "submitted_at": "2026-06-15T10:30:00"
     }
     ```
   - Insert at least 10 feedback documents with varied ratings (1-5), courses, and trainers

2. **CRUD Operations (8 marks)**
   - **Insert:** Add single and multiple feedback documents
   - **Find:** All feedbacks for a specific course, feedbacks with rating >= 4, search by trainer name
   - **Update:** Update a student's rating, add a new topic to `topics_covered` array using `$push`
   - **Delete:** Remove feedback by student email

3. **Aggregation Pipeline (7 marks)**
   Write aggregation queries to find:
   - Average rating per course (sorted best to worst)
   - Average rating per trainer
   - Number of feedbacks per rating value (1-5 distribution)
   - Courses with average rating below 3 (needs improvement)

**Deliverables:** Python script, screenshot of MongoDB Compass showing the data, console output

---

## Rubric

| Criterion | Excellent (100%) | Good (75%) | Needs Work (50%) | Incomplete (25%) |
|-----------|-----------------|------------|-----------------|-----------------|
| **Task 1: Schema (30)** | All 5 tables with proper constraints, realistic data, clean ERD | Tables created but minor constraint issues, basic ERD | Missing tables or major constraint issues, no ERD | Incomplete schema, no data |
| **Task 2: Queries (25)** | 15+ queries covering all categories, correct results, clear comments | 10-14 queries, mostly correct | 5-9 queries, some errors | Fewer than 5 queries |
| **Task 3: SQLAlchemy (25)** | Full CRUD with relationships, Alembic migrations working, clean code | CRUD works but missing Alembic or relationships | Basic model definitions, partial CRUD | Models only, no operations |
| **Task 4: MongoDB (20)** | Full CRUD + aggregation pipeline, good document design | CRUD works, basic aggregation | Insert and find only | Incomplete or not attempted |

---

**Submission Checklist:**
- [ ] `task1_schema.sql` -- CREATE TABLE + INSERT statements
- [ ] `task1_erd.png` -- ERD diagram screenshot
- [ ] `task2_queries.sql` -- All SQL queries with comments
- [ ] `task3_app.py` -- SQLAlchemy CRUD application
- [ ] `task3_models.py` -- SQLAlchemy model definitions
- [ ] `task3_alembic/` -- Alembic configuration and migration files
- [ ] `task4_feedback.py` -- PyMongo CRUD and aggregation script
- [ ] `screenshots/` -- Screenshots of running code and outputs
