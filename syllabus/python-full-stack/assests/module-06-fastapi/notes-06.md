# Module 06: FastAPI — Modern API Development

## 1. What is FastAPI?

FastAPI is a **modern, high-performance** Python web framework for building APIs. It was created by Sebastian Ramirez and released in 2018.

### Why FastAPI?

| Feature | FastAPI | Flask | Django REST |
|---------|---------|-------|-------------|
| Speed | Very fast (async) | Moderate | Moderate |
| Auto docs | Yes (Swagger + ReDoc) | No | Partial |
| Type checking | Built-in (Pydantic) | Manual | Serializers |
| Async support | Native | Limited | Limited |
| Learning curve | Easy | Easy | Steep |

**Key benefits:**
- **Automatic documentation** — Swagger UI at `/docs`, ReDoc at `/redoc`
- **Data validation** — uses Pydantic models to validate request/response data
- **Type hints** — Python type hints power validation and editor autocomplete
- **Async support** — handles thousands of requests at once
- **Fast to code** — fewer bugs, less boilerplate

### ASGI vs WSGI — Explained Simply

Think of a restaurant:
- **WSGI** (Flask, Django) = one waiter who takes an order, goes to the kitchen, waits, brings the food, then takes the next order. **One thing at a time.**
- **ASGI** (FastAPI) = a waiter who takes an order, sends it to the kitchen, immediately takes the next order, and delivers food as it comes out. **Multiple things at once.**

```
WSGI (synchronous):
  Request 1 → Process → Respond → Request 2 → Process → Respond

ASGI (asynchronous):
  Request 1 → Process ──────────→ Respond
  Request 2 ──→ Process ────→ Respond
  Request 3 ────→ Process → Respond
```

### Uvicorn — The ASGI Server

Uvicorn is the server that runs FastAPI applications. Think of it like how `python manage.py runserver` runs Django.

```bash
# Install
pip install fastapi uvicorn

# Run your app
uvicorn main:app --reload

# main   = filename (main.py)
# app    = FastAPI instance variable name
# --reload = auto-restart when code changes (dev only)
```

---

## 2. Your First FastAPI App

```python
from fastapi import FastAPI

app = FastAPI(title="TechPath Student API", version="1.0")

@app.get("/")
def home():
    return {"message": "Welcome to TechPath Institute API!"}

@app.get("/about")
def about():
    return {
        "institute": "TechPath Institute",
        "city": "Bhopal",
        "courses": ["Python Full Stack", "ADCA", "DCA"]
    }
```

Run it:
```bash
uvicorn main:app --reload
```

Open in browser:
- `http://localhost:8000` — JSON response
- `http://localhost:8000/docs` — Swagger UI (interactive documentation)
- `http://localhost:8000/redoc` — ReDoc (alternative documentation)

---

## 3. Swagger UI — Auto-Generated Documentation

FastAPI automatically creates interactive API documentation. You do not need to write any documentation manually.

### Swagger UI (`/docs`)
- Test every endpoint from the browser
- Click "Try it out" → fill parameters → "Execute"
- Shows request body schemas, response examples, status codes
- Great for testing during development

### ReDoc (`/redoc`)
- Read-only documentation (no testing)
- Clean, professional look — good for sharing with clients

### Customizing Docs

```python
app = FastAPI(
    title="TechPath Student API",
    description="API for managing students at TechPath Institute, Bhopal",
    version="2.0",
    contact={
        "name": "TechPath Institute",
        "email": "info@techpath.biz"
    }
)
```

---

## 4. Routes and HTTP Methods

### HTTP Methods Explained

| Method | Purpose | Example |
|--------|---------|---------|
| `GET` | Read/fetch data | Get list of students |
| `POST` | Create new data | Add a new student |
| `PUT` | Replace entire record | Update all fields of a student |
| `PATCH` | Update part of record | Update only the marks |
| `DELETE` | Remove data | Delete a student |

### Path Parameters

Path parameters are part of the URL path. They are **required**.

```python
@app.get("/students/{student_id}")
def get_student(student_id: int):
    """Get a student by their ID"""
    return {"student_id": student_id, "name": "Rahul Sharma"}

# URL: /students/1 → student_id = 1
# URL: /students/abc → Error! (must be int)
```

### Query Parameters

Query parameters come after `?` in the URL. They are **optional** by default.

```python
from typing import Optional

@app.get("/students")
def list_students(
    city: Optional[str] = None,     # ?city=Bhopal
    course: Optional[str] = None,   # ?course=ADCA
    page: int = 1,                  # ?page=2 (default: 1)
    limit: int = 10                 # ?limit=20 (default: 10)
):
    return {
        "city": city,
        "course": course,
        "page": page,
        "limit": limit
    }

# URL: /students?city=Bhopal&course=ADCA&page=1
```

### Request Body

For `POST` and `PUT` requests, data comes in the request body as JSON.

```python
from pydantic import BaseModel

class StudentCreate(BaseModel):
    name: str
    email: str
    city: str = "Bhopal"   # default value
    marks: int

@app.post("/students")
def create_student(student: StudentCreate):
    return {"message": f"Student {student.name} created!", "data": student}

# Client sends JSON:
# {"name": "Priya Patel", "email": "priya@email.com", "marks": 92}
```

### Combining Path, Query, and Body

```python
@app.put("/students/{student_id}")
def update_student(
    student_id: int,             # from URL path
    notify: bool = False,        # from query string
    student: StudentCreate = ... # from request body (JSON)
):
    return {
        "id": student_id,
        "updated": student,
        "notification_sent": notify
    }

# PUT /students/5?notify=true
# Body: {"name": "Amit Kumar", "email": "amit@email.com", "marks": 88}
```

---

## 5. Response Models and Status Codes

### Status Codes

| Code | Meaning | When to Use |
|------|---------|-------------|
| `200` | OK | Successful GET, PUT, PATCH |
| `201` | Created | Successful POST (new record created) |
| `204` | No Content | Successful DELETE |
| `400` | Bad Request | Invalid input from client |
| `401` | Unauthorized | Not logged in |
| `403` | Forbidden | Logged in but not allowed |
| `404` | Not Found | Record does not exist |
| `422` | Validation Error | Pydantic validation failed |
| `500` | Server Error | Something broke on the server |

### Setting Status Codes

```python
from fastapi import FastAPI, HTTPException

@app.post("/students", status_code=201)
def create_student(student: StudentCreate):
    # Return 201 Created on success
    return {"success": True, "data": student}

@app.get("/students/{student_id}")
def get_student(student_id: int):
    student = find_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"success": True, "data": student}
```

### Response Models

Define what the response looks like using a Pydantic model:

```python
from pydantic import BaseModel
from typing import List

class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    city: str

class StudentListResponse(BaseModel):
    success: bool = True
    total: int
    data: List[StudentResponse]

@app.get("/students", response_model=StudentListResponse)
def list_students():
    """FastAPI will validate the response matches this schema"""
    return {
        "success": True,
        "total": 2,
        "data": [
            {"id": 1, "name": "Rahul", "email": "rahul@email.com", "city": "Bhopal"},
            {"id": 2, "name": "Priya", "email": "priya@email.com", "city": "Indore"}
        ]
    }
```

---

## 6. Pydantic v2 Models — Data Validation

Pydantic is the library that validates data in FastAPI. When someone sends a request, Pydantic checks if the data is correct before your code runs.

### Basic Model

```python
from pydantic import BaseModel, Field
from typing import Optional

class Student(BaseModel):
    name: str = Field(min_length=2, max_length=50, description="Student full name")
    email: str = Field(description="Student email address")
    age: int = Field(ge=16, le=60, description="Age must be 16-60")
    marks: float = Field(ge=0, le=100, description="Marks out of 100")
    city: str = "Bhopal"
    phone: Optional[str] = None
```

### Field Validators

| Validator | Type | Meaning |
|-----------|------|---------|
| `min_length` | str | Minimum characters |
| `max_length` | str | Maximum characters |
| `ge` | int/float | Greater than or equal to |
| `le` | int/float | Less than or equal to |
| `gt` | int/float | Greater than |
| `lt` | int/float | Less than |
| `pattern` | str | Regex pattern match |

### Custom Validators

```python
from pydantic import BaseModel, Field, field_validator

class Student(BaseModel):
    name: str = Field(min_length=2)
    email: str
    phone: str
    marks: float = Field(ge=0, le=100)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email — must contain @")
        return v.lower()   # normalize to lowercase

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        if not v.startswith("+91"):
            raise ValueError("Phone must start with +91 (Indian number)")
        if len(v) != 13:  # +91 + 10 digits
            raise ValueError("Phone must be +91 followed by 10 digits")
        return v
```

### Nested Models

```python
class Address(BaseModel):
    street: str
    city: str = "Bhopal"
    state: str = "Madhya Pradesh"
    pincode: str = Field(pattern=r"^\d{6}$")  # exactly 6 digits

class Student(BaseModel):
    name: str
    email: str
    address: Address  # nested model

# Client sends:
# {
#   "name": "Vikram Singh",
#   "email": "vikram@email.com",
#   "address": {
#     "street": "123 MP Nagar",
#     "city": "Bhopal",
#     "pincode": "462011"
#   }
# }
```

### model_dump() and ConfigDict

```python
from pydantic import ConfigDict

class StudentDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # can create from ORM objects
    
    id: int
    name: str
    email: str
    city: str

# Convert model to dictionary
student = StudentDB(id=1, name="Rahul", email="rahul@email.com", city="Bhopal")
data = student.model_dump()
# {'id': 1, 'name': 'Rahul', 'email': 'rahul@email.com', 'city': 'Bhopal'}

# Exclude unset fields (useful for partial updates)
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    marks: Optional[float] = None

update = StudentUpdate(marks=95)
update.model_dump(exclude_unset=True)
# {'marks': 95}  — only the fields that were actually sent
```

---

## 7. CRUD API with Database (SQLAlchemy + PostgreSQL)

A real API stores data in a database, not in a Python list. We use **SQLAlchemy** (the ORM) to talk to the database using Python objects instead of raw SQL.

### Setup

```bash
pip install fastapi uvicorn sqlalchemy asyncpg   # PostgreSQL async driver
# or for SQLite:
pip install fastapi uvicorn sqlalchemy aiosqlite
```

### Database Configuration

```python
# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./techpath.db"
# For PostgreSQL: "postgresql+asyncpg://user:password@localhost/techpath"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with async_session() as session:
        yield session
```

### SQLAlchemy Models

```python
# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    city = Column(String(50), default="Bhopal")
    marks = Column(Float, default=0)
    course_id = Column(Integer, ForeignKey("courses.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    course = relationship("Course", back_populates="students")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    duration_months = Column(Integer)
    fee = Column(Float)

    students = relationship("Student", back_populates="course")
```

### Async CRUD Endpoints

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

@app.post("/api/students", status_code=201)
async def create_student(data: StudentCreate, db: AsyncSession = Depends(get_db)):
    student = Student(**data.model_dump())
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return {"success": True, "data": student}

@app.get("/api/students")
async def list_students(
    city: str | None = None,
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    query = select(Student)
    if city:
        query = query.where(Student.city == city)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    students = result.scalars().all()
    return {"success": True, "total": len(students), "data": students}

@app.get("/api/students/{student_id}")
async def get_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"success": True, "data": student}

@app.put("/api/students/{student_id}")
async def update_student(
    student_id: int,
    data: StudentUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(student, key, value)
    await db.commit()
    await db.refresh(student)
    return {"success": True, "data": student}

@app.delete("/api/students/{student_id}")
async def delete_student(student_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await db.delete(student)
    await db.commit()
    return {"success": True, "message": f"Deleted {student.name}"}
```

---

## 8. Authentication — JWT Tokens

Authentication means verifying who the user is. We use **JWT (JSON Web Tokens)** — a secure token the server gives after login that the client sends with every request.

### How JWT Works

```
1. Client sends:  POST /login  { email, password }
2. Server checks password
3. Server creates JWT token (contains user info + expiry time)
4. Client stores the token
5. Client sends token in every request:
   Header: Authorization: Bearer eyJhbGci...
6. Server verifies token and knows who the user is
```

### Install Required Packages

```bash
pip install passlib[bcrypt] python-jose[cryptography]
```

### Password Hashing

Never store passwords as plain text. Use **bcrypt** to hash them.

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash a password (when user registers)
hashed = pwd_context.hash("rahul123")
# '$2b$12$K4v...'  — looks nothing like the original

# Verify a password (when user logs in)
pwd_context.verify("rahul123", hashed)    # True
pwd_context.verify("wrongpass", hashed)   # False
```

### Creating JWT Tokens

```python
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

def create_token(data: dict):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

### OAuth2 with Password Bearer

```python
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# This dependency extracts the token and returns the current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = find_user_by_email(payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Protect a route — only logged-in users can access
@app.get("/api/me")
async def get_my_profile(current_user = Depends(get_current_user)):
    return {"success": True, "data": current_user}
```

### Role-Based Access

```python
async def get_admin_user(current_user = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# Only admins can delete students
@app.delete("/api/students/{student_id}")
async def delete_student(student_id: int, admin = Depends(get_admin_user)):
    # Only runs if user is admin
    ...
```

---

## 9. Background Tasks

Background tasks run **after** the response is sent. Useful for:
- Sending emails
- Writing logs
- Processing files
- Sending notifications

```python
from fastapi import BackgroundTasks

def send_welcome_email(email: str, name: str):
    """This runs in the background after response is sent"""
    print(f"Sending welcome email to {name} at {email}...")
    # In real app: use smtplib or email service
    import time
    time.sleep(2)  # simulate slow email sending
    print(f"Email sent to {name}!")

def log_activity(action: str, user: str):
    with open("activity.log", "a") as f:
        f.write(f"{datetime.now()} | {user} | {action}\n")

@app.post("/api/students", status_code=201)
async def create_student(
    student: StudentCreate,
    background_tasks: BackgroundTasks
):
    # Create the student first
    new_student = save_to_db(student)

    # Schedule background tasks (run after response is sent)
    background_tasks.add_task(send_welcome_email, student.email, student.name)
    background_tasks.add_task(log_activity, "student_created", student.name)

    # Response is sent immediately — email sends in background
    return {"success": True, "data": new_student}
```

---

## 10. Dependency Injection

Dependency injection means FastAPI automatically provides things your function needs. You already use it with `Depends(get_db)` and `Depends(get_current_user)`.

### Why Use Dependencies?

- **Reuse code** — write once, use in many endpoints
- **Clean code** — keep endpoints simple
- **Easy testing** — swap real database for test database

### Creating Dependencies

```python
from fastapi import Depends, Query

# Simple dependency — pagination
def pagination_params(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=100)
):
    skip = (page - 1) * per_page
    return {"skip": skip, "limit": per_page, "page": page}

@app.get("/api/students")
async def list_students(pagination: dict = Depends(pagination_params)):
    # pagination = {"skip": 0, "limit": 10, "page": 1}
    return get_students(skip=pagination["skip"], limit=pagination["limit"])

@app.get("/api/courses")
async def list_courses(pagination: dict = Depends(pagination_params)):
    # Same pagination logic reused!
    return get_courses(skip=pagination["skip"], limit=pagination["limit"])
```

### Chaining Dependencies

```python
# Dependency 1: Get database session
async def get_db():
    async with async_session() as session:
        yield session

# Dependency 2: Get current user (depends on token)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    return find_user(payload["sub"])

# Dependency 3: Get admin user (depends on current user)
async def get_admin_user(user = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(403, "Admin only")
    return user

# Endpoint uses the chain: token → user → admin check
@app.delete("/api/students/{id}")
async def delete_student(id: int, admin = Depends(get_admin_user)):
    ...
```

---

## 11. Middleware

Middleware is code that runs **before every request** and **after every response**. It wraps around all your endpoints.

### CORS Middleware

CORS (Cross-Origin Resource Sharing) allows your frontend (running on localhost:3000) to call your API (running on localhost:8000).

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # frontend URLs
    allow_credentials=True,
    allow_methods=["*"],        # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],        # Allow all headers
)
```

### Custom Middleware — Request Timing

```python
import time
from starlette.middleware.base import BaseHTTPMiddleware

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        response.headers["X-Response-Time"] = f"{duration:.3f}s"
        print(f"{request.method} {request.url.path} — {duration:.3f}s")
        return response

app.add_middleware(TimingMiddleware)
```

### Logging Middleware

```python
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        print(f"→ {request.method} {request.url.path}")
        response = await call_next(request)
        print(f"← {response.status_code}")
        return response

app.add_middleware(LoggingMiddleware)
```

---

## 12. File Uploads

### Basic File Upload

```python
from fastapi import UploadFile, File

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size
    }
```

### Saving Uploaded Files

```python
import os

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/students/{student_id}/photo")
async def upload_photo(student_id: int, photo: UploadFile = File(...)):
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    if photo.content_type not in allowed_types:
        raise HTTPException(400, f"Only JPEG, PNG, WebP allowed. Got: {photo.content_type}")

    # Validate file size (max 2 MB)
    contents = await photo.read()
    if len(contents) > 2 * 1024 * 1024:
        raise HTTPException(400, "File too large. Max 2 MB.")

    # Save to disk
    file_path = os.path.join(UPLOAD_DIR, f"student_{student_id}_{photo.filename}")
    with open(file_path, "wb") as f:
        f.write(contents)

    return {
        "success": True,
        "message": "Photo uploaded",
        "path": file_path,
        "size_kb": round(len(contents) / 1024, 1)
    }
```

### Multiple File Upload

```python
from typing import List

@app.post("/api/upload-multiple")
async def upload_multiple(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        contents = await file.read()
        results.append({
            "filename": file.filename,
            "size_kb": round(len(contents) / 1024, 1)
        })
    return {"success": True, "uploaded": len(results), "files": results}
```

---

## 13. WebSockets — Real-Time Communication

HTTP is like sending letters — you send a request, wait for a response. WebSockets are like a phone call — both sides can talk at any time.

### Simple WebSocket Echo

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")
```

### Connection Manager Pattern (Chat Room)

```python
from fastapi import WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/chat")
async def chat(websocket: WebSocket, username: str = "Anonymous"):
    await manager.connect(websocket)
    await manager.broadcast(f"{username} joined the chat!")
    try:
        while True:
            message = await websocket.receive_text()
            await manager.broadcast(f"{username}: {message}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"{username} left the chat.")
```

### Testing WebSockets

You can test WebSockets using a simple HTML page:

```html
<!DOCTYPE html>
<html>
<body>
    <h2>TechPath Chat</h2>
    <input id="msg" placeholder="Type a message...">
    <button onclick="send()">Send</button>
    <div id="messages"></div>
    <script>
        const ws = new WebSocket("ws://localhost:8000/ws/chat?username=Rahul");
        ws.onmessage = (e) => {
            document.getElementById("messages").innerHTML += `<p>${e.data}</p>`;
        };
        function send() {
            ws.send(document.getElementById("msg").value);
            document.getElementById("msg").value = "";
        }
    </script>
</body>
</html>
```

---

## 14. Streaming Responses

Use `StreamingResponse` when sending large files or data that takes time to generate.

```python
from fastapi.responses import StreamingResponse
import io

@app.get("/api/export/students")
async def export_students_csv():
    """Download all students as a CSV file"""
    output = io.StringIO()
    output.write("ID,Name,Email,City,Marks\n")
    for s in students:
        output.write(f"{s['id']},{s['name']},{s['email']},{s['city']},{s['marks']}\n")

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=students.csv"}
    )
```

### Streaming Large Files

```python
@app.get("/api/download/{filename}")
async def download_file(filename: str):
    file_path = f"uploads/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")

    def file_generator():
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):  # Read 8KB at a time
                yield chunk

    return StreamingResponse(
        file_generator(),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
```

---

## 15. Testing FastAPI with pytest

### Setup

```bash
pip install pytest httpx pytest-asyncio
```

### Using TestClient

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to TechPath Institute API!"

def test_create_student():
    response = client.post("/api/students", json={
        "name": "Neha Gupta",
        "email": "neha@email.com",
        "city": "Indore",
        "marks": 88
    })
    assert response.status_code == 201
    assert response.json()["success"] is True
    assert response.json()["data"]["name"] == "Neha Gupta"

def test_create_student_invalid_marks():
    response = client.post("/api/students", json={
        "name": "Test",
        "email": "test@email.com",
        "marks": 150   # too high, should fail
    })
    assert response.status_code == 422  # validation error

def test_get_student_not_found():
    response = client.get("/api/students/9999")
    assert response.status_code == 404

def test_list_students():
    response = client.get("/api/students")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
```

### Testing Auth Endpoints

```python
def test_login():
    # Register first
    client.post("/api/register", json={
        "name": "Amit Kumar",
        "email": "amit@email.com",
        "password": "amit123"
    })

    # Login
    response = client.post("/api/login", data={
        "username": "amit@email.com",
        "password": "amit123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_route_without_token():
    response = client.get("/api/me")
    assert response.status_code == 401

def test_protected_route_with_token():
    # Login to get token
    login = client.post("/api/login", data={
        "username": "amit@email.com",
        "password": "amit123"
    })
    token = login.json()["access_token"]

    # Use token
    response = client.get("/api/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()["data"]["email"] == "amit@email.com"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with details
pytest -v

# Run one file
pytest test_main.py

# Run one test
pytest test_main.py::test_create_student

# Run with coverage
pip install pytest-cov
pytest --cov=. --cov-report=term-missing
```

---

## 16. Putting It All Together — Project Structure

For a real project, organize your code into multiple files:

```
student-api/
├── main.py              # FastAPI app, startup, middleware
├── database.py          # Database engine, session, Base
├── models.py            # SQLAlchemy models (Student, Course, User)
├── schemas.py           # Pydantic models (request/response)
├── auth.py              # JWT token, password hashing, dependencies
├── routes/
│   ├── students.py      # Student CRUD endpoints
│   ├── courses.py       # Course endpoints
│   └── auth.py          # Login, register endpoints
├── services/
│   ├── email.py         # Email sending (background task)
│   └── storage.py       # File upload handling
├── tests/
│   ├── test_students.py
│   ├── test_auth.py
│   └── conftest.py      # Shared test fixtures
├── uploads/             # Uploaded files
├── requirements.txt
└── .env
```

### Using APIRouter for Route Organization

```python
# routes/students.py
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/api/students", tags=["Students"])

@router.get("/")
async def list_students():
    ...

@router.post("/", status_code=201)
async def create_student():
    ...

# main.py
from routes.students import router as students_router
from routes.auth import router as auth_router

app.include_router(students_router)
app.include_router(auth_router)
```

---

## Quick Reference

| What | How |
|------|-----|
| Create app | `app = FastAPI()` |
| GET route | `@app.get("/path")` |
| POST route | `@app.post("/path", status_code=201)` |
| Path param | `def func(id: int):` |
| Query param | `def func(page: int = 1):` |
| Request body | `def func(data: MyModel):` |
| Validate field | `Field(min_length=2, ge=0, le=100)` |
| Custom validator | `@field_validator("field")` |
| Raise error | `raise HTTPException(404, "Not found")` |
| DB dependency | `db: AsyncSession = Depends(get_db)` |
| Auth dependency | `user = Depends(get_current_user)` |
| Background task | `background_tasks.add_task(func, arg)` |
| File upload | `file: UploadFile = File(...)` |
| WebSocket | `@app.websocket("/ws")` |
| CORS | `app.add_middleware(CORSMiddleware, ...)` |
| Run server | `uvicorn main:app --reload` |
| Run tests | `pytest -v` |
