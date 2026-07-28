# Cheat Sheet — FastAPI: Modern API Development

**Module 06 | Quick Reference Card**

---

## Quick Start

```bash
pip install "fastapi[standard]"
uvicorn main:app --reload              # Dev server at :8000
uvicorn main:app --host 0.0.0.0 --port 8080  # Custom host/port
```

```python
from fastapi import FastAPI
app = FastAPI(title="TechPath API", version="1.0.0")

@app.get("/")
def home():
    return {"message": "Hello, TechPath!"}
```

**Docs:** `http://localhost:8000/docs` (Swagger) | `/redoc` (ReDoc)

## HTTP Methods

```python
@app.get("/items")           # Read
@app.post("/items")          # Create
@app.put("/items/{id}")      # Full update
@app.patch("/items/{id}")    # Partial update
@app.delete("/items/{id}")   # Delete
```

## Path Parameters

```python
@app.get("/students/{student_id}")
def get_student(student_id: int):    # Auto-validated as int
    return {"id": student_id}
```

## Query Parameters

```python
from fastapi import Query
from typing import Optional

@app.get("/students")
def list_students(
    city: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None, min_length=1),
):
    ...
```

## Request Body (Pydantic)

```python
from pydantic import BaseModel, Field, EmailStr, ConfigDict

class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    city: str = "Bhopal"
    fee: float = Field(ge=0, default=0)

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None

class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str

@app.post("/students", response_model=StudentResponse, status_code=201)
def create(data: StudentCreate):
    ...
```

## Pydantic Validators

```python
from pydantic import field_validator, model_validator

class Student(BaseModel):
    name: str
    age: int

    @field_validator('name')
    @classmethod
    def clean_name(cls, v):
        return v.strip().title()

    @model_validator(mode='after')
    def check_age(self):
        if self.age < 16:
            raise ValueError('Must be 16+')
        return self
```

## Serialization

```python
data = student.model_dump()                    # → dict
data = student.model_dump(exclude_unset=True)  # Only sent fields
data = student.model_dump(exclude={"password"})
json_str = student.model_dump_json()           # → JSON string
obj = Student.model_validate(dict_data)        # dict → model
```

## Status Codes

```python
from fastapi import status

@app.post("/", status_code=status.HTTP_201_CREATED)
@app.delete("/", status_code=status.HTTP_204_NO_CONTENT)
```

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Validation Error |
| 500 | Server Error |

## Error Handling

```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Student not found")
raise HTTPException(status_code=409, detail="Email already exists")
```

## Dependencies

```python
from fastapi import Depends

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@app.get("/students")
async def list_students(db: AsyncSession = Depends(get_db)):
    ...

# Chain: get_db → get_current_user → get_admin_user
async def get_current_user(db = Depends(get_db)): ...
async def get_admin_user(user = Depends(get_current_user)): ...
```

## JWT Authentication

```python
from jose import jwt
from passlib.context import CryptContext

pwd = CryptContext(schemes=["bcrypt"])
pwd.hash("password")                  # Hash
pwd.verify("password", hashed)        # Verify

token = jwt.encode({"sub": email, "exp": expire}, SECRET, algorithm="HS256")
payload = jwt.decode(token, SECRET, algorithms=["HS256"])
```

## APIRouter

```python
# endpoints/students.py
from fastapi import APIRouter
router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/")
def list_students(): ...

# main.py
app.include_router(router, prefix="/api/v1")
```

## Middleware

```python
@app.middleware("http")
async def timing(request, call_next):
    start = time.time()
    response = await call_next(request)
    response.headers["X-Time"] = f"{time.time()-start:.4f}s"
    return response
```

## CORS

```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"])
```

## Background Tasks

```python
from fastapi import BackgroundTasks

def send_email(to: str): ...

@app.post("/register")
async def register(bg: BackgroundTasks):
    bg.add_task(send_email, "rahul@email.com")
    return {"status": "ok"}  # Returns immediately
```

## File Upload

```python
from fastapi import UploadFile, File

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}
```

## WebSocket

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    await websocket.send_text(f"Echo: {data}")
```

## SQLAlchemy CRUD Pattern

```python
# Create
db.add(Student(**data.model_dump())); await db.flush()

# Read
student = await db.get(Student, id)
result = await db.execute(select(Student).where(...))
students = result.scalars().all()

# Update
student.city = "Pune"; await db.flush()
# or: update_data = data.model_dump(exclude_unset=True)

# Delete
await db.delete(student); await db.flush()
```

## Testing

```python
# conftest.py
@pytest_asyncio.fixture
async def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:
        yield ac

# test_students.py
@pytest.mark.asyncio
async def test_create(client):
    r = await client.post("/api/v1/students", json={...})
    assert r.status_code == 201
```

```bash
pytest -v                              # Verbose
pytest --cov=app                       # With coverage
pytest tests/test_students.py::test_x  # Single test
pytest -k "login"                      # By keyword
```

## Project Structure

```
app/
├── main.py          # FastAPI app
├── core/
│   ├── config.py    # Settings
│   ├── database.py  # DB connection
│   └── security.py  # JWT, bcrypt
├── api/v1/
│   ├── endpoints/   # Route handlers
│   └── dependencies.py
├── models/          # SQLAlchemy
├── schemas/         # Pydantic
├── crud/            # DB operations
└── services/        # Business logic
```

---

*TechPath Institute — Python Full Stack Development*
