# Database Schema Design

**Module 16 -- Spec-Kit Development Methodology | Topic 5**

---

## What is Schema Design?

Database schema design is the process of organizing your data into tables, defining relationships between them, and planning how data will be stored, retrieved, and modified.

Think of it like designing an office filing cabinet. You need to decide what folders to create (tables), what information goes in each folder (columns), how folders reference each other (relationships), and how to find any document quickly (indexes). A poorly organized filing cabinet wastes hours searching for documents. A poorly designed database wastes milliseconds on every query -- and those add up to seconds for your users.

---

## ER Diagrams: The Blueprint for Your Database

An Entity-Relationship (ER) diagram is a visual representation of your database tables and their relationships. Each box represents a table, and lines between boxes show how tables are connected.

### Reading an ER Diagram

```
+------------------+          +------------------+
|     users        |          |     orders       |
+------------------+          +------------------+
| PK  id           |---+      | PK  id           |
|     name         |   |      | FK  user_id      |---+
|     email        |   +------| FK  address_id   |   |
|     phone        |          |     total_amount  |   |
|     created_at   |          |     status        |   |
+------------------+          |     created_at    |   |
                              +------------------+   |
                                                     |
+------------------+          +------------------+   |
|   addresses      |          |   order_items    |   |
+------------------+          +------------------+   |
| PK  id           |          | PK  id           |   |
| FK  user_id      |          | FK  order_id     |---+
|     street       |          | FK  product_id   |
|     city         |          |     quantity      |
|     pincode      |          |     unit_price    |
|     state        |          +------------------+
+------------------+
```

**Legend:**
- **PK** = Primary Key (unique identifier for each row)
- **FK** = Foreign Key (references another table's primary key)
- Lines show relationships between tables

---

## Relationship Types

### One-to-Many (1:N)

The most common relationship. One record in Table A relates to many records in Table B.

**Example:** One user can have many orders, but each order belongs to one user.

```
users (1) -----> (N) orders
```

In SQL, this is implemented with a foreign key:

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Many-to-Many (M:N)

When records in both tables can relate to multiple records in the other table. This requires a **junction table** (also called a bridge table or association table).

**Example:** Products can be in many categories, and categories can have many products.

```
products (M) <-----> (N) categories
                |
          product_categories (junction table)
```

```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL
);

-- Junction table
CREATE TABLE product_categories (
    product_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

### One-to-One (1:1)

Rare, but useful when you want to split a large table or separate sensitive data.

**Example:** Each user has one profile with detailed information.

```
users (1) -----> (1) user_profiles
```

---

## Normalization: Organizing Data Properly

Normalization is the process of organizing data to reduce redundancy and prevent anomalies. There are several levels (called "normal forms"), but the first three are the most important.

### First Normal Form (1NF)

**Rule:** Each column must contain a single value. No arrays or comma-separated lists.

**Violation:**

| id | name | phone_numbers |
|----|------|---------------|
| 1 | Rahul | 9876543210, 9123456789 |
| 2 | Priya | 8765432109 |

**Fixed (1NF compliant):**

**users table:**

| id | name |
|----|------|
| 1 | Rahul |
| 2 | Priya |

**user_phones table:**

| id | user_id | phone_number |
|----|---------|-------------|
| 1 | 1 | 9876543210 |
| 2 | 1 | 9123456789 |
| 3 | 2 | 8765432109 |

### Second Normal Form (2NF)

**Rule:** Must be in 1NF, and every non-key column must depend on the entire primary key (not just part of it). This mainly applies to tables with composite primary keys.

**Violation (composite key: order_id + product_id):**

| order_id | product_id | product_name | quantity |
|----------|-----------|--------------|----------|
| 101 | 5 | Basmati Rice | 2 |
| 101 | 8 | Toor Dal | 1 |

Here, `product_name` depends only on `product_id`, not on the full key. Move it to the products table.

### Third Normal Form (3NF)

**Rule:** Must be in 2NF, and no non-key column should depend on another non-key column.

**Violation:**

| id | name | city | state |
|----|------|------|-------|
| 1 | Amit | Bhopal | Madhya Pradesh |
| 2 | Meera | Pune | Maharashtra |

Here, `state` depends on `city`, not directly on the primary key. In practice, for simple apps, this level of normalization is often relaxed for performance and simplicity.

### When to Denormalize

Sometimes you intentionally break normalization for performance:

| Scenario | Normalize or Denormalize? | Reason |
|----------|--------------------------|--------|
| User's order history page | Denormalize (store total with order) | Avoid calculating total on every read |
| Product search results | Denormalize (store category name with product) | Avoid join on every search |
| Analytics dashboard | Denormalize (pre-computed aggregates) | Reporting queries are expensive |
| Data integrity is critical | Normalize | Prevent inconsistencies |

---

## Migration Strategies with Alembic

Database migrations are version-controlled changes to your database schema. Alembic is the migration tool for SQLAlchemy (used with FastAPI).

### How Migrations Work

```
Initial Schema --> Migration 001 --> Migration 002 --> Migration 003
(empty DB)       (create users)    (add orders)      (add index)
```

Each migration has two functions:
- **upgrade()**: Apply the change (move forward)
- **downgrade()**: Reverse the change (roll back)

### Creating a Migration

```bash
# Generate a migration automatically from model changes
poetry run alembic revision --autogenerate -m "create users table"

# Apply all pending migrations
poetry run alembic upgrade head

# Roll back the last migration
poetry run alembic downgrade -1

# See current migration status
poetry run alembic current
```

### Sample Migration File

```python
"""create users table

Revision ID: a1b2c3d4e5f6
Create Date: 2026-07-25 10:30:00.000000
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(200), unique=True, nullable=False),
        sa.Column('phone', sa.String(15)),
        sa.Column('city', sa.String(50)),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.func.now()),
    )

def downgrade():
    op.drop_table('users')
```

### Migration Best Practices

| Practice | Why |
|----------|-----|
| Never edit a migration that has been applied | Other environments already ran it |
| Always write a downgrade function | Enables rollback if something goes wrong |
| Test migrations on a copy of production data | Catch issues before they hit real users |
| Keep migrations small and focused | One logical change per migration |
| Name migrations descriptively | "add_phone_to_users" not "update_1" |

---

## Seed Data and Test Data

### Seed Data

Seed data is the initial data your application needs to function. For example, a list of Indian states, default admin user, or product categories.

```python
# seed_data.py
import asyncio
from app.database import get_db
from app.models import Category

async def seed_categories():
    categories = [
        {"name": "Dal & Pulses", "slug": "dal-pulses"},
        {"name": "Rice & Flour", "slug": "rice-flour"},
        {"name": "Cooking Oil", "slug": "cooking-oil"},
        {"name": "Spices & Masala", "slug": "spices-masala"},
        {"name": "Snacks & Namkeen", "slug": "snacks-namkeen"},
        {"name": "Beverages", "slug": "beverages"},
        {"name": "Dairy & Paneer", "slug": "dairy-paneer"},
        {"name": "Fruits & Vegetables", "slug": "fruits-vegetables"},
    ]
    async for db in get_db():
        for cat in categories:
            db.add(Category(**cat))
        await db.commit()
        print(f"Seeded {len(categories)} categories")

if __name__ == "__main__":
    asyncio.run(seed_categories())
```

### Test Data with Factories

Test data factories generate realistic but fake data for testing. The `faker` library is commonly used.

```python
# tests/factories.py
from faker import Faker

fake = Faker('en_IN')  # Indian locale

def make_user(**overrides):
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "city": fake.city(),
        **overrides,
    }

def make_product(**overrides):
    return {
        "name": fake.word().title() + " " + fake.word().title(),
        "price": round(fake.pyfloat(min_value=10, max_value=5000), 2),
        "description": fake.sentence(),
        "in_stock": True,
        **overrides,
    }

# Usage in tests:
# user = make_user(city="Bhopal")
# product = make_product(price=299.00, name="Toor Dal 1kg")
```

---

## Example: E-Commerce Database Schema

Here is a complete schema for a small e-commerce app, showing how all the concepts fit together.

| Table | Columns | Relationships |
|-------|---------|---------------|
| users | id, name, email, phone, password_hash, created_at | Has many orders, has many addresses |
| addresses | id, user_id, street, city, state, pincode, is_default | Belongs to user |
| categories | id, name, slug, parent_id | Has many products (via junction) |
| products | id, name, description, price, stock_quantity, image_url | Belongs to many categories |
| product_categories | product_id, category_id | Junction table |
| orders | id, user_id, address_id, total_amount, status, created_at | Belongs to user, has many order_items |
| order_items | id, order_id, product_id, quantity, unit_price | Belongs to order, references product |
| payments | id, order_id, method, transaction_id, amount, status | Belongs to order |

---

## Key Takeaways

1. ER diagrams visually represent tables and their relationships before you write SQL.
2. Use foreign keys for one-to-many relationships and junction tables for many-to-many.
3. Normalization (1NF, 2NF, 3NF) reduces data redundancy and prevents anomalies.
4. Alembic manages database migrations as version-controlled Python scripts.
5. Seed data provides initial required data; test factories generate realistic test data.
6. Design the schema on paper first, then implement it -- just like every other part of the spec-kit.

---

*TechPath Institute -- Spec-Kit Development Methodology*
