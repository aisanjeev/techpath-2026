# JWT Authentication — Securing Your API

**Module 06 — FastAPI: Modern API Development | Topic 5**

---

## Why Authentication?

Without authentication, anyone can access your API and read, modify, or delete data. Authentication verifies **who** the user is. Authorization determines **what** they can do.

| Concept | Question It Answers | Example |
|---------|-------------------|---------|
| **Authentication** | Who are you? | Login with email + password |
| **Authorization** | What can you do? | Admin can delete users, students cannot |

---

## What is JWT?

JWT (JSON Web Token) is a compact, self-contained token that securely represents user identity. After login, the server gives the client a JWT. The client sends this token with every request to prove they are logged in.

### How JWT Works

```
1. Client sends email + password
2. Server verifies credentials
3. Server creates a JWT token
4. Server sends token back to client
5. Client stores the token
6. Client sends token with every request (in Authorization header)
7. Server verifies the token and processes the request
```

### JWT Structure

A JWT has three parts separated by dots: `xxxxx.yyyyy.zzzzz`

| Part | Name | Contains |
|------|------|----------|
| `xxxxx` | Header | Algorithm used (e.g., HS256) |
| `yyyyy` | Payload | User data (id, email, role, expiry time) |
| `zzzzz` | Signature | Verification that the token is not tampered with |

**Example decoded payload:**
```json
{
    "sub": "rahul@email.com",
    "user_id": 1,
    "role": "student",
    "exp": 1690000000
}
```

---

## Password Hashing with bcrypt

Never store passwords as plain text. Always hash them.

```python
# app/core/security.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if a plain password matches the hash."""
    return pwd_context.verify(plain_password, hashed_password)
```

```python
# Usage
hashed = hash_password("MySecurePassword123")
# "$2b$12$LJ3m4ys..."  ← Random salt makes every hash unique

verify_password("MySecurePassword123", hashed)  # True
verify_password("WrongPassword", hashed)        # False
```

**Key point:** Even if two users have the same password, their hashes will be different because bcrypt adds a random salt.

---

## Creating and Verifying JWT Tokens

```python
# app/core/security.py
from datetime import datetime, timedelta
from jose import JWTError, jwt

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str) -> dict | None:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
```

---

## User Model and Schemas

```python
# app/models/user.py
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(200), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="student")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
```

```python
# app/schemas/auth.py
from pydantic import BaseModel, EmailStr, Field

class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: str
    role: str
    is_active: bool
```

---

## Authentication Endpoints

```python
# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserResponse
from app.models.user import User
from sqlalchemy import select

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    # Check if email exists
    stmt = select(User).where(User.email == data.email)
    existing = (await db.execute(stmt)).scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Create user with hashed password
    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password)
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user

@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    # Find user
    stmt = select(User).where(User.email == data.email)
    user = (await db.execute(stmt)).scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    # Create token
    token = create_access_token({
        "sub": user.email,
        "user_id": user.id,
        "role": user.role
    })
    return TokenResponse(access_token=token)
```

---

## Protecting Endpoints with Dependencies

```python
# app/api/v1/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import verify_access_token
from app.models.user import User

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get the current authenticated user from the JWT token."""
    token = credentials.credentials
    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    user = await db.get(User, payload["user_id"])
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    return user

async def get_current_admin_user(
    user: User = Depends(get_current_user)
) -> User:
    """Require the current user to be an admin."""
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user

async def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    db: AsyncSession = Depends(get_db)
) -> User | None:
    """Get user if token provided, None otherwise."""
    if not credentials:
        return None
    payload = verify_access_token(credentials.credentials)
    if not payload:
        return None
    return await db.get(User, payload["user_id"])
```

### Using Dependencies in Endpoints

```python
from app.api.v1.dependencies import get_current_user, get_current_admin_user

# Any authenticated user
@router.get("/me", response_model=UserResponse)
async def get_profile(user: User = Depends(get_current_user)):
    return user

# Admin only
@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    admin: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    # Only admins reach this code
    target = await db.get(User, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(target)
    return {"message": f"User {user_id} deleted by admin {admin.name}"}
```

---

## OAuth2 with FastAPI

FastAPI has built-in OAuth2 support that integrates with Swagger UI:

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    # form_data.username and form_data.password
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
```

This adds a "Lock" icon to Swagger UI where you can enter credentials and test protected endpoints.

---

## Security Best Practices

| Practice | Why |
|----------|-----|
| Never store plain-text passwords | Use bcrypt hashing |
| Set short token expiry (1 hour) | Limits damage if token is stolen |
| Use HTTPS in production | Prevents token interception |
| Store SECRET_KEY in .env | Never hardcode secrets |
| Validate token on every request | Use dependencies |
| Return generic "Invalid credentials" | Do not reveal if email or password was wrong |

---

## Summary

| Concept | Key Takeaway |
|---------|-------------|
| JWT | Token-based authentication, stateless |
| bcrypt | Hash passwords before storing |
| create_access_token() | Create a JWT with user data + expiry |
| verify_access_token() | Decode and validate a JWT |
| get_current_user | Dependency that extracts user from token |
| get_current_admin_user | Dependency that requires admin role |
| OAuth2PasswordBearer | Integrates with Swagger UI login |

---

*TechPath Institute — Python Full Stack Development*
