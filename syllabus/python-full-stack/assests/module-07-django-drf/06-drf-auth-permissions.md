# DRF Authentication & Permissions

**Module 07 — Django & Django REST Framework | Topic 6**

---

## Why Do APIs Need Authentication?

Think of your API as a bank. You would not let anyone walk in and access any locker, right? You need to verify who the person is (authentication) and check what they are allowed to do (permissions).

- **Authentication** = "Who are you?" (showing your Aadhaar card at the bank)
- **Permission** = "What can you do?" (you can access your locker, but not the vault)

Without authentication, anyone can read, modify, or delete your data. Imagine if Sneha could delete all products from Amit's online store just by sending a DELETE request.

---

## Authentication Types in DRF

DRF supports several authentication methods out of the box:

| Authentication Type | How It Works | Best For |
|--------------------|--------------|----------|
| SessionAuthentication | Uses Django's session cookies | Browser-based apps (same domain) |
| BasicAuthentication | Sends username:password with every request | Testing only (not secure for production) |
| TokenAuthentication | Server gives a token after login; client sends it with every request | Simple mobile/SPA apps |
| JWT (JSON Web Token) | Like TokenAuth but token contains user info and expires automatically | Modern APIs, mobile apps |

### SessionAuthentication

This is what Django uses by default — it stores a session ID in a cookie. Good for when your frontend and backend are on the same domain.

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}
```

### TokenAuthentication

The server generates a unique token for each user. The client sends this token in every request header.

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'rest_framework.authtoken',  # Add this
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

Run migrations to create the token table:

```bash
python manage.py migrate
```

Generate a token for a user:

```python
# In Django shell
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

user = User.objects.get(username='rahul')
token = Token.objects.create(user=user)
print(token.key)  # e.g., "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

Client sends the token in the header:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Limitation**: Token never expires unless you manually delete it. That is why most production apps use JWT.

---

## JWT Authentication with SimpleJWT

JWT (JSON Web Token) is the industry standard for API authentication. Think of it like a movie ticket — it has your details printed on it, it expires after the show, and the theatre can verify it without calling the ticket counter.

### How JWT Works

1. Rahul sends his username and password to `/api/token/`
2. Server verifies credentials and returns two tokens:
   - **Access Token** — short-lived (5-60 minutes), used for API requests
   - **Refresh Token** — long-lived (1-30 days), used to get a new access token
3. Rahul sends the access token with every API request
4. When the access token expires, Rahul uses the refresh token to get a new one

### Installing SimpleJWT

```bash
pip install djangorestframework-simplejwt
```

### Configuration

```python
# settings.py
from datetime import timedelta

INSTALLED_APPS = [
    # ...
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,       # New refresh token on each refresh
    'BLACKLIST_AFTER_ROTATION': True,     # Old refresh token becomes invalid
    'AUTH_HEADER_TYPES': ('Bearer',),     # Authorization: Bearer <token>
}
```

### Adding Token URLs

```python
# urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # ...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

### Getting Tokens

**Obtain tokens** (login):

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "rahul", "password": "rahul123"}'
```

Response:

```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOi...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOi..."
}
```

**Use the access token** in requests:

```bash
curl http://localhost:8000/api/products/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOi..."
```

**Refresh the token** when it expires:

```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOi..."}'
```

---

## Permission Classes

Authentication tells you WHO the user is. Permissions tell you WHAT they can do.

### Built-in Permission Classes

| Permission Class | Who Gets Access |
|-----------------|----------------|
| `AllowAny` | Everyone, even without login |
| `IsAuthenticated` | Only logged-in users |
| `IsAdminUser` | Only users with `is_staff=True` |
| `IsAuthenticatedOrReadOnly` | Anyone can read; only logged-in users can write |

### Setting Permissions Globally

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

Now every endpoint requires login. You can override this per view.

### Setting Permissions Per View

```python
# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Anyone can browse products
            return [AllowAny()]
        # Only logged-in users can create/update/delete
        return [IsAuthenticated()]
```

---

## E-Commerce API Example: Amit's Online Store

Let us build a real-world example. Amit runs an online store selling electronics in Delhi. He wants:

- Anyone can browse products (no login needed)
- Only Amit (the shop owner) can add, edit, or delete products
- Registered customers can place orders

### The Product Model

```python
# shop/models.py
from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # In rupees
    stock = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - Rs.{self.price}"
```

### Custom Permission: Only Owner Can Edit

```python
# shop/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Anyone can view products.
    Only the product owner can edit or delete.
    """

    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS are safe methods — allow everyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the owner
        return obj.owner == request.user
```

### The Serializer

```python
# shop/serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    owner_name = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'owner', 'owner_name', 'created_at']
        read_only_fields = ['owner', 'created_at']
```

### The ViewSet with Permissions

```python
# shop/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the owner to the logged-in user
        serializer.save(owner=self.request.user)
```

### What Happens Now

| Action | Amit (Owner) | Priya (Customer) | Anonymous |
|--------|-------------|-------------------|-----------|
| Browse products | Yes | Yes | Yes |
| View product details | Yes | Yes | Yes |
| Add new product | Yes | Yes (as her own) | No (401) |
| Edit Amit's product | Yes | No (403 Forbidden) | No (401) |
| Delete Amit's product | Yes | No (403 Forbidden) | No (401) |

---

## Throttling — Rate Limiting

Throttling prevents abuse. Without it, someone could send 10,000 requests per second and crash your server. Think of it like a security guard at a busy Diwali sale — only a certain number of people can enter the shop per minute.

### Built-in Throttle Classes

| Throttle Class | What It Limits |
|---------------|----------------|
| `AnonRateThrottle` | Limits requests from unauthenticated users (by IP) |
| `UserRateThrottle` | Limits requests from authenticated users (by user ID) |

### Configuration

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/minute',     # Anonymous users: 20 requests per minute
        'user': '100/minute',    # Logged-in users: 100 requests per minute
    },
}
```

### Custom Throttle for Sensitive Endpoints

For login attempts, you might want stricter limits:

```python
# shop/throttles.py
from rest_framework.throttling import AnonRateThrottle

class LoginRateThrottle(AnonRateThrottle):
    rate = '5/minute'  # Only 5 login attempts per minute
```

Use it in a view:

```python
from rest_framework_simplejwt.views import TokenObtainPairView
from .throttles import LoginRateThrottle

class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [LoginRateThrottle]
```

When a user exceeds the limit, DRF returns:

```json
{
    "detail": "Request was throttled. Expected available in 42 seconds."
}
```

---

## Protecting API Endpoints — Complete Setup

Here is how Amit's complete API settings look:

```python
# settings.py
from datetime import timedelta

REST_FRAMEWORK = {
    # Authentication
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],

    # Permissions
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    # Throttling
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '30/minute',
        'user': '200/minute',
    },

    # Pagination
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

---

## Common Mistakes Beginners Make

| Mistake | Why It Is Wrong | Fix |
|---------|----------------|-----|
| Using BasicAuth in production | Sends password in every request (base64, not encrypted) | Use JWT instead |
| Never expiring tokens | Stolen tokens work forever | Set short ACCESS_TOKEN_LIFETIME |
| Using AllowAny everywhere | No security at all | Default to IsAuthenticated, open up selectively |
| Not throttling login endpoints | Allows brute-force password attacks | Add strict throttle to login views |
| Storing JWT in localStorage | Vulnerable to XSS attacks | Use httpOnly cookies for web apps |

---

## Quick Reference

| Concept | Purpose |
|---------|---------|
| SessionAuth | Cookie-based auth for same-domain browser apps |
| TokenAuth | Simple token per user, does not expire automatically |
| JWT (SimpleJWT) | Industry-standard tokens with expiry and refresh |
| IsAuthenticated | Only logged-in users |
| IsAdminUser | Only staff/admin users |
| IsAuthenticatedOrReadOnly | Anyone reads, login required to write |
| Custom Permission | Write your own rules (e.g., owner-only editing) |
| AnonRateThrottle | Rate limit anonymous users by IP |
| UserRateThrottle | Rate limit authenticated users by user ID |

---

*TechPath Institute — Python Full Stack Development Program*
