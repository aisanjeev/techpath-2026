-- =============================================
-- Institute Database — Module 12 Code Snap
-- Run in: DB Browser for SQLite or sqliteonline.com
-- =============================================

-- Drop existing tables (for re-running)
DROP TABLE IF EXISTS marks;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS trainers;
DROP TABLE IF EXISTS courses;

-- === CREATE TABLES ===

CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    duration_months INTEGER NOT NULL CHECK(duration_months > 0),
    fee INTEGER NOT NULL CHECK(fee > 0),
    description TEXT
);

CREATE TABLE trainers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXT,
    email TEXT UNIQUE NOT NULL
);

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT CHECK(LENGTH(phone) = 10),
    course_id INTEGER NOT NULL,
    batch TEXT DEFAULT '2026-A',
    city TEXT,
    enrolled_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

CREATE TABLE attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    date DATE NOT NULL,
    status TEXT CHECK(status IN ('present', 'absent')) NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE marks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject TEXT NOT NULL,
    marks INTEGER CHECK(marks >= 0 AND marks <= 100),
    max_marks INTEGER DEFAULT 100,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

-- === INSERT DATA ===

INSERT INTO courses (name, duration_months, fee, description) VALUES
    ('ADCA', 12, 35000, 'Advanced Diploma in Computer Applications'),
    ('DCA', 6, 18000, 'Diploma in Computer Applications'),
    ('Tally Pro', 3, 8000, 'Tally ERP with GST');

INSERT INTO trainers (name, specialization, email) VALUES
    ('Sanjeev Kumar', 'Python, FastAPI, Web Development', 'sanjeev@techpath.biz'),
    ('Priyanka Sharma', 'MS Office, Tally, Accounting', 'priyanka@techpath.biz');

INSERT INTO students (name, email, phone, course_id, city) VALUES
    ('Rahul Sharma', 'rahul@email.com', '9876543210', 1, 'Bhopal'),
    ('Priya Patel', 'priya@email.com', '9876543211', 2, 'Indore'),
    ('Amit Kumar', 'amit@email.com', '9876543212', 1, 'Delhi'),
    ('Sneha Gupta', 'sneha@email.com', '9876543213', 1, 'Bhopal'),
    ('Vikram Singh', 'vikram@email.com', '9876543214', 2, 'Jaipur'),
    ('Ananya Reddy', 'ananya@email.com', '9876543215', 1, 'Hyderabad'),
    ('Karan Verma', 'karan@email.com', '9876543216', 3, 'Bhopal'),
    ('Neha Joshi', 'neha@email.com', '9876543217', 1, 'Pune'),
    ('Rohit Mishra', 'rohit@email.com', '9876543218', 2, 'Delhi'),
    ('Divya Saxena', 'divya@email.com', '9876543219', 1, 'Mumbai');

INSERT INTO marks (student_id, subject, marks) VALUES
    (1, 'Hindi', 78), (1, 'English', 82), (1, 'Maths', 70), (1, 'Computer', 88),
    (2, 'Hindi', 85), (2, 'English', 90), (2, 'Maths', 88), (2, 'Computer', 95),
    (3, 'Hindi', 45), (3, 'English', 50), (3, 'Maths', 35), (3, 'Computer', 60),
    (4, 'Hindi', 92), (4, 'English', 88), (4, 'Maths', 85), (4, 'Computer', 94),
    (5, 'Hindi', 38), (5, 'English', 42), (5, 'Maths', 30), (5, 'Computer', 45),
    (6, 'Hindi', 95), (6, 'English', 98), (6, 'Maths', 92), (6, 'Computer', 99),
    (7, 'Hindi', 52), (7, 'English', 60), (7, 'Maths', 48), (7, 'Computer', 65),
    (8, 'Hindi', 88), (8, 'English', 75), (8, 'Maths', 80), (8, 'Computer', 90),
    (9, 'Hindi', 70), (9, 'English', 68), (9, 'Maths', 60), (9, 'Computer', 72),
    (10, 'Hindi', 65), (10, 'English', 72), (10, 'Maths', 68), (10, 'Computer', 80);

INSERT INTO attendance (student_id, date, status) VALUES
    (1, '2026-07-01', 'present'), (1, '2026-07-02', 'present'), (1, '2026-07-03', 'absent'),
    (2, '2026-07-01', 'present'), (2, '2026-07-02', 'absent'), (2, '2026-07-03', 'present'),
    (3, '2026-07-01', 'absent'),  (3, '2026-07-02', 'absent'), (3, '2026-07-03', 'present'),
    (4, '2026-07-01', 'present'), (4, '2026-07-02', 'present'), (4, '2026-07-03', 'present'),
    (5, '2026-07-01', 'absent'),  (5, '2026-07-02', 'absent'), (5, '2026-07-03', 'absent'),
    (6, '2026-07-01', 'present'), (6, '2026-07-02', 'present'), (6, '2026-07-03', 'present'),
    (7, '2026-07-01', 'present'), (7, '2026-07-02', 'absent'),
    (8, '2026-07-01', 'present'), (8, '2026-07-02', 'present');

-- === USEFUL QUERIES ===

-- All students with their course name
SELECT s.name, s.city, c.name AS course, c.fee
FROM students s
JOIN courses c ON s.course_id = c.id
ORDER BY s.name;

-- Total students per course
SELECT c.name, COUNT(s.id) AS students, c.fee * COUNT(s.id) AS revenue
FROM courses c
LEFT JOIN students s ON c.id = s.course_id
GROUP BY c.id;

-- Average marks per subject
SELECT subject, ROUND(AVG(marks), 1) AS avg_marks
FROM marks GROUP BY subject ORDER BY avg_marks DESC;

-- Top 5 students by total marks
SELECT s.name, SUM(m.marks) AS total, ROUND(AVG(m.marks), 1) AS average
FROM students s
JOIN marks m ON s.id = m.student_id
GROUP BY s.id
ORDER BY total DESC LIMIT 5;

-- Attendance percentage per student
SELECT s.name,
    COUNT(CASE WHEN a.status = 'present' THEN 1 END) AS present,
    COUNT(a.id) AS total,
    ROUND(100.0 * COUNT(CASE WHEN a.status = 'present' THEN 1 END) / COUNT(a.id), 1) AS attendance_pct
FROM students s
LEFT JOIN attendance a ON s.id = a.student_id
GROUP BY s.id
ORDER BY attendance_pct DESC;
