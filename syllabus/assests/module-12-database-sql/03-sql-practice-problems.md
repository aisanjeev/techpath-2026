# SQL — 20 Practice Problems with Solutions

**Module 12 — Database & SQL | Interview-Ready Practice**

---

## Why This Matters

> "Write a SQL query to..." is in every IT interview — frontend, backend, data analyst, even QA. These 20 problems cover exactly what companies ask freshers. Don't just read them — type each query yourself.

---

## Setup: Sample Database

We'll use 3 tables. Create them first:

```sql
-- Employees table
CREATE TABLE employees (
    emp_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department VARCHAR(50),
    salary DECIMAL(10,2),
    joining_date DATE,
    manager_id INTEGER,
    city VARCHAR(50)
);

INSERT INTO employees VALUES
(1, 'Rahul Sharma', 'IT', 75000, '2022-03-15', NULL, 'Mumbai'),
(2, 'Priya Patel', 'HR', 55000, '2021-06-01', 1, 'Delhi'),
(3, 'Amit Kumar', 'IT', 82000, '2020-11-10', 1, 'Bangalore'),
(4, 'Sneha Gupta', 'Sales', 48000, '2023-01-20', 1, 'Mumbai'),
(5, 'Vikram Singh', 'IT', 90000, '2019-08-05', 1, 'Pune'),
(6, 'Kavita Joshi', 'HR', 52000, '2022-09-12', 2, 'Delhi'),
(7, 'Ravi Verma', 'Sales', 45000, '2023-04-01', 4, 'Mumbai'),
(8, 'Anita Das', 'IT', 70000, '2021-12-15', 3, 'Bangalore'),
(9, 'Manoj Tiwari', 'Finance', 65000, '2020-05-22', 1, 'Pune'),
(10, 'Pooja Reddy', 'Sales', 50000, '2022-07-30', 4, 'Hyderabad'),
(11, 'Deepak Nair', 'Finance', 72000, '2021-03-18', 9, 'Mumbai'),
(12, 'Sunita Mehta', 'HR', 58000, '2023-02-14', 2, 'Delhi');

-- Orders table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    product VARCHAR(100),
    quantity INTEGER,
    price DECIMAL(10,2),
    order_date DATE,
    city VARCHAR(50)
);

INSERT INTO orders VALUES
(1, 'Tech Corp', 'Laptop', 5, 55000, '2024-01-15', 'Mumbai'),
(2, 'DataSoft', 'Monitor', 10, 18000, '2024-01-20', 'Delhi'),
(3, 'WebAgency', 'Keyboard', 25, 2500, '2024-02-05', 'Bangalore'),
(4, 'Tech Corp', 'Mouse', 50, 800, '2024-02-10', 'Mumbai'),
(5, 'StartupXYZ', 'Laptop', 3, 55000, '2024-02-15', 'Pune'),
(6, 'DataSoft', 'Headphones', 15, 3500, '2024-03-01', 'Delhi'),
(7, 'WebAgency', 'Monitor', 8, 18000, '2024-03-10', 'Bangalore'),
(8, 'Tech Corp', 'Laptop', 2, 55000, '2024-03-20', 'Mumbai'),
(9, 'CloudInc', 'Keyboard', 30, 2500, '2024-04-05', 'Hyderabad'),
(10, 'StartupXYZ', 'Mouse', 100, 800, '2024-04-15', 'Pune');

-- Departments table
CREATE TABLE departments (
    dept_name VARCHAR(50) PRIMARY KEY,
    location VARCHAR(50),
    budget DECIMAL(12,2)
);

INSERT INTO departments VALUES
('IT', 'Bangalore', 5000000),
('HR', 'Delhi', 2000000),
('Sales', 'Mumbai', 3500000),
('Finance', 'Pune', 3000000),
('Marketing', 'Mumbai', 2500000);
```

---

## Easy (Must Know — Asked in Every Interview)

### Problem 1: Select all employees in the IT department

```sql
SELECT * FROM employees WHERE department = 'IT';
```

| emp_id | name | department | salary | city |
|--------|------|-----------|--------|------|
| 1 | Rahul Sharma | IT | 75000 | Mumbai |
| 3 | Amit Kumar | IT | 82000 | Bangalore |
| 5 | Vikram Singh | IT | 90000 | Pune |
| 8 | Anita Das | IT | 70000 | Bangalore |

---

### Problem 2: Find the highest salary

```sql
SELECT MAX(salary) AS highest_salary FROM employees;
-- Answer: 90000
```

---

### Problem 3: Count employees per department

```sql
SELECT department, COUNT(*) AS employee_count
FROM employees
GROUP BY department
ORDER BY employee_count DESC;
```

| department | employee_count |
|-----------|---------------|
| IT | 4 |
| HR | 3 |
| Sales | 3 |
| Finance | 2 |

---

### Problem 4: Employees who earn more than 60,000

```sql
SELECT name, salary
FROM employees
WHERE salary > 60000
ORDER BY salary DESC;
```

---

### Problem 5: Employees who joined in 2022

```sql
SELECT name, joining_date
FROM employees
WHERE joining_date BETWEEN '2022-01-01' AND '2022-12-31';

-- Alternative:
SELECT name, joining_date
FROM employees
WHERE YEAR(joining_date) = 2022;  -- MySQL/SQL Server syntax
```

---

## Medium (Fresher Interview Level)

### Problem 6: Second highest salary

This is the **#1 most asked SQL interview question** for freshers.

```sql
-- Method 1: Subquery
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);

-- Method 2: LIMIT/OFFSET
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 1;

-- Method 3: DENSE_RANK (modern, impressive)
SELECT salary FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rank
    FROM employees
) ranked
WHERE rank = 2;
```

**Answer:** 82000

---

### Problem 7: Average salary by department (only departments with avg > 60000)

```sql
SELECT department, ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 60000
ORDER BY avg_salary DESC;
```

| department | avg_salary |
|-----------|-----------|
| IT | 79250.00 |
| Finance | 68500.00 |

**Key concept:** `WHERE` filters rows, `HAVING` filters groups.

---

### Problem 8: Total revenue by product

```sql
SELECT product,
       SUM(quantity) AS total_qty,
       SUM(quantity * price) AS total_revenue
FROM orders
GROUP BY product
ORDER BY total_revenue DESC;
```

| product | total_qty | total_revenue |
|---------|----------|--------------|
| Laptop | 10 | 550000 |
| Monitor | 18 | 324000 |
| Mouse | 150 | 120000 |
| Keyboard | 55 | 137500 |
| Headphones | 15 | 52500 |

---

### Problem 9: Employees in cities that have more than 2 employees

```sql
SELECT name, city
FROM employees
WHERE city IN (
    SELECT city
    FROM employees
    GROUP BY city
    HAVING COUNT(*) > 2
);
```

---

### Problem 10: Top 3 highest paid employees

```sql
SELECT name, salary
FROM employees
ORDER BY salary DESC
LIMIT 3;
```

---

### Problem 11: Find duplicate customer names in orders

```sql
SELECT customer_name, COUNT(*) AS order_count
FROM orders
GROUP BY customer_name
HAVING COUNT(*) > 1;
```

---

### Problem 12: Employees who don't have a manager

```sql
SELECT name
FROM employees
WHERE manager_id IS NULL;
```

---

## Hard (Stand Out in Interviews)

### Problem 13: Department-wise salary ranking

```sql
SELECT name, department, salary,
       RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS dept_rank
FROM employees;
```

| name | department | salary | dept_rank |
|------|-----------|--------|----------|
| Vikram Singh | IT | 90000 | 1 |
| Amit Kumar | IT | 82000 | 2 |
| Rahul Sharma | IT | 75000 | 3 |
| Anita Das | IT | 70000 | 4 |
| Sunita Mehta | HR | 58000 | 1 |
| Priya Patel | HR | 55000 | 2 |
| ... | ... | ... | ... |

---

### Problem 14: Running total of order revenue by date

```sql
SELECT order_date, product,
       quantity * price AS revenue,
       SUM(quantity * price) OVER (ORDER BY order_date) AS running_total
FROM orders
ORDER BY order_date;
```

---

### Problem 15: Find employees earning more than their department average

```sql
SELECT e.name, e.department, e.salary, dept_avg.avg_salary
FROM employees e
JOIN (
    SELECT department, AVG(salary) AS avg_salary
    FROM employees
    GROUP BY department
) dept_avg ON e.department = dept_avg.department
WHERE e.salary > dept_avg.avg_salary;
```

---

### Problem 16: Monthly revenue trend

```sql
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    COUNT(*) AS total_orders,
    SUM(quantity * price) AS revenue
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;
```

---

### Problem 17: Departments with no employees (LEFT JOIN)

```sql
SELECT d.dept_name
FROM departments d
LEFT JOIN employees e ON d.dept_name = e.department
WHERE e.emp_id IS NULL;
```

**Answer:** Marketing (exists in departments table but no employees)

---

### Problem 18: Employee with their manager's name

```sql
SELECT
    e.name AS employee,
    m.name AS manager
FROM employees e
LEFT JOIN employees e AS m ON e.manager_id = m.emp_id;
```

This is a **self-join** — the table joins with itself.

---

### Problem 19: Customer who placed the most orders

```sql
SELECT customer_name, COUNT(*) AS order_count, SUM(quantity * price) AS total_spent
FROM orders
GROUP BY customer_name
ORDER BY order_count DESC
LIMIT 1;
```

---

### Problem 20: Create a view for the dashboard

```sql
CREATE VIEW sales_dashboard AS
SELECT
    o.city,
    COUNT(*) AS total_orders,
    SUM(o.quantity * o.price) AS total_revenue,
    AVG(o.quantity * o.price) AS avg_order_value,
    MAX(o.order_date) AS last_order_date
FROM orders o
GROUP BY o.city;

-- Now use it like a table:
SELECT * FROM sales_dashboard ORDER BY total_revenue DESC;
```

---

## SQL Concepts Interviewers Ask About

| Question | Answer |
|----------|--------|
| WHERE vs HAVING | WHERE filters rows before grouping, HAVING filters after GROUP BY |
| INNER vs LEFT JOIN | INNER returns only matches, LEFT returns all from left table + matches |
| RANK vs DENSE_RANK | RANK skips numbers after ties (1,2,2,4), DENSE_RANK doesn't (1,2,2,3) |
| DELETE vs TRUNCATE | DELETE removes specific rows (can rollback), TRUNCATE removes all (faster, no rollback) |
| PRIMARY KEY vs UNIQUE | PK: one per table, no NULL. UNIQUE: many per table, allows one NULL |
| Index | Speeds up SELECT queries on a column, slows INSERT/UPDATE slightly |
| Normalization | Organizing data to reduce redundancy (1NF, 2NF, 3NF) |
| ACID properties | Atomicity, Consistency, Isolation, Durability — transaction guarantees |

---

## Practice Suggestions

1. **Install SQLite** (comes with Python) or use **DB Browser for SQLite** (free, visual)
2. Create the tables above
3. Solve each problem by typing (not copy-pasting)
4. Try variations: change conditions, add new data
5. Practice on **HackerRank SQL** and **LeetCode Database** sections
