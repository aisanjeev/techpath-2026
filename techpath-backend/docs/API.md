# TechPath API Documentation

## Overview

The TechPath API is a RESTful API built with FastAPI. It provides endpoints for managing services, blog posts, contact inquiries, and AI-powered features.

**Base URL:** `http://localhost:8000/api/v1`

**Authentication:** Bearer token (JWT)

## Authentication

### Login

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "admin@techpath.biz",
  "password": "SecurePassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Using the Token

Include the token in the Authorization header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Response Format

### Success Response

```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message",
  "timestamp": "2025-12-16T10:30:00Z"
}
```

### Error Response

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "details": { ... }
  },
  "timestamp": "2025-12-16T10:30:00Z"
}
```

## Services

### List Services

```http
GET /api/v1/services/?skip=0&limit=20&featured=true&active_only=true
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| skip | int | Records to skip (default: 0) |
| limit | int | Max records (default: 20, max: 100) |
| featured | bool | Filter featured services |
| active_only | bool | Only active services (default: true) |

### Get Service

```http
GET /api/v1/services/{slug}
```

### Create Service (Admin)

```http
POST /api/v1/services/
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Web Development",
  "slug": "web-development",
  "description": "Full description...",
  "short_description": "Brief summary",
  "icon": "code",
  "features": ["Feature 1", "Feature 2"],
  "price": "Starting at $5,000",
  "cta_text": "Get Started",
  "featured": true,
  "display_order": 1
}
```

### Update Service (Admin)

```http
PUT /api/v1/services/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Updated Title",
  "featured": false
}
```

### Delete Service (Admin)

```http
DELETE /api/v1/services/{id}
Authorization: Bearer {token}
```

## Blog

### List Posts

```http
GET /api/v1/blog/posts?skip=0&limit=10&featured=true&tag=ai
```

### Get Post

```http
GET /api/v1/blog/posts/{slug}
```

### Create Post (Admin)

```http
POST /api/v1/blog/posts
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Getting Started with AI",
  "slug": "getting-started-with-ai",
  "content": "Full markdown content...",
  "excerpt": "Brief summary",
  "status": "published",
  "featured": true,
  "tag_ids": [1, 2]
}
```

### Upload Image (Admin)

```http
POST /api/v1/blog/posts/{id}/upload-image
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: <image file>
```

**Response:**
```json
{
  "success": true,
  "data": {
    "path": "blog/image_20251216_1030_abc12345.webp",
    "url": "/uploads/blog/image_20251216_1030_abc12345.webp"
  }
}
```

## Contact

### Submit Contact Form (Public)

```http
POST /api/v1/contact/
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "company": "Acme Corp",
  "subject": "Project Inquiry",
  "message": "I'm interested in your services...",
  "service_interest": "web-development"
}
```

### Subscribe to Newsletter (Public)

```http
POST /api/v1/contact/newsletter
Content-Type: application/json

{
  "email": "subscriber@example.com",
  "name": "Jane Doe",
  "source": "footer"
}
```

### List Inquiries (Admin)

```http
GET /api/v1/contact/inquiries?skip=0&limit=20&status=new
Authorization: Bearer {token}
```

### Update Inquiry Status (Admin)

```http
PUT /api/v1/contact/inquiries/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "status": "in_progress",
  "notes": "Contacted via phone"
}
```

## AI Endpoints

### Chat with AI

```http
POST /api/v1/ai/chat
Content-Type: application/json

{
  "message": "What services do you offer for cloud migration?",
  "conversation_history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"}
  ]
}
```

**Response:**
```json
{
  "message": "We offer comprehensive cloud migration services including..."
}
```

### Get Service Suggestions

```http
POST /api/v1/ai/suggest
Content-Type: application/json

{
  "query": "We need to modernize our legacy systems and add AI capabilities",
  "industry": "Healthcare",
  "budget": "$50,000-$100,000",
  "timeline": "6 months"
}
```

**Response:**
```json
{
  "suggestions": [
    {
      "service_name": "AI Consulting",
      "service_slug": "ai-consulting",
      "relevance_score": 0.95,
      "explanation": "Our AI consulting service can help modernize your systems..."
    }
  ],
  "reasoning": "Based on your requirements..."
}
```

### Check AI Status

```http
GET /api/v1/ai/status
```

## HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Validation Error |
| 429 | Too Many Requests |
| 500 | Internal Server Error |
| 503 | Service Unavailable |

## Rate Limiting

Public endpoints are rate limited to 100 requests per minute per IP.

## Pagination

List endpoints support pagination:
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (varies by endpoint)

## Error Codes

| Code | Description |
|------|-------------|
| `VALIDATION_ERROR` | Request validation failed |
| `NOT_FOUND` | Resource not found |
| `UNAUTHORIZED` | Authentication required |
| `FORBIDDEN` | Insufficient permissions |
| `CONFLICT` | Resource already exists |
| `RATE_LIMIT_EXCEEDED` | Too many requests |
| `EXTERNAL_SERVICE_ERROR` | External service unavailable |
| `INTERNAL_SERVER_ERROR` | Unexpected error |

