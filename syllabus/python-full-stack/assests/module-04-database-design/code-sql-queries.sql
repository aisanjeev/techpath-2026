-- =============================================================
-- Module 04: SQL Queries for TechPath Training Institute
-- Database: MySQL / SQLite compatible
-- MySQL uses INT AUTO_INCREMENT; SQLite uses INTEGER PRIMARY KEY AUTOINCREMENT
-- =============================================================

-- =============================================================
-- SECTION 1: CREATE TABLES (DDL)
-- =============================================================

-- Drop tables if they exist (for a clean start)
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS trainers;
DROP TABLE IF EXISTS courses;

-- Courses offered by TechPath Institute
CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    duration_months INTEGER NOT NULL CHECK (duration_months > 0),
    fee DECIMAL(10, 2) NOT NULL CHECK (fee >= 0),
    category VARCHAR(50) DEFAULT 'Technical',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Trainers at TechPath Institute
CREATE TABLE trainers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(15),
    specialization VARCHAR(100),
    city VARCHAR(50),
    experience_years INTEGER DEFAULT 0 CHECK (experience_years >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students enrolled at TechPath Institute
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(15),
    city VARCHAR(50) DEFAULT 'Bhopal',
    date_of_birth DATE,
    is_active BOOLEAN DEFAULT TRUE,
    enrolled_date DATE DEFAULT CURRENT_DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Enrollments (junction table: many students <-> many courses)
CREATE TABLE enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    trainer_id INTEGER REFERENCES trainers(id) ON DELETE SET NULL,
    enrolled_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'dropped')),
    grade VARCHAR(2),
    UNIQUE(student_id, course_id)  -- a student cannot enroll in the same course twice
);

-- Payments made by students
CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    amount DECIMAL(10, 2) NOT NULL CHECK (amount > 0),
    payment_date DATE DEFAULT CURRENT_DATE,
    payment_method VARCHAR(30) DEFAULT 'UPI' CHECK (payment_method IN ('UPI', 'Cash', 'Card', 'Net Banking', 'Cheque')),
    receipt_number VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =============================================================
-- SECTION 2: INSERT SAMPLE DATA (DML)
-- =============================================================

-- Insert Courses
INSERT INTO courses (name, duration_months, fee, category) VALUES
    ('Python Full Stack', 6, 35000.00, 'Development'),
    ('Data Science with Python', 4, 28000.00, 'Data'),
    ('Java Full Stack', 6, 32000.00, 'Development'),
    ('Web Development', 3, 18000.00, 'Development'),
    ('DevOps & Cloud', 4, 30000.00, 'Infrastructure'),
    ('UI/UX Design', 3, 15000.00, 'Design'),
    ('Digital Marketing', 2, 12000.00, 'Marketing');

-- Insert Trainers
INSERT INTO trainers (name, email, phone, specialization, city, experience_years) VALUES
    ('Ananya Reddy', 'ananya@techpath.in', '9876543220', 'Python, Django', 'Hyderabad', 8),
    ('Vikram Singh', 'vikram@techpath.in', '9876543221', 'Java, Spring Boot', 'Delhi', 10),
    ('Neha Joshi', 'neha@techpath.in', '9876543222', 'Data Science, ML', 'Pune', 6),
    ('Karan Verma', 'karan@techpath.in', '9876543223', 'DevOps, AWS', 'Bhopal', 5),
    ('Sneha Gupta', 'sneha.trainer@techpath.in', '9876543224', 'UI/UX, Figma', 'Indore', 4);

-- Insert Students (12 students with Indian names and cities)
INSERT INTO students (name, email, phone, city, date_of_birth, enrolled_date) VALUES
    ('Rahul Sharma', 'rahul.sharma@email.com', '9876543210', 'Bhopal', '2003-05-15', '2026-01-10'),
    ('Priya Patel', 'priya.patel@email.com', '9876543211', 'Pune', '2002-08-22', '2026-01-12'),
    ('Amit Kumar', 'amit.kumar@email.com', '9876543212', 'Delhi', '2004-01-30', '2026-02-01'),
    ('Sneha Gupta', 'sneha.gupta@email.com', '9876543213', 'Indore', '2003-11-18', '2026-02-05'),
    ('Vikram Patel', 'vikram.patel@email.com', '9876543214', 'Hyderabad', '2002-03-25', '2026-02-10'),
    ('Ananya Mishra', 'ananya.mishra@email.com', '9876543215', 'Bhopal', '2004-07-08', '2026-02-15'),
    ('Karan Mehta', 'karan.mehta@email.com', '9876543216', 'Delhi', '2003-09-12', '2026-03-01'),
    ('Neha Agarwal', 'neha.agarwal@email.com', '9876543217', 'Pune', '2002-12-04', '2026-03-05'),
    ('Arjun Yadav', 'arjun.yadav@email.com', '9876543218', 'Bhopal', '2003-06-20', '2026-03-10'),
    ('Pooja Deshmukh', 'pooja.deshmukh@email.com', '9876543219', 'Indore', '2004-02-14', '2026-03-15'),
    ('Rohan Jain', 'rohan.jain@email.com', '9876543230', 'Hyderabad', '2003-10-01', '2026-04-01'),
    ('Kavita Nair', 'kavita.nair@email.com', '9876543231', 'Delhi', '2002-04-16', '2026-04-05');

-- Insert Enrollments
INSERT INTO enrollments (student_id, course_id, trainer_id, enrolled_date, status, grade) VALUES
    (1, 1, 1, '2026-01-10', 'active', NULL),     -- Rahul -> Python Full Stack
    (2, 1, 1, '2026-01-12', 'active', NULL),     -- Priya -> Python Full Stack
    (3, 3, 2, '2026-02-01', 'active', NULL),     -- Amit -> Java Full Stack
    (4, 2, 3, '2026-02-05', 'completed', 'A'),   -- Sneha -> Data Science
    (5, 1, 1, '2026-02-10', 'active', NULL),     -- Vikram -> Python Full Stack
    (6, 4, 1, '2026-02-15', 'completed', 'B'),   -- Ananya -> Web Development
    (7, 5, 4, '2026-03-01', 'active', NULL),     -- Karan -> DevOps
    (8, 2, 3, '2026-03-05', 'active', NULL),     -- Neha -> Data Science
    (9, 1, 1, '2026-03-10', 'active', NULL),     -- Arjun -> Python Full Stack
    (10, 6, 5, '2026-03-15', 'dropped', NULL),   -- Pooja -> UI/UX (dropped)
    (11, 3, 2, '2026-04-01', 'active', NULL),    -- Rohan -> Java Full Stack
    (12, 5, 4, '2026-04-05', 'active', NULL),    -- Kavita -> DevOps
    (1, 2, 3, '2026-04-10', 'active', NULL),     -- Rahul also in Data Science
    (2, 4, 1, '2026-04-12', 'completed', 'A');   -- Priya also in Web Dev

-- Insert Payments
INSERT INTO payments (student_id, course_id, amount, payment_date, payment_method, receipt_number) VALUES
    (1, 1, 20000.00, '2026-01-10', 'UPI', 'REC-2026-001'),
    (1, 1, 15000.00, '2026-02-10', 'UPI', 'REC-2026-002'),
    (2, 1, 35000.00, '2026-01-12', 'Net Banking', 'REC-2026-003'),
    (3, 3, 16000.00, '2026-02-01', 'Cash', 'REC-2026-004'),
    (3, 3, 16000.00, '2026-03-01', 'UPI', 'REC-2026-005'),
    (4, 2, 28000.00, '2026-02-05', 'Card', 'REC-2026-006'),
    (5, 1, 35000.00, '2026-02-10', 'UPI', 'REC-2026-007'),
    (6, 4, 18000.00, '2026-02-15', 'Cash', 'REC-2026-008'),
    (7, 5, 15000.00, '2026-03-01', 'Net Banking', 'REC-2026-009'),
    (7, 5, 15000.00, '2026-04-01', 'UPI', 'REC-2026-010'),
    (8, 2, 14000.00, '2026-03-05', 'UPI', 'REC-2026-011'),
    (9, 1, 20000.00, '2026-03-10', 'Cash', 'REC-2026-012'),
    (10, 6, 8000.00, '2026-03-15', 'UPI', 'REC-2026-013'),
    (11, 3, 32000.00, '2026-04-01', 'Card', 'REC-2026-014'),
    (12, 5, 30000.00, '2026-04-05', 'Net Banking', 'REC-2026-015'),
    (1, 2, 28000.00, '2026-04-10', 'UPI', 'REC-2026-016');


-- =============================================================
-- SECTION 3: BASIC SELECT QUERIES
-- =============================================================

-- 3.1: All students sorted by name
SELECT name, email, city FROM students ORDER BY name;

-- 3.2: Students from Bhopal
SELECT name, email, phone FROM students WHERE city = 'Bhopal';

-- 3.3: Students enrolled after March 2026
SELECT name, city, enrolled_date
FROM students
WHERE enrolled_date > '2026-03-01'
ORDER BY enrolled_date;

-- 3.4: Active students from Delhi or Pune
SELECT name, city, email
FROM students
WHERE city IN ('Delhi', 'Pune') AND is_active = TRUE;

-- 3.5: Students whose name starts with 'A'
SELECT name, email FROM students WHERE name LIKE 'A%';

-- 3.6: Top 5 most recently enrolled students
SELECT name, city, enrolled_date
FROM students
ORDER BY enrolled_date DESC
LIMIT 5;


-- =============================================================
-- SECTION 4: AGGREGATE FUNCTIONS WITH GROUP BY AND HAVING
-- =============================================================

-- 4.1: Total number of students
SELECT COUNT(*) AS total_students FROM students;

-- 4.2: Number of students per city
SELECT city, COUNT(*) AS student_count
FROM students
GROUP BY city
ORDER BY student_count DESC;

-- 4.3: Total revenue collected (sum of all payments)
SELECT SUM(amount) AS total_revenue FROM payments;

-- 4.4: Average course fee
SELECT AVG(fee) AS average_fee FROM courses;

-- 4.5: Highest and lowest course fees
SELECT
    MAX(fee) AS highest_fee,
    MIN(fee) AS lowest_fee,
    MAX(fee) - MIN(fee) AS fee_range
FROM courses;

-- 4.6: Revenue per payment method
SELECT
    payment_method,
    COUNT(*) AS transactions,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount
FROM payments
GROUP BY payment_method
ORDER BY total_amount DESC;

-- 4.7: Cities with more than 2 students (HAVING)
SELECT city, COUNT(*) AS student_count
FROM students
GROUP BY city
HAVING COUNT(*) > 2
ORDER BY student_count DESC;

-- 4.8: Courses with total revenue above Rs. 30,000
SELECT
    c.name AS course,
    COUNT(DISTINCT p.student_id) AS paying_students,
    SUM(p.amount) AS total_revenue
FROM courses c
JOIN payments p ON c.id = p.course_id
GROUP BY c.name
HAVING SUM(p.amount) > 30000
ORDER BY total_revenue DESC;


-- =============================================================
-- SECTION 5: ALL JOIN TYPES
-- =============================================================

-- 5.1: INNER JOIN -- Students with their enrolled courses
SELECT
    s.name AS student,
    c.name AS course,
    e.status,
    e.enrolled_date
FROM students s
INNER JOIN enrollments e ON s.id = e.student_id
INNER JOIN courses c ON e.course_id = c.id
ORDER BY s.name;

-- 5.2: LEFT JOIN -- All students, even those not enrolled in any course
--       (useful to find students who haven't enrolled yet)
SELECT
    s.name AS student,
    s.city,
    c.name AS course
FROM students s
LEFT JOIN enrollments e ON s.id = e.student_id
LEFT JOIN courses c ON e.course_id = c.id
ORDER BY s.name;

-- 5.3: RIGHT JOIN -- All courses, even those with no enrollments
SELECT
    c.name AS course,
    c.fee,
    COUNT(e.student_id) AS enrolled_students
FROM enrollments e
RIGHT JOIN courses c ON e.course_id = c.id
GROUP BY c.name, c.fee
ORDER BY enrolled_students DESC;

-- 5.4: FULL OUTER JOIN -- All students and all courses
--       Note: MySQL and SQLite do not support FULL OUTER JOIN directly.
--       Workaround: use UNION of LEFT JOIN and RIGHT JOIN.
SELECT s.name AS student, c.name AS course
FROM students s
LEFT JOIN enrollments e ON s.id = e.student_id
LEFT JOIN courses c ON e.course_id = c.id
UNION
SELECT s.name AS student, c.name AS course
FROM enrollments e
RIGHT JOIN courses c ON e.course_id = c.id
LEFT JOIN students s ON s.id = e.student_id
ORDER BY student, course;

-- 5.5: CROSS JOIN -- Every student paired with every course (for a brochure)
SELECT
    s.name AS student,
    c.name AS course,
    c.fee
FROM students s
CROSS JOIN courses c
WHERE c.is_active = TRUE
ORDER BY s.name, c.name;

-- 5.6: SELF JOIN -- Find students from the same city
SELECT
    a.name AS student_1,
    b.name AS student_2,
    a.city
FROM students a
JOIN students b ON a.city = b.city AND a.id < b.id
ORDER BY a.city, a.name;

-- 5.7: Multi-table JOIN -- Student, course, trainer, and payment details
SELECT
    s.name AS student,
    s.city,
    c.name AS course,
    t.name AS trainer,
    e.status,
    COALESCE(SUM(p.amount), 0) AS total_paid,
    c.fee - COALESCE(SUM(p.amount), 0) AS balance_due
FROM students s
JOIN enrollments e ON s.id = e.student_id
JOIN courses c ON e.course_id = c.id
LEFT JOIN trainers t ON e.trainer_id = t.id
LEFT JOIN payments p ON s.id = p.student_id AND c.id = p.course_id
GROUP BY s.name, s.city, c.name, t.name, e.status, c.fee
ORDER BY s.name;


-- =============================================================
-- SECTION 6: SUBQUERIES
-- =============================================================

-- 6.1: Students enrolled in courses that cost more than average
SELECT s.name, c.name AS course, c.fee
FROM students s
JOIN enrollments e ON s.id = e.student_id
JOIN courses c ON e.course_id = c.id
WHERE c.fee > (SELECT AVG(fee) FROM courses);

-- 6.2: Student who paid the most in total
SELECT s.name, SUM(p.amount) AS total_paid
FROM students s
JOIN payments p ON s.id = p.student_id
GROUP BY s.name
HAVING SUM(p.amount) = (
    SELECT MAX(total)
    FROM (SELECT SUM(amount) AS total FROM payments GROUP BY student_id) sub
);

-- 6.3: Courses with no enrollments
SELECT name, fee FROM courses
WHERE id NOT IN (SELECT DISTINCT course_id FROM enrollments);

-- 6.4: Students who are enrolled in more than one course
SELECT name, email FROM students
WHERE id IN (
    SELECT student_id FROM enrollments
    GROUP BY student_id
    HAVING COUNT(course_id) > 1
);

-- 6.5: Trainers who teach the most expensive course
SELECT t.name, t.specialization, c.name AS course, c.fee
FROM trainers t
JOIN enrollments e ON t.id = e.trainer_id
JOIN courses c ON e.course_id = c.id
WHERE c.fee = (SELECT MAX(fee) FROM courses)
GROUP BY t.name, t.specialization, c.name, c.fee;


-- =============================================================
-- SECTION 7: CTEs (Common Table Expressions)
-- =============================================================

-- 7.1: Revenue report per course using CTE
WITH course_revenue AS (
    SELECT
        c.id AS course_id,
        c.name AS course_name,
        c.fee AS course_fee,
        COUNT(DISTINCT e.student_id) AS total_enrolled,
        COALESCE(SUM(p.amount), 0) AS total_collected
    FROM courses c
    LEFT JOIN enrollments e ON c.id = e.course_id
    LEFT JOIN payments p ON c.id = p.course_id
    GROUP BY c.id, c.name, c.fee
)
SELECT
    course_name,
    course_fee,
    total_enrolled,
    total_collected,
    (total_enrolled * course_fee) AS expected_revenue,
    (total_enrolled * course_fee) - total_collected AS outstanding
FROM course_revenue
ORDER BY total_collected DESC;

-- 7.2: Student rankings by total payment using multiple CTEs
WITH
student_payments AS (
    SELECT
        s.id,
        s.name,
        s.city,
        COALESCE(SUM(p.amount), 0) AS total_paid
    FROM students s
    LEFT JOIN payments p ON s.id = p.student_id
    GROUP BY s.id, s.name, s.city
),
ranked_students AS (
    SELECT
        name,
        city,
        total_paid,
        RANK() OVER (ORDER BY total_paid DESC) AS payment_rank
    FROM student_payments
    WHERE total_paid > 0
)
SELECT * FROM ranked_students ORDER BY payment_rank;

-- 7.3: City-wise enrollment summary with CTE
WITH city_summary AS (
    SELECT
        s.city,
        COUNT(DISTINCT s.id) AS total_students,
        COUNT(e.id) AS total_enrollments,
        COALESCE(SUM(p.amount), 0) AS total_revenue
    FROM students s
    LEFT JOIN enrollments e ON s.id = e.student_id
    LEFT JOIN payments p ON s.id = p.student_id
    GROUP BY s.city
)
SELECT
    city,
    total_students,
    total_enrollments,
    total_revenue,
    ROUND(total_revenue / NULLIF(total_students, 0), 2) AS revenue_per_student
FROM city_summary
ORDER BY total_revenue DESC;


-- =============================================================
-- SECTION 8: CASE EXPRESSIONS
-- =============================================================

-- 8.1: Categorize students by enrollment month
--       MySQL: use MONTH() function. SQLite: use strftime('%m', date).
SELECT
    name,
    enrolled_date,
    CASE
        WHEN MONTH(enrolled_date) <= 3 THEN 'Q1 (Jan-Mar)'
        WHEN MONTH(enrolled_date) <= 6 THEN 'Q2 (Apr-Jun)'
        WHEN MONTH(enrolled_date) <= 9 THEN 'Q3 (Jul-Sep)'
        ELSE 'Q4 (Oct-Dec)'
    END AS enrollment_quarter
FROM students
ORDER BY enrolled_date;

-- 8.2: Payment status per enrollment
SELECT
    s.name AS student,
    c.name AS course,
    c.fee,
    COALESCE(SUM(p.amount), 0) AS paid,
    CASE
        WHEN COALESCE(SUM(p.amount), 0) >= c.fee THEN 'Fully Paid'
        WHEN COALESCE(SUM(p.amount), 0) > 0 THEN 'Partially Paid'
        ELSE 'Unpaid'
    END AS payment_status
FROM students s
JOIN enrollments e ON s.id = e.student_id
JOIN courses c ON e.course_id = c.id
LEFT JOIN payments p ON s.id = p.student_id AND c.id = p.course_id
GROUP BY s.name, c.name, c.fee
ORDER BY s.name;

-- 8.3: Categorize courses by fee range
SELECT
    name,
    fee,
    CASE
        WHEN fee >= 30000 THEN 'Premium'
        WHEN fee >= 20000 THEN 'Standard'
        WHEN fee >= 15000 THEN 'Value'
        ELSE 'Budget'
    END AS fee_tier,
    CONCAT(duration_months, ' months') AS duration
FROM courses
ORDER BY fee DESC;


-- =============================================================
-- SECTION 9: CREATE INDEXES
-- =============================================================

-- Index on student email (for login lookups)
CREATE INDEX idx_students_email ON students(email);

-- Index on student city (for filtering by city)
CREATE INDEX idx_students_city ON students(city);

-- Index on enrollment status (for filtering active/completed)
CREATE INDEX idx_enrollments_status ON enrollments(status);

-- Composite index on payments (for revenue queries)
CREATE INDEX idx_payments_student_course ON payments(student_id, course_id);

-- Index on payment date (for date range queries)
CREATE INDEX idx_payments_date ON payments(payment_date);

-- Index on trainer specialization (for search)
CREATE INDEX idx_trainers_specialization ON trainers(specialization);


-- =============================================================
-- SECTION 10: USEFUL QUERIES FOR PRACTICE
-- =============================================================

-- 10.1: Complete student report card
SELECT
    s.name AS student,
    s.city,
    c.name AS course,
    t.name AS trainer,
    e.status,
    e.grade,
    COALESCE(SUM(p.amount), 0) AS total_paid,
    c.fee - COALESCE(SUM(p.amount), 0) AS balance
FROM students s
JOIN enrollments e ON s.id = e.student_id
JOIN courses c ON e.course_id = c.id
LEFT JOIN trainers t ON e.trainer_id = t.id
LEFT JOIN payments p ON s.id = p.student_id AND c.id = p.course_id
GROUP BY s.name, s.city, c.name, t.name, e.status, e.grade, c.fee
ORDER BY s.name, c.name;

-- 10.2: Monthly revenue trend
--        MySQL: DATE_FORMAT(). SQLite: strftime('%Y-%m', date).
SELECT
    DATE_FORMAT(payment_date, '%Y-%m') AS month,
    COUNT(*) AS transactions,
    SUM(amount) AS revenue
FROM payments
GROUP BY DATE_FORMAT(payment_date, '%Y-%m')
ORDER BY month;

-- 10.3: Trainer workload (how many students each trainer handles)
SELECT
    t.name AS trainer,
    t.specialization,
    COUNT(DISTINCT e.student_id) AS active_students,
    COUNT(DISTINCT e.course_id) AS courses_taught
FROM trainers t
LEFT JOIN enrollments e ON t.id = e.trainer_id AND e.status = 'active'
GROUP BY t.name, t.specialization
ORDER BY active_students DESC;

-- 10.4: Students with pending balance
SELECT
    s.name,
    c.name AS course,
    c.fee,
    COALESCE(SUM(p.amount), 0) AS paid,
    c.fee - COALESCE(SUM(p.amount), 0) AS pending
FROM students s
JOIN enrollments e ON s.id = e.student_id
JOIN courses c ON e.course_id = c.id
LEFT JOIN payments p ON s.id = p.student_id AND c.id = p.course_id
GROUP BY s.name, c.name, c.fee
HAVING c.fee - COALESCE(SUM(p.amount), 0) > 0
ORDER BY pending DESC;
