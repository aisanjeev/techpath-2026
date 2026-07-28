"""
TechPath Institute — FastAPI JWT Authentication API
=====================================================
A complete authentication system with:
- User registration with password hashing (bcrypt)
- Login endpoint returning JWT token
- Protected routes using OAuth2PasswordBearer
- Role-based access control (admin vs student)
- Token verification and current_user dependency

Run this file:
    pip install fastapi uvicorn passlib[bcrypt] python-jose[cryptography]
    uvicorn code-fastapi-auth-jwt:app --reload

Then open:
    http://localhost:8000/docs   — Swagger UI
"""

# ──────────────────────────────────────────────
# IMPORTS
# ──────────────────────────────────────────────

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from jose import jwt, JWTError

# ──────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────

# JWT settings
SECRET_KEY = "techpath-secret-key-change-this-in-production"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60  # Token is valid for 1 hour

# Password hashing setup (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme — tells FastAPI to look for token in Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


# ──────────────────────────────────────────────
# PYDANTIC SCHEMAS
# ──────────────────────────────────────────────

class UserRegister(BaseModel):
    """Schema for user registration."""
    name: str = Field(min_length=2, max_length=100, description="Full name")
    email: str = Field(description="Email address")
    password: str = Field(min_length=6, max_length=100, description="Password (min 6 chars)")
    city: str = Field(default="Bhopal", max_length=50)
    role: str = Field(default="student", description="Role: student or admin")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email format")
        return v.lower().strip()

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v not in ("student", "admin"):
            raise ValueError("Role must be 'student' or 'admin'")
        return v


class UserLogin(BaseModel):
    """Schema for login response."""
    email: str
    password: str


class UserResponse(BaseModel):
    """Schema for user data in API responses (no password)."""
    id: int
    name: str
    email: str
    city: str
    role: str
    created_at: str


class TokenResponse(BaseModel):
    """Schema for login response with JWT token."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


class ProfileUpdate(BaseModel):
    """Schema for updating user profile."""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    city: Optional[str] = Field(None, max_length=50)


# ──────────────────────────────────────────────
# IN-MEMORY USER DATABASE
# ──────────────────────────────────────────────
# In a real app, this would be a database table.
# We use a list here for simplicity.

users_db = []
next_user_id = 1


def find_user_by_email(email: str) -> Optional[dict]:
    """Find a user by email address."""
    for user in users_db:
        if user["email"] == email.lower():
            return user
    return None


def user_to_response(user: dict) -> dict:
    """Convert internal user dict to response dict (no password)."""
    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "city": user["city"],
        "role": user["role"],
        "created_at": user["created_at"],
    }


# ──────────────────────────────────────────────
# JWT TOKEN FUNCTIONS
# ──────────────────────────────────────────────

def create_access_token(data: dict) -> str:
    """
    Create a JWT token with user data and expiry time.

    Args:
        data: Dictionary with user info (e.g., {"sub": "email@example.com", "role": "student"})

    Returns:
        Encoded JWT token string
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_access_token(token: str) -> Optional[dict]:
    """
    Verify and decode a JWT token.

    Args:
        token: The JWT token string

    Returns:
        Decoded payload dict if valid, None if invalid/expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# ──────────────────────────────────────────────
# AUTH DEPENDENCIES
# ──────────────────────────────────────────────

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Dependency: Extract and verify the JWT token from the Authorization header.
    Returns the current user's data.

    Usage in endpoints:
        @app.get("/protected")
        async def protected_route(user = Depends(get_current_user)):
            return user
    """
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email = payload.get("sub")
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing user information",
        )

    user = find_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


async def get_admin_user(current_user: dict = Depends(get_current_user)) -> dict:
    """
    Dependency: Verify that the current user is an admin.
    Use this to protect admin-only routes.

    Usage:
        @app.delete("/admin-only")
        async def admin_route(admin = Depends(get_admin_user)):
            ...
    """
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required. Your role is: " + current_user["role"],
        )
    return current_user


# ──────────────────────────────────────────────
# FASTAPI APP
# ──────────────────────────────────────────────

app = FastAPI(
    title="TechPath Auth API",
    description="JWT Authentication API for TechPath Institute — register, login, and access protected routes",
    version="1.0.0",
    contact={"name": "TechPath Institute", "email": "info@techpath.biz"},
)


# ──────────────────────────────────────────────
# SEED SAMPLE USERS ON STARTUP
# ──────────────────────────────────────────────

@app.on_event("startup")
async def startup():
    """Seed sample users for testing."""
    global next_user_id

    sample_users = [
        {
            "name": "Rahul Sharma",
            "email": "rahul@techpath.biz",
            "password": "rahul123",
            "city": "Bhopal",
            "role": "admin",
        },
        {
            "name": "Priya Patel",
            "email": "priya@techpath.biz",
            "password": "priya123",
            "city": "Indore",
            "role": "student",
        },
        {
            "name": "Amit Kumar",
            "email": "amit@techpath.biz",
            "password": "amit123",
            "city": "Delhi",
            "role": "student",
        },
    ]

    for user_data in sample_users:
        users_db.append({
            "id": next_user_id,
            "name": user_data["name"],
            "email": user_data["email"],
            "password_hash": pwd_context.hash(user_data["password"]),
            "city": user_data["city"],
            "role": user_data["role"],
            "created_at": datetime.now(timezone.utc).isoformat(),
        })
        next_user_id += 1

    print("Sample users seeded!")
    print("  Admin: rahul@techpath.biz / rahul123")
    print("  Student: priya@techpath.biz / priya123")
    print("  Student: amit@techpath.biz / amit123")


# ──────────────────────────────────────────────
# PUBLIC ROUTES (no login required)
# ──────────────────────────────────────────────

@app.get("/")
async def home():
    """Welcome page with API info."""
    return {
        "success": True,
        "data": {
            "message": "Welcome to TechPath Auth API!",
            "docs": "/docs",
            "endpoints": {
                "register": "POST /api/register",
                "login": "POST /api/login",
                "profile": "GET /api/me (requires token)",
                "all_users": "GET /api/users (admin only)",
            },
            "test_accounts": {
                "admin": "rahul@techpath.biz / rahul123",
                "student": "priya@techpath.biz / priya123",
            }
        }
    }


@app.post("/api/register", status_code=201)
async def register(data: UserRegister):
    """
    Register a new user account.

    - Password is hashed using bcrypt before storing
    - Email must be unique
    - Role defaults to 'student'
    """
    global next_user_id

    # Check if email already exists
    if find_user_by_email(data.email):
        raise HTTPException(
            status_code=409,
            detail=f"Email '{data.email}' is already registered"
        )

    # Hash the password — NEVER store plain text passwords
    password_hash = pwd_context.hash(data.password)

    # Create user
    new_user = {
        "id": next_user_id,
        "name": data.name,
        "email": data.email,
        "password_hash": password_hash,
        "city": data.city,
        "role": data.role,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    users_db.append(new_user)
    next_user_id += 1

    return {
        "success": True,
        "message": f"User {data.name} registered successfully!",
        "data": user_to_response(new_user),
    }


@app.post("/api/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Log in and receive a JWT token.

    In Swagger UI:
    1. Click the "Authorize" button (lock icon at the top)
    2. Enter email as username and password
    3. Click "Authorize"
    4. Now all protected endpoints will automatically use your token

    Or use this endpoint directly:
    - username: email address
    - password: your password
    """
    # Find user by email (OAuth2 form uses "username" field)
    user = find_user_by_email(form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verify password
    if not pwd_context.verify(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT token
    token = create_access_token({
        "sub": user["email"],   # subject = user's email
        "role": user["role"],   # include role in token
        "name": user["name"],
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": TOKEN_EXPIRE_MINUTES * 60,  # in seconds
        "user": user_to_response(user),
    }


# ──────────────────────────────────────────────
# PROTECTED ROUTES (login required)
# ──────────────────────────────────────────────

@app.get("/api/me")
async def get_my_profile(current_user: dict = Depends(get_current_user)):
    """
    Get the current logged-in user's profile.
    Requires a valid JWT token in the Authorization header.
    """
    return {"success": True, "data": user_to_response(current_user)}


@app.put("/api/me")
async def update_my_profile(
    data: ProfileUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update the current user's profile (name and city only)."""
    for key, value in data.model_dump(exclude_unset=True).items():
        current_user[key] = value

    return {
        "success": True,
        "message": "Profile updated",
        "data": user_to_response(current_user),
    }


@app.get("/api/dashboard")
async def student_dashboard(current_user: dict = Depends(get_current_user)):
    """
    Student dashboard — shows personalized info.
    Any logged-in user can access this.
    """
    return {
        "success": True,
        "data": {
            "welcome": f"Welcome back, {current_user['name']}!",
            "role": current_user["role"],
            "institute": "TechPath Institute, Bhopal",
            "message": "Keep learning and building great things!",
        }
    }


# ──────────────────────────────────────────────
# ADMIN-ONLY ROUTES (admin role required)
# ──────────────────────────────────────────────

@app.get("/api/users")
async def list_all_users(admin: dict = Depends(get_admin_user)):
    """
    List all registered users. Admin only.
    Students get 403 Forbidden if they try this.
    """
    return {
        "success": True,
        "total": len(users_db),
        "data": [user_to_response(u) for u in users_db],
    }


@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int, admin: dict = Depends(get_admin_user)):
    """
    Delete a user by ID. Admin only.
    Admin cannot delete their own account.
    """
    if admin["id"] == user_id:
        raise HTTPException(status_code=400, detail="You cannot delete your own account")

    for i, user in enumerate(users_db):
        if user["id"] == user_id:
            removed = users_db.pop(i)
            return {
                "success": True,
                "message": f"Deleted user: {removed['name']} ({removed['email']})",
            }

    raise HTTPException(status_code=404, detail="User not found")


@app.put("/api/users/{user_id}/role")
async def change_user_role(
    user_id: int,
    new_role: str,
    admin: dict = Depends(get_admin_user),
):
    """
    Change a user's role. Admin only.
    new_role must be 'student' or 'admin'.
    """
    if new_role not in ("student", "admin"):
        raise HTTPException(status_code=400, detail="Role must be 'student' or 'admin'")

    for user in users_db:
        if user["id"] == user_id:
            old_role = user["role"]
            user["role"] = new_role
            return {
                "success": True,
                "message": f"Changed {user['name']}'s role from {old_role} to {new_role}",
                "data": user_to_response(user),
            }

    raise HTTPException(status_code=404, detail="User not found")


# ──────────────────────────────────────────────
# TOKEN VERIFICATION ENDPOINT (for testing)
# ──────────────────────────────────────────────

@app.post("/api/verify-token")
async def verify_token_endpoint(current_user: dict = Depends(get_current_user)):
    """
    Verify that a token is valid and return the user info.
    Useful for frontend apps to check if the stored token is still valid.
    """
    return {
        "success": True,
        "valid": True,
        "data": user_to_response(current_user),
    }


# ──────────────────────────────────────────────
# RUN (if executed directly)
# ──────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    print("Starting TechPath Auth API...")
    print("Open http://localhost:8000/docs for Swagger UI")
    print()
    print("Test accounts:")
    print("  Admin:   rahul@techpath.biz / rahul123")
    print("  Student: priya@techpath.biz / priya123")
    uvicorn.run("code-fastapi-auth-jwt:app", host="127.0.0.1", port=8000, reload=True)
