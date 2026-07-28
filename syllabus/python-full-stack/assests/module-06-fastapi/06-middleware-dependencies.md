# Middleware, Dependencies & Background Tasks

**Module 06 — FastAPI: Modern API Development | Topic 6**

---

## What is Middleware?

Middleware is code that runs **before every request** and **after every response**. It is like a security checkpoint at a building entrance — everyone passes through it, regardless of where they are going.

```
Client → Middleware (before) → Your Endpoint → Middleware (after) → Client
```

### Common Uses

| Use Case | What It Does |
|----------|-------------|
| Logging | Record every request (method, URL, time taken) |
| CORS | Allow frontend on a different domain to call your API |
| Timing | Measure how long each request takes |
| Error handling | Catch all exceptions in one place |
| Rate limiting | Block users making too many requests |

---

## Creating Custom Middleware

### Request Timing Middleware

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)  # Process the request

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    print(f"{request.method} {request.url.path} — {process_time:.4f}s")
    return response
```

### Request Logging Middleware

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log the incoming request
    print(f"→ {request.method} {request.url.path}")
    print(f"  Client: {request.client.host}")
    print(f"  Headers: {dict(request.headers)}")

    response = await call_next(request)

    # Log the response
    print(f"← {response.status_code}")
    return response
```

### CORS Middleware

CORS (Cross-Origin Resource Sharing) allows your frontend (running on `localhost:3000`) to call your API (running on `localhost:8000`). Without CORS, the browser blocks these cross-origin requests.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Next.js admin
        "http://localhost:4321",      # Astro frontend
        "https://techpath.biz",       # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],              # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],              # Accept any header
)
```

---

## Dependency Injection (DI)

Dependency Injection is a design pattern where a function receives its dependencies as parameters instead of creating them itself. FastAPI uses the `Depends()` function for this.

**Without DI:**
```python
@app.get("/students")
async def get_students():
    db = create_database_session()    # Create DB session inside
    try:
        students = await fetch_students(db)
        return students
    finally:
        await db.close()              # Must remember to close!
```

**With DI:**
```python
@app.get("/students")
async def get_students(db: AsyncSession = Depends(get_db)):
    # db is automatically created, injected, and closed
    students = await fetch_students(db)
    return students
```

### Creating Dependencies

```python
from fastapi import Depends, Query
from typing import Optional

# Simple dependency — returns a value
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

# Dependency with parameters
def pagination_params(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return")
):
    return {"skip": skip, "limit": limit}

# Using the dependency
@app.get("/students")
async def list_students(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(pagination_params)
):
    students = await get_students(db, **pagination)
    return students
```

### Dependency Chains

Dependencies can depend on other dependencies:

```python
# Level 1: Database session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Level 2: Current user (depends on db)
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    payload = verify_token(token)
    user = await db.get(User, payload["user_id"])
    if not user:
        raise HTTPException(401, "Invalid user")
    return user

# Level 3: Admin user (depends on current user)
async def get_admin_user(
    user: User = Depends(get_current_user)
) -> User:
    if user.role != "admin":
        raise HTTPException(403, "Admin required")
    return user

# Endpoint uses Level 3 (which automatically triggers Levels 2 and 1)
@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    admin: User = Depends(get_admin_user),  # Triggers the entire chain
    db: AsyncSession = Depends(get_db)
):
    ...
```

### Class-Based Dependencies

```python
class RateLimiter:
    def __init__(self, max_requests: int = 100, window: int = 60):
        self.max_requests = max_requests
        self.window = window

    async def __call__(self, request: Request):
        client_ip = request.client.host
        # Check rate limit logic here
        # Raise HTTPException(429) if exceeded
        return True

# Usage
rate_limit = RateLimiter(max_requests=60, window=60)

@app.get("/api/data", dependencies=[Depends(rate_limit)])
async def get_data():
    return {"data": "..."}
```

### Router-Level Dependencies

Apply a dependency to all endpoints in a router:

```python
admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(get_admin_user)]  # All routes require admin
)

@admin_router.get("/dashboard")
async def admin_dashboard():
    # Only admins reach here
    return {"message": "Admin Dashboard"}

@admin_router.get("/users")
async def list_users():
    # Only admins reach here too
    return {"users": []}
```

---

## Background Tasks

Background tasks run **after** the response is sent to the client. Perfect for tasks that should not slow down the response.

```python
from fastapi import BackgroundTasks

# Background task function
def send_welcome_email(email: str, name: str):
    """This runs after the response is sent."""
    print(f"Sending welcome email to {name} at {email}")
    # In reality: call email service (SendGrid, SES, etc.)

def log_activity(user_id: int, action: str):
    """Log user activity to database."""
    print(f"User {user_id} performed: {action}")

# Endpoint with background tasks
@app.post("/students", status_code=201)
async def create_student(
    data: StudentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    # Create the student (fast)
    student = await crud_create_student(db, data)

    # Queue background tasks (do not wait for them)
    background_tasks.add_task(send_welcome_email, data.email, data.name)
    background_tasks.add_task(log_activity, student.id, "registered")

    # Return immediately — email sends in the background
    return student
```

### When to Use Background Tasks

| Use Background Tasks | Do Not Use |
|----------------------|------------|
| Sending emails | Database writes (do in the request) |
| Push notifications | Anything the response depends on |
| Logging and analytics | Payment processing |
| Cache warming | File operations the user needs immediately |
| Webhook notifications | |

---

## Lifespan Events

Run code when the app starts up or shuts down:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: runs before the app starts accepting requests
    print("Starting up...")
    await create_tables()
    await warm_cache()
    redis = await connect_redis()

    yield  # App runs here

    # Shutdown: runs when the app is stopping
    print("Shutting down...")
    await redis.close()

app = FastAPI(lifespan=lifespan)
```

---

## Request Object

Access raw request data when needed:

```python
from fastapi import Request

@app.get("/info")
async def request_info(request: Request):
    return {
        "method": request.method,
        "url": str(request.url),
        "path": request.url.path,
        "query_params": dict(request.query_params),
        "client_ip": request.client.host,
        "headers": dict(request.headers),
    }
```

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| Middleware | Code that runs before/after every request |
| CORS | Allows cross-origin requests from frontend |
| Depends() | Inject dependencies into endpoints |
| Dependency chains | Dependencies can depend on other dependencies |
| BackgroundTasks | Run tasks after the response is sent |
| Lifespan events | Code for startup/shutdown |

---

*TechPath Institute — Python Full Stack Development*
