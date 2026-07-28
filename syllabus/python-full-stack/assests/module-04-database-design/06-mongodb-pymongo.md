# MongoDB & PyMongo — Document Databases

**Module 04 — Database Design, SQL & NoSQL | Topic 6**

---

## What is MongoDB?

MongoDB is a **document database** (NoSQL). Instead of rows in tables, data is stored as flexible JSON-like documents in collections.

**SQL vs MongoDB terminology:**

| SQL | MongoDB | Example |
|-----|---------|---------|
| Database | Database | `techpath_db` |
| Table | Collection | `students` |
| Row | Document | `{ "name": "Rahul", "city": "Bhopal" }` |
| Column | Field | `name`, `city` |
| Primary Key | `_id` | Auto-generated ObjectId |
| JOIN | Embedding / `$lookup` | Nested documents or references |

### When to Use MongoDB

| Use MongoDB When | Use PostgreSQL When |
|-----------------|---------------------|
| Data structure changes frequently | Data is highly structured and relational |
| You need flexible schemas | You need strict data integrity |
| Rapid prototyping | Complex joins and transactions |
| Storing JSON/documents naturally | ACID compliance is critical |
| Horizontal scaling (sharding) | Vertical scaling is sufficient |

---

## Installation and Setup

### Installing MongoDB

```bash
# Ubuntu
sudo apt install mongodb

# Or using Docker (recommended for development)
docker run -d --name mongodb -p 27017:27017 mongo:latest
```

### Installing PyMongo

```bash
pip install pymongo
# For async: pip install motor
```

### Connecting to MongoDB

```python
from pymongo import MongoClient

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Create/select a database
db = client["techpath_db"]

# Create/select a collection (like a table)
students = db["students"]
```

MongoDB creates databases and collections automatically when you first insert data.

---

## Documents — The Building Block

A MongoDB document is like a Python dictionary. It can have nested objects and arrays.

```python
# A simple document
student_doc = {
    "name": "Rahul Sharma",
    "email": "rahul@email.com",
    "age": 22,
    "city": "Bhopal",
    "is_active": True
}

# A document with nested data
student_doc = {
    "name": "Priya Patel",
    "email": "priya@email.com",
    "address": {
        "street": "MG Road",
        "city": "Pune",
        "state": "Maharashtra",
        "pincode": "411001"
    },
    "skills": ["Python", "FastAPI", "React"],
    "courses": [
        {"title": "Python Full Stack", "fee": 25000, "status": "active"},
        {"title": "Data Science", "fee": 30000, "status": "completed"}
    ]
}
```

Notice: No rigid schema. Each document can have different fields. This is the power (and danger) of MongoDB.

---

## CRUD Operations

### Create — Inserting Documents

```python
# Insert one document
result = students.insert_one({
    "name": "Rahul Sharma",
    "email": "rahul@email.com",
    "city": "Bhopal",
    "fee_paid": 15000
})
print(result.inserted_id)  # ObjectId('64a7b2c3...')

# Insert multiple documents
result = students.insert_many([
    {"name": "Priya Patel", "email": "priya@email.com", "city": "Pune", "fee_paid": 18000},
    {"name": "Amit Kumar", "email": "amit@email.com", "city": "Delhi", "fee_paid": 15000},
    {"name": "Sneha Gupta", "email": "sneha@email.com", "city": "Bhopal", "fee_paid": 20000},
    {"name": "Ananya Singh", "email": "ananya@email.com", "city": "Pune", "fee_paid": 22000},
])
print(result.inserted_ids)  # List of ObjectIds
```

### Read — Finding Documents

```python
# Find one document
student = students.find_one({"email": "rahul@email.com"})
print(student["name"])  # Rahul Sharma

# Find all documents
all_students = students.find()
for s in all_students:
    print(s["name"], s["city"])

# Find with conditions
bhopal_students = students.find({"city": "Bhopal"})

# Find with projection (select specific fields)
names = students.find({}, {"name": 1, "email": 1, "_id": 0})
# Returns: [{"name": "Rahul", "email": "rahul@..."}, ...]

# Find with multiple conditions (AND)
result = students.find({
    "city": "Bhopal",
    "fee_paid": {"$gte": 15000}
})

# Sort results
result = students.find().sort("name", 1)   # 1 = ascending
result = students.find().sort("fee_paid", -1)  # -1 = descending

# Limit and skip (pagination)
page_1 = students.find().sort("_id", 1).limit(10).skip(0)
page_2 = students.find().sort("_id", 1).limit(10).skip(10)

# Count documents
total = students.count_documents({"city": "Bhopal"})
```

### Query Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| `$eq` | Equal to | `{"age": {"$eq": 22}}` |
| `$ne` | Not equal | `{"city": {"$ne": "Delhi"}}` |
| `$gt` | Greater than | `{"fee_paid": {"$gt": 15000}}` |
| `$gte` | Greater than or equal | `{"fee_paid": {"$gte": 15000}}` |
| `$lt` | Less than | `{"age": {"$lt": 25}}` |
| `$lte` | Less than or equal | `{"age": {"$lte": 25}}` |
| `$in` | In a list | `{"city": {"$in": ["Bhopal", "Pune"]}}` |
| `$nin` | Not in a list | `{"city": {"$nin": ["Delhi"]}}` |
| `$and` | All conditions true | `{"$and": [{"city": "Bhopal"}, {"fee_paid": {"$gt": 10000}}]}` |
| `$or` | Any condition true | `{"$or": [{"city": "Bhopal"}, {"city": "Pune"}]}` |
| `$exists` | Field exists | `{"phone": {"$exists": True}}` |
| `$regex` | Pattern match | `{"name": {"$regex": "^R", "$options": "i"}}` |

### Update — Modifying Documents

```python
# Update one document
students.update_one(
    {"email": "rahul@email.com"},           # Filter
    {"$set": {"city": "Indore", "fee_paid": 20000}}  # Update
)

# Update multiple documents
students.update_many(
    {"city": "Bhopal"},
    {"$set": {"is_active": True}}
)

# Increment a value
students.update_one(
    {"email": "rahul@email.com"},
    {"$inc": {"fee_paid": 5000}}  # Add 5000 to fee_paid
)

# Add to an array
students.update_one(
    {"email": "rahul@email.com"},
    {"$push": {"skills": "Docker"}}
)

# Remove from an array
students.update_one(
    {"email": "rahul@email.com"},
    {"$pull": {"skills": "Docker"}}
)

# Upsert (update or insert)
students.update_one(
    {"email": "new@email.com"},
    {"$set": {"name": "New Student", "city": "Mumbai"}},
    upsert=True
)
```

### Update Operators

| Operator | What It Does | Example |
|----------|-------------|---------|
| `$set` | Set a field value | `{"$set": {"city": "Pune"}}` |
| `$unset` | Remove a field | `{"$unset": {"phone": ""}}` |
| `$inc` | Increment a number | `{"$inc": {"fee_paid": 5000}}` |
| `$push` | Add to an array | `{"$push": {"skills": "React"}}` |
| `$pull` | Remove from an array | `{"$pull": {"skills": "React"}}` |
| `$addToSet` | Add to array (no duplicates) | `{"$addToSet": {"skills": "Python"}}` |
| `$rename` | Rename a field | `{"$rename": {"phone": "mobile"}}` |

### Delete — Removing Documents

```python
# Delete one document
students.delete_one({"email": "rahul@email.com"})

# Delete multiple documents
result = students.delete_many({"is_active": False})
print(f"Deleted {result.deleted_count} documents")

# Delete all documents in a collection
students.delete_many({})

# Drop an entire collection
students.drop()
```

---

## Aggregation Pipeline

The aggregation pipeline processes documents through a series of stages — like a data processing assembly line.

```python
# Count students per city
pipeline = [
    {"$group": {
        "_id": "$city",
        "count": {"$sum": 1},
        "total_fees": {"$sum": "$fee_paid"},
        "avg_fee": {"$avg": "$fee_paid"}
    }},
    {"$sort": {"count": -1}},
]
result = students.aggregate(pipeline)
for doc in result:
    print(doc)
# {"_id": "Bhopal", "count": 3, "total_fees": 50000, "avg_fee": 16666.67}
```

### Common Pipeline Stages

| Stage | What It Does | Like SQL |
|-------|-------------|----------|
| `$match` | Filter documents | `WHERE` |
| `$group` | Group and aggregate | `GROUP BY` |
| `$sort` | Sort results | `ORDER BY` |
| `$limit` | Limit results | `LIMIT` |
| `$skip` | Skip results | `OFFSET` |
| `$project` | Select/reshape fields | `SELECT` |
| `$lookup` | Join with another collection | `JOIN` |
| `$unwind` | Flatten arrays | - |

### Complex Aggregation Example

```python
# Find top 3 cities by total fees, only where avg fee > 15000
pipeline = [
    {"$match": {"is_active": True}},
    {"$group": {
        "_id": "$city",
        "student_count": {"$sum": 1},
        "total_fees": {"$sum": "$fee_paid"},
        "avg_fee": {"$avg": "$fee_paid"},
        "students": {"$push": "$name"}
    }},
    {"$match": {"avg_fee": {"$gt": 15000}}},
    {"$sort": {"total_fees": -1}},
    {"$limit": 3},
    {"$project": {
        "city": "$_id",
        "student_count": 1,
        "total_fees": 1,
        "avg_fee": {"$round": ["$avg_fee", 2]},
        "_id": 0
    }}
]
```

### $lookup (JOIN equivalent)

```python
# Join students with their enrollments
pipeline = [
    {"$lookup": {
        "from": "enrollments",       # Collection to join
        "localField": "_id",         # Field from students
        "foreignField": "student_id", # Field from enrollments
        "as": "enrolled_courses"     # Output array name
    }},
    {"$match": {"enrolled_courses": {"$ne": []}}}  # Only students with enrollments
]
```

---

## Indexes in MongoDB

```python
# Create a single-field index
students.create_index("email", unique=True)

# Create a compound index
students.create_index([("city", 1), ("name", 1)])

# Create a text index for search
students.create_index([("name", "text"), ("bio", "text")])

# List all indexes
for index in students.list_indexes():
    print(index)

# Drop an index
students.drop_index("email_1")
```

---

## Schema Validation (Optional)

Even though MongoDB is schemaless, you can enforce rules:

```python
db.create_collection("students", validator={
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["name", "email"],
        "properties": {
            "name": {"bsonType": "string", "minLength": 1},
            "email": {"bsonType": "string", "pattern": "^.+@.+\\..+$"},
            "age": {"bsonType": "int", "minimum": 16, "maximum": 100},
            "city": {"bsonType": "string"}
        }
    }
})
```

---

## Motor — Async MongoDB for FastAPI

For production FastAPI apps, use Motor (async PyMongo):

```python
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["techpath_db"]

# Async CRUD
async def create_student(name: str, email: str):
    result = await db.students.insert_one({"name": name, "email": email})
    return str(result.inserted_id)

async def get_students(skip: int = 0, limit: int = 10):
    cursor = db.students.find().skip(skip).limit(limit)
    return await cursor.to_list(length=limit)
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| Document | JSON-like data unit (like a Python dict) |
| Collection | Group of documents (like a SQL table) |
| `insert_one/many` | Add documents |
| `find/find_one` | Query documents |
| `update_one/many` | Modify documents |
| `delete_one/many` | Remove documents |
| Aggregation pipeline | Multi-stage data processing |
| `$lookup` | MongoDB's version of JOIN |
| Motor | Async MongoDB driver for FastAPI |

---

*TechPath Institute — Python Full Stack Development*
