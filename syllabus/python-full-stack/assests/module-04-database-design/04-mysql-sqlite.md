# MySQL & SQLite — Relational Databases for Python Developers

**Module 04 — Database Design, SQL & NoSQL | Topic 4**

---

## Why MySQL and SQLite?

In this course, we use **two** relational databases:

| Feature | SQLite | MySQL |
|---------|--------|-------|
| Type | File-based (no server) | Server-based |
| Setup | Zero install | Install server |
| Best for | Learning, prototyping, small apps | Production web apps, Indian IT industry |
| Concurrent writes | Poor (file-level lock) | Good |
| JSON support | Basic (JSON functions) | JSON type with functions |
| Full-text search | FTS5 extension | Built-in FULLTEXT |
| Used by | Android, browsers, embedded | TCS, Infosys, Wipro, most Indian startups |

- **SQLite** is perfect for beginners -- no server to install, just a single file. You can start writing SQL in minutes.
- **MySQL** is the most widely used database in Indian IT companies. Learning it gives you a direct job-ready skill.

**In this course:** We use SQLite for local development (simple, no setup) and MySQL for production-ready projects.

---

## SQLite — The Simple Choice

### What Makes SQLite Special?

SQLite is a **file-based database**. The entire database is stored in a single `.db` file on your computer. No server process, no configuration, no passwords.

```
Traditional database:  App -> Network -> Database Server -> Disk
SQLite:               App -> Single File on Disk
```

SQLite is used everywhere:
- Every Android phone has SQLite
- Every web browser uses SQLite (for bookmarks, history, etc.)
- Python comes with SQLite built-in (`sqlite3` module)
- WhatsApp stores messages in SQLite

### Using SQLite with Python (Built-in)

Python includes SQLite support -- no installation needed:

```python
import sqlite3

# Create (or connect to) a database file
conn = sqlite3.connect("techpath.db")
cursor = conn.cursor()

# Create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        city TEXT DEFAULT 'Bhopal',
        fee_paid REAL DEFAULT 0.0,
        is_active INTEGER DEFAULT 1,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")

# Insert data
cursor.execute(
    "INSERT INTO students (name, email, city) VALUES (?, ?, ?)",
    ("Rahul Sharma", "rahul@techpath.in", "Bhopal")
)
conn.commit()

# Query data
cursor.execute("SELECT name, city FROM students")
for row in cursor.fetchall():
    print(row)

# Close connection
conn.close()
```

### DB Browser for SQLite — The Visual Tool

**DB Browser for SQLite** is a free GUI tool to view and edit SQLite databases.

1. Download from https://sqlitebrowser.org/dl/
2. Install and open the application
3. Click **Open Database** and select your `.db` file
4. Browse tables, run queries, and view data visually

**Key features:**
- Visual table browser and editor
- SQL query editor with syntax highlighting
- Import/Export CSV and SQL files
- View database structure and indexes

### Common DB Browser Tasks

| Task | How |
|------|-----|
| Open a database | File > Open Database > select `.db` file |
| View table data | Click on a table name > Browse Data tab |
| Run SQL | Execute SQL tab > type query > click Play |
| Create a table | Execute SQL tab > write CREATE TABLE |
| Export data | File > Export > Table as CSV or SQL |

### sqlite3 Command Line Tool

Python includes a command-line SQLite tool:

```bash
# Open (or create) a database
python -m sqlite3 techpath.db

# Or if sqlite3 is installed separately:
sqlite3 techpath.db
```

| Command | What It Does |
|---------|-------------|
| `.tables` | List all tables |
| `.schema tablename` | Show CREATE TABLE statement |
| `.headers on` | Show column headers in output |
| `.mode column` | Format output in columns |
| `.mode csv` | Output in CSV format |
| `.import file.csv table` | Import CSV into a table |
| `.dump` | Export entire database as SQL |
| `.exit` | Quit sqlite3 |

### SQLite Data Types

SQLite uses a simpler type system than MySQL:

| SQLite Type | Stores | Example |
|-------------|--------|---------|
| `INTEGER` | Whole numbers | `id INTEGER PRIMARY KEY` |
| `REAL` | Decimal numbers | `fee REAL` |
| `TEXT` | Any text | `name TEXT` |
| `BLOB` | Binary data | `photo BLOB` |
| `NULL` | No value | (empty cell) |

**Note:** SQLite is flexible with types -- it uses "type affinity" rather than strict types. A `TEXT` column can store a number, and SQLite will not complain. This is different from MySQL which enforces types strictly.

---

## MySQL — The Industry Standard

### Why MySQL?

MySQL is the world's most popular open-source relational database. It powers:
- Facebook, Twitter, YouTube, Netflix
- WordPress (and most PHP websites)
- Nearly every Indian IT services company (TCS, Infosys, Wipro, HCL)

### Installing MySQL on Windows

1. Download **MySQL Installer** from https://dev.mysql.com/downloads/installer/
2. Choose **Full** or **Custom** installation
3. During setup:
   - Set a **root password** (remember this!)
   - Keep the default port **3306**
   - Select **MySQL Workbench** (GUI tool)
4. After installation, MySQL runs as a Windows service

**Verify installation:**
```bash
mysql --version
# mysql  Ver 8.0.x for Win64
```

### Installing on Ubuntu/Linux

```bash
# Install MySQL
sudo apt update
sudo apt install mysql-server

# Start the service
sudo systemctl start mysql
sudo systemctl enable mysql

# Secure the installation (set root password)
sudo mysql_secure_installation

# Check status
sudo systemctl status mysql
```

### First-Time Setup

```bash
# Connect to MySQL as root
mysql -u root -p
# Enter the root password you set during installation

# Create a new database user
CREATE USER 'techpath'@'localhost' IDENTIFIED BY 'secure_password_123';

# Create a database
CREATE DATABASE techpath_db;

# Grant all privileges
GRANT ALL PRIVILEGES ON techpath_db.* TO 'techpath'@'localhost';
FLUSH PRIVILEGES;

# Exit
EXIT;
```

### Connecting to MySQL

```bash
# Command line
mysql -h localhost -u techpath -p techpath_db

# Connection string (used in Python apps)
# mysql+pymysql://username:password@host:port/database
mysql+pymysql://techpath:secure_password_123@localhost:3306/techpath_db
```

---

## MySQL Workbench — The Visual Interface

MySQL Workbench is the official GUI for managing MySQL databases. It comes bundled with the MySQL installer.

**Key features:**
- Visual query editor with syntax highlighting
- Table viewer and data editor
- Database design and ERD tool
- User and permission management
- Server performance dashboard
- Data import/export (CSV, SQL, JSON)

### Common MySQL Workbench Tasks

| Task | How |
|------|-----|
| Connect to server | Click your connection on home screen |
| View tables | Expand Schema > your_database > Tables |
| Run a query | Open a new Query Tab (Ctrl+T) |
| View table data | Right-click table > Select Rows |
| Create a table | Right-click Tables > Create Table |
| Export data | Server > Data Export |
| Import SQL file | File > Open SQL Script > Run |

---

## mysql Command Line Tool

`mysql` is the MySQL interactive terminal. Here are the most useful commands:

| Command | What It Does |
|---------|-------------|
| `SHOW DATABASES;` | List all databases |
| `USE dbname;` | Switch to a database |
| `SHOW TABLES;` | List all tables in current database |
| `DESCRIBE tablename;` | Show table structure (columns, types) |
| `SHOW INDEX FROM tablename;` | List all indexes on a table |
| `SHOW CREATE TABLE tablename;` | Show the CREATE TABLE statement |
| `SELECT USER();` | Show current user |
| `STATUS;` | Show connection info |
| `SOURCE filename.sql;` | Execute SQL from a file |
| `EXIT;` | Quit mysql |

---

## MySQL Data Types

| Category | Type | Description | Example |
|----------|------|-------------|---------|
| Integer | `INT` | Whole number | `age INT` |
| Integer | `BIGINT` | Large whole number | `population BIGINT` |
| Integer | `TINYINT(1)` | Boolean (0 or 1) | `is_active TINYINT(1)` |
| Auto ID | `INT AUTO_INCREMENT` | Auto-increment ID | `id INT AUTO_INCREMENT PRIMARY KEY` |
| Text | `VARCHAR(n)` | Variable-length text | `name VARCHAR(100)` |
| Text | `TEXT` | Long text (up to 65KB) | `bio TEXT` |
| Text | `LONGTEXT` | Very long text (up to 4GB) | `content LONGTEXT` |
| Number | `DECIMAL(p,s)` | Exact decimal | `fee DECIMAL(10,2)` |
| Boolean | `BOOLEAN` | Alias for TINYINT(1) | `is_active BOOLEAN` |
| Date/Time | `DATE` | Date only | `dob DATE` |
| Date/Time | `DATETIME` | Date + time | `created_at DATETIME` |
| Date/Time | `TIMESTAMP` | Date + time (auto-updates) | `updated_at TIMESTAMP` |
| JSON | `JSON` | JSON document | `metadata JSON` |

**SQLite vs MySQL type comparison:**

| Concept | SQLite | MySQL |
|---------|--------|-------|
| Auto-increment PK | `INTEGER PRIMARY KEY AUTOINCREMENT` | `INT AUTO_INCREMENT PRIMARY KEY` |
| Boolean | `INTEGER` (0 or 1) | `BOOLEAN` or `TINYINT(1)` |
| Decimal | `REAL` | `DECIMAL(10,2)` |
| Date/Time | `TEXT` (stored as string) | `DATE`, `DATETIME`, `TIMESTAMP` |
| JSON | `TEXT` (with JSON functions) | `JSON` (native type) |

---

## JSON Support in MySQL

MySQL 8.0+ has built-in JSON support. While not as powerful as some other databases, it covers most common needs.

### Creating a Table with JSON

```sql
CREATE TABLE products (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    name    VARCHAR(200) NOT NULL,
    price   DECIMAL(10, 2) NOT NULL,
    details JSON DEFAULT NULL
);
```

### Inserting JSON Data

```sql
INSERT INTO products (name, price, details) VALUES
('Laptop', 65000.00, '{
    "brand": "HP",
    "ram": "16GB",
    "storage": "512GB SSD",
    "color": "Silver",
    "ports": ["USB-C", "HDMI", "USB-A"]
}'),
('Phone', 25000.00, '{
    "brand": "Samsung",
    "ram": "8GB",
    "storage": "128GB",
    "color": "Black",
    "features": ["5G", "AMOLED", "IP68"]
}');
```

### Querying JSON in MySQL

```sql
-- Access a JSON key (returns JSON)
SELECT name, details->'$.brand' AS brand FROM products;

-- Access a JSON key as text (unquoted)
SELECT name, details->>'$.brand' AS brand FROM products;

-- Access array element
SELECT name, details->'$.ports[0]' AS first_port FROM products;

-- Filter by JSON value
SELECT * FROM products WHERE details->>'$.brand' = 'HP';

-- Check if a key exists
SELECT * FROM products WHERE JSON_CONTAINS_PATH(details, 'one', '$.features');

-- Check if array contains a value
SELECT * FROM products WHERE JSON_CONTAINS(details->'$.features', '"5G"');

-- Search inside JSON
SELECT * FROM products
WHERE JSON_EXTRACT(details, '$.ram') = '"16GB"';
```

### MySQL JSON Functions Quick Reference

| Function | Meaning | Example |
|----------|---------|---------|
| `->` | Get JSON element (quoted) | `details->'$.brand'` returns `"HP"` |
| `->>` | Get JSON element (unquoted text) | `details->>'$.brand'` returns `HP` |
| `JSON_EXTRACT()` | Same as `->` | `JSON_EXTRACT(details, '$.brand')` |
| `JSON_UNQUOTE()` | Remove quotes from JSON string | `JSON_UNQUOTE(details->'$.brand')` |
| `JSON_CONTAINS()` | Does JSON contain this value? | `JSON_CONTAINS(details, '"HP"', '$.brand')` |
| `JSON_CONTAINS_PATH()` | Does this path exist? | `JSON_CONTAINS_PATH(details, 'one', '$.brand')` |
| `JSON_ARRAY_LENGTH()` | Length of a JSON array | `JSON_LENGTH(details->'$.ports')` |

### Indexing JSON in MySQL

```sql
-- Create a generated column from JSON, then index it
ALTER TABLE products ADD COLUMN brand VARCHAR(100)
    GENERATED ALWAYS AS (details->>'$.brand') STORED;

CREATE INDEX idx_products_brand ON products(brand);

-- Now you can query efficiently
SELECT * FROM products WHERE brand = 'HP';
```

**Note:** MySQL cannot directly index JSON fields. You create a **generated column** that extracts the JSON value, then index that column.

---

## JSON in SQLite

SQLite also supports JSON through built-in functions (SQLite 3.38+):

```sql
-- Create table (JSON stored as TEXT)
CREATE TABLE products (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL,
    price   REAL NOT NULL,
    details TEXT DEFAULT '{}'
);

-- Extract JSON value
SELECT name, json_extract(details, '$.brand') AS brand FROM products;

-- Filter by JSON value
SELECT * FROM products WHERE json_extract(details, '$.brand') = 'HP';

-- Check if path exists
SELECT * FROM products WHERE json_type(details, '$.features') IS NOT NULL;

-- Get array element
SELECT name, json_extract(details, '$.ports[0]') AS first_port FROM products;
```

---

## Stored Procedures (MySQL)

Stored procedures are reusable SQL code blocks stored in the database. MySQL supports them with its own syntax.

### Creating a Function

```sql
-- Function to calculate course discount
DELIMITER //
CREATE FUNCTION calculate_discount(
    original_price DECIMAL(10,2),
    discount_percent INT
)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    IF discount_percent < 0 OR discount_percent > 100 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Discount must be between 0 and 100';
    END IF;
    RETURN original_price - (original_price * discount_percent / 100.0);
END //
DELIMITER ;

-- Usage
SELECT calculate_discount(25000, 20);  -- Returns 20000.00
SELECT title, price, calculate_discount(price, 15) AS discounted
FROM courses;
```

### Creating a Procedure

```sql
DELIMITER //
CREATE PROCEDURE enroll_student(
    IN p_student_id INT,
    IN p_course_id INT
)
BEGIN
    -- Check if already enrolled
    IF EXISTS (
        SELECT 1 FROM enrollments
        WHERE student_id = p_student_id AND course_id = p_course_id
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Student is already enrolled in this course';
    END IF;

    -- Insert enrollment
    INSERT INTO enrollments (student_id, course_id)
    VALUES (p_student_id, p_course_id);

    SELECT CONCAT('Student ', p_student_id, ' enrolled in course ', p_course_id) AS message;
END //
DELIMITER ;

-- Usage
CALL enroll_student(1, 3);
```

**Note:** MySQL uses `DELIMITER //` to change the statement delimiter temporarily, because the procedure body contains semicolons.

**SQLite Note:** SQLite does NOT support stored procedures or functions. All logic must be written in your application code (Python).

---

## Triggers

A trigger automatically runs code when an INSERT, UPDATE, or DELETE event happens on a table.

### MySQL Trigger Example: Auto-Update Timestamp

```sql
-- MySQL trigger to update timestamp on row change
DELIMITER //
CREATE TRIGGER set_updated_at
BEFORE UPDATE ON students
FOR EACH ROW
BEGIN
    SET NEW.updated_at = NOW();
END //
DELIMITER ;
```

### SQLite Trigger Example

```sql
-- SQLite trigger (simpler syntax, no DELIMITER needed)
CREATE TRIGGER set_updated_at
AFTER UPDATE ON students
FOR EACH ROW
BEGIN
    UPDATE students SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
```

### Audit Log Trigger (MySQL)

```sql
-- Create audit table
CREATE TABLE audit_log (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    table_name  VARCHAR(100),
    action      VARCHAR(10),
    old_data    JSON,
    new_data    JSON,
    changed_at  DATETIME DEFAULT NOW()
);

-- Trigger for INSERT
DELIMITER //
CREATE TRIGGER student_insert_audit
AFTER INSERT ON students
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, action, new_data)
    VALUES ('students', 'INSERT', JSON_OBJECT(
        'id', NEW.id, 'name', NEW.name, 'email', NEW.email, 'city', NEW.city
    ));
END //
DELIMITER ;

-- Trigger for UPDATE
CREATE TRIGGER student_update_audit
AFTER UPDATE ON students
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (table_name, action, old_data, new_data)
    VALUES ('students', 'UPDATE',
        JSON_OBJECT('id', OLD.id, 'name', OLD.name, 'city', OLD.city),
        JSON_OBJECT('id', NEW.id, 'name', NEW.name, 'city', NEW.city)
    );
END //
DELIMITER ;
```

---

## Views

A view is a saved query that acts like a virtual table. Views work the same way in both MySQL and SQLite.

```sql
-- Create a view
CREATE VIEW student_course_summary AS
SELECT
    s.name AS student_name,
    s.city,
    c.title AS course_title,
    c.price,
    e.enrolled_on
FROM students s
JOIN enrollments e ON s.id = e.student_id
JOIN courses c ON e.course_id = c.id;

-- Use it like a table
SELECT * FROM student_course_summary WHERE city = 'Bhopal';
```

**Note:** MySQL also supports **materialized views** through workarounds (create a regular table and refresh it with a scheduled event). SQLite does not support materialized views.

---

## Backup and Restore

### SQLite Backup

SQLite backup is simple -- just copy the `.db` file:

```bash
# Backup (just copy the file)
cp techpath.db techpath_backup.db

# Export as SQL (using sqlite3 command line)
sqlite3 techpath.db .dump > backup.sql

# Restore from SQL
sqlite3 techpath_new.db < backup.sql
```

### MySQL Backup

```bash
# Backup a database
mysqldump -u techpath -p techpath_db > backup.sql

# Backup specific tables
mysqldump -u techpath -p techpath_db students courses > tables_backup.sql

# Backup as compressed file
mysqldump -u techpath -p techpath_db | gzip > backup.sql.gz

# Restore from SQL file
mysql -u techpath -p techpath_db < backup.sql

# Restore from compressed file
gunzip < backup.sql.gz | mysql -u techpath -p techpath_db
```

---

## SQLAlchemy Connection Strings

SQLAlchemy works with both MySQL and SQLite. Here are the connection strings:

```python
from sqlalchemy import create_engine

# SQLite (development -- no server needed)
engine = create_engine("sqlite:///techpath.db")

# MySQL (production)
engine = create_engine("mysql+pymysql://techpath:password@localhost:3306/techpath_db")
```

**Required Python packages:**
```bash
pip install sqlalchemy          # ORM (works with any database)
pip install pymysql             # MySQL driver for Python
# SQLite driver is built into Python -- no extra install needed
```

---

## MySQL vs SQLite — When to Use Which?

| Scenario | Use SQLite | Use MySQL |
|----------|-----------|-----------|
| Learning SQL | Yes | - |
| Class assignments and labs | Yes | - |
| Prototyping a new app | Yes | - |
| Small personal projects | Yes | - |
| Production web application | - | Yes |
| Multiple users at the same time | - | Yes |
| Job interviews (Indian IT) | - | Yes |
| Mobile/embedded apps | Yes | - |
| Large datasets (millions of rows) | - | Yes |

**TechPath recommendation:** Start with SQLite for all labs and practice. Switch to MySQL when building production-ready projects or preparing for job interviews.

---

## Summary

| Feature | SQLite | MySQL |
|---------|--------|-------|
| Setup | Zero (built into Python) | Install server + set password |
| GUI Tool | DB Browser for SQLite | MySQL Workbench |
| Connection | `sqlite:///file.db` | `mysql+pymysql://user:pass@host/db` |
| JSON | `json_extract()` functions | Native JSON type with `->` / `->>` |
| Stored Procedures | Not supported | Supported (DELIMITER syntax) |
| Triggers | Supported (simple syntax) | Supported (DELIMITER syntax) |
| Views | Supported | Supported |
| Backup | Copy the file | `mysqldump` command |
| Best for | Learning, prototyping | Production, industry |

---

*TechPath Institute -- Python Full Stack Development*
