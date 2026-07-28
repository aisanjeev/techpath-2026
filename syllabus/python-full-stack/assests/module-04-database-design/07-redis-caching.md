# Redis — Caching, Sessions & Real-Time Data

**Module 04 — Database Design, SQL & NoSQL | Topic 7**

---

## What is Redis?

Redis (Remote Dictionary Server) is an **in-memory key-value store**. It stores data in RAM, making it extremely fast — hundreds of thousands of operations per second.

**Think of it this way:** PostgreSQL is your permanent filing cabinet (disk). Redis is your desk (RAM) — you keep the things you need right now on your desk for instant access.

### What Redis is Used For

| Use Case | Example |
|----------|---------|
| **Caching** | Store API responses to avoid repeated database queries |
| **Session management** | Store user login sessions |
| **Rate limiting** | Track API requests per user per minute |
| **Real-time counters** | Page views, likes, online users |
| **Pub/Sub messaging** | Chat applications, live notifications |
| **Job queues** | Background task processing |
| **Leaderboards** | Sorted sets for rankings |

### Redis vs Other Databases

| Feature | Redis | PostgreSQL | MongoDB |
|---------|-------|-----------|---------|
| Storage | RAM (in-memory) | Disk | Disk |
| Speed | Extremely fast | Fast | Fast |
| Data model | Key-value | Tables/rows | Documents |
| Persistence | Optional (RDB/AOF) | Always | Always |
| Data size | Limited by RAM | Limited by disk | Limited by disk |
| Best for | Caching, real-time | Primary data store | Flexible documents |

---

## Installation and Setup

### Installing Redis

```bash
# Ubuntu/Debian
sudo apt install redis-server
sudo systemctl start redis

# Docker (recommended)
docker run -d --name redis -p 6379:6379 redis:latest

# Verify it works
redis-cli ping
# Output: PONG
```

### Installing Python Client

```bash
pip install redis
# For async: pip install redis[hiredis]
```

### Connecting from Python

```python
import redis

# Sync connection
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Test connection
print(r.ping())  # True

# Async connection
import redis.asyncio as aioredis

async def get_redis():
    r = aioredis.Redis(host="localhost", port=6379, decode_responses=True)
    return r
```

The `decode_responses=True` parameter makes Redis return strings instead of bytes.

---

## Data Types and Commands

### Strings — The Simplest Type

```python
# SET a value
r.set("name", "Rahul Sharma")

# GET a value
name = r.get("name")  # "Rahul Sharma"

# SET with expiry (seconds)
r.set("otp:rahul", "482916", ex=300)  # Expires in 5 minutes

# SET with expiry (milliseconds)
r.set("session:abc123", "user_data", px=3600000)  # 1 hour

# SET only if key does NOT exist
r.setnx("lock:order:42", "processing")

# Increment/Decrement
r.set("page_views", 0)
r.incr("page_views")       # 1
r.incr("page_views")       # 2
r.incrby("page_views", 10) # 12
r.decr("page_views")       # 11

# Multiple SET/GET
r.mset({"city": "Bhopal", "state": "MP", "country": "India"})
values = r.mget(["city", "state", "country"])  # ["Bhopal", "MP", "India"]
```

### Key Management

```python
# Check if a key exists
r.exists("name")  # 1 (exists) or 0 (not found)

# Delete a key
r.delete("name")

# Set expiry on existing key
r.expire("session:abc", 3600)  # 1 hour

# Check remaining TTL (Time To Live)
r.ttl("otp:rahul")  # Seconds remaining, -1 if no expiry, -2 if key gone

# Find keys by pattern
r.keys("session:*")  # All session keys

# Get data type of a key
r.type("name")  # "string"
```

### Hashes — Like Python Dictionaries

Perfect for storing objects with multiple fields.

```python
# Set hash fields
r.hset("student:1", mapping={
    "name": "Rahul Sharma",
    "email": "rahul@email.com",
    "city": "Bhopal",
    "fee_paid": "15000"
})

# Get one field
name = r.hget("student:1", "name")  # "Rahul Sharma"

# Get all fields
student = r.hgetall("student:1")
# {"name": "Rahul Sharma", "email": "rahul@email.com", "city": "Bhopal", "fee_paid": "15000"}

# Update one field
r.hset("student:1", "city", "Indore")

# Increment a numeric field
r.hincrby("student:1", "fee_paid", 5000)

# Check if a field exists
r.hexists("student:1", "phone")  # False

# Delete a field
r.hdel("student:1", "city")

# Get all field names
r.hkeys("student:1")  # ["name", "email", "fee_paid"]
```

### Lists — Ordered Collections

```python
# Push to the end (right)
r.rpush("notifications:rahul", "Welcome to TechPath!")
r.rpush("notifications:rahul", "Assignment 1 due tomorrow")
r.rpush("notifications:rahul", "New module unlocked: FastAPI")

# Push to the beginning (left)
r.lpush("notifications:rahul", "URGENT: Fee payment pending")

# Get all items
r.lrange("notifications:rahul", 0, -1)
# ["URGENT: Fee payment pending", "Welcome to TechPath!", ...]

# Get items by range
r.lrange("notifications:rahul", 0, 2)  # First 3 items

# Pop from left (oldest first — queue behavior)
msg = r.lpop("notifications:rahul")

# Pop from right (newest first — stack behavior)
msg = r.rpop("notifications:rahul")

# Get list length
r.llen("notifications:rahul")

# Trim to keep only last 100 notifications
r.ltrim("notifications:rahul", -100, -1)
```

### Sets — Unique Unordered Collections

```python
# Add members
r.sadd("online_users", "rahul", "priya", "amit")

# Check membership
r.sismember("online_users", "rahul")  # True

# Get all members
r.smembers("online_users")  # {"rahul", "priya", "amit"}

# Remove a member
r.srem("online_users", "amit")

# Set operations
r.sadd("python_students", "rahul", "priya", "sneha")
r.sadd("react_students", "rahul", "amit", "ananya")

# Intersection (students in both courses)
r.sinter("python_students", "react_students")  # {"rahul"}

# Union (all unique students)
r.sunion("python_students", "react_students")  # {"rahul", "priya", "sneha", "amit", "ananya"}

# Difference (Python-only students)
r.sdiff("python_students", "react_students")  # {"priya", "sneha"}

# Count members
r.scard("online_users")  # 2
```

### Sorted Sets — Ranked Collections

Perfect for leaderboards.

```python
# Add members with scores
r.zadd("leaderboard", {
    "Rahul": 850,
    "Priya": 920,
    "Amit": 780,
    "Sneha": 890,
    "Ananya": 950
})

# Get top 3 (highest scores)
r.zrevrange("leaderboard", 0, 2, withscores=True)
# [("Ananya", 950.0), ("Priya", 920.0), ("Sneha", 890.0)]

# Get rank of a member (0-based, highest first)
r.zrevrank("leaderboard", "Rahul")  # 3

# Get score of a member
r.zscore("leaderboard", "Rahul")  # 850.0

# Increment score
r.zincrby("leaderboard", 100, "Rahul")  # 950.0

# Get members within a score range
r.zrangebyscore("leaderboard", 800, 900, withscores=True)

# Count members in score range
r.zcount("leaderboard", 800, 900)
```

---

## Caching Pattern — The Most Common Use Case

### Basic Cache-Aside Pattern

```python
import json

async def get_student(student_id: int):
    # Step 1: Check cache first
    cache_key = f"student:{student_id}"
    cached = r.get(cache_key)

    if cached:
        return json.loads(cached)  # Cache HIT

    # Step 2: Cache MISS — query database
    student = await db.execute(
        select(Student).where(Student.id == student_id)
    )
    student = student.scalar_one_or_none()

    if student:
        # Step 3: Store in cache for 5 minutes
        r.set(cache_key, json.dumps({
            "id": student.id,
            "name": student.name,
            "email": student.email
        }), ex=300)

    return student
```

### Cache Invalidation

When data changes, remove the stale cache:

```python
async def update_student(student_id: int, data: dict):
    # Update in database
    await db.execute(
        update(Student).where(Student.id == student_id).values(**data)
    )
    await db.commit()

    # Invalidate cache
    r.delete(f"student:{student_id}")
```

### Caching Best Practices

| Practice | Why |
|----------|-----|
| Always set an expiry (TTL) | Prevents stale data from living forever |
| Use meaningful key names | `student:42` not `key1` |
| Cache expensive queries | Database JOINs, aggregations |
| Do not cache sensitive data | Passwords, tokens, personal details |
| Monitor cache hit rate | If below 80%, reconsider your caching strategy |

---

## Session Management

```python
import uuid
import json

def create_session(user_id: int, user_data: dict) -> str:
    session_id = str(uuid.uuid4())
    r.set(
        f"session:{session_id}",
        json.dumps({"user_id": user_id, **user_data}),
        ex=3600  # 1 hour expiry
    )
    return session_id

def get_session(session_id: str) -> dict | None:
    data = r.get(f"session:{session_id}")
    if data:
        # Extend session on activity
        r.expire(f"session:{session_id}", 3600)
        return json.loads(data)
    return None

def destroy_session(session_id: str):
    r.delete(f"session:{session_id}")
```

---

## Pub/Sub — Real-Time Messaging

Redis Pub/Sub lets you broadcast messages to multiple subscribers.

### Publisher

```python
# Publish a message to a channel
r.publish("notifications", json.dumps({
    "type": "new_module",
    "message": "Module 5: Git & GitHub is now available!",
    "timestamp": "2026-07-25T10:00:00"
}))
```

### Subscriber

```python
# Subscribe to a channel
pubsub = r.pubsub()
pubsub.subscribe("notifications")

# Listen for messages
for message in pubsub.listen():
    if message["type"] == "message":
        data = json.loads(message["data"])
        print(f"Received: {data['message']}")
```

**Use cases:** Chat messages, live notifications, real-time dashboards, WebSocket event broadcasting.

---

## Rate Limiting

```python
def is_rate_limited(user_id: str, max_requests: int = 60, window: int = 60) -> bool:
    """Allow max_requests per window seconds."""
    key = f"rate_limit:{user_id}"
    current = r.get(key)

    if current is None:
        # First request in this window
        r.set(key, 1, ex=window)
        return False

    if int(current) >= max_requests:
        return True  # Rate limit exceeded

    r.incr(key)
    return False

# Usage in a FastAPI endpoint
@app.get("/api/data")
async def get_data(user = Depends(get_current_user)):
    if is_rate_limited(user.id, max_requests=100, window=60):
        raise HTTPException(429, "Too many requests. Try again in a minute.")
    return {"data": "..."}
```

---

## Redis with FastAPI

```python
import redis.asyncio as aioredis
from fastapi import FastAPI, Depends

app = FastAPI()

# Create Redis connection pool
redis_pool = aioredis.ConnectionPool.from_url("redis://localhost:6379")

async def get_redis():
    return aioredis.Redis(connection_pool=redis_pool, decode_responses=True)

@app.get("/student/{student_id}")
async def get_student(student_id: int, cache: aioredis.Redis = Depends(get_redis)):
    # Check cache
    cached = await cache.get(f"student:{student_id}")
    if cached:
        return {"source": "cache", "data": json.loads(cached)}

    # Fetch from database...
    student = await fetch_from_db(student_id)

    # Cache for 5 minutes
    await cache.set(f"student:{student_id}", json.dumps(student), ex=300)
    return {"source": "database", "data": student}

@app.on_event("shutdown")
async def shutdown():
    await redis_pool.disconnect()
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| Redis | In-memory key-value store — extremely fast |
| Strings | Basic key-value pairs with optional expiry |
| Hashes | Store objects with multiple fields |
| Lists | Ordered collections (queues, stacks) |
| Sets | Unique unordered collections |
| Sorted Sets | Ranked collections (leaderboards) |
| Caching | Store frequently-accessed data in Redis to reduce DB load |
| Pub/Sub | Real-time messaging between services |
| TTL | Always set expiry to prevent stale data |

---

*TechPath Institute — Python Full Stack Development*
