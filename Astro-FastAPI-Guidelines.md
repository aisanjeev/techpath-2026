# Astro + FastAPI Full-Stack Development Guidelines
## Complete Guide for TechPath Professional Services Website

**Project:** TechPath.biz - IT Services & Gen AI Solutions
**Stack:** Astro 5 (Frontend) + FastAPI (Backend)
**IDE:** Cursor AI
**Date:** December 2025
**Version:** 1.0

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Frontend Structure (Astro)](#frontend-structure-astro)
3. [Backend Structure (FastAPI)](#backend-structure-fastapi)
4. [Cursor IDE Configuration](#cursor-ide-configuration)
5. [Coding Guidelines](#coding-guidelines)
6. [Design System & UI Components](#design-system--ui-components)
7. [Performance & SEO Optimization](#performance--seo-optimization)
8. [Database & API Design](#database--api-design)
9. [Testing & Quality Assurance](#testing--quality-assurance)
10. [Deployment & DevOps](#deployment--devops)

---

## Architecture Overview

### 3-Tier Architecture Pattern

```
┌─────────────────────────────────────────────────────┐
│          ASTRO FRONTEND (SSR/SSG)                   │
│  - Static Pages (SEO-optimized)                     │
│  - Interactive Islands (React/Svelte)               │
│  - Zero JS by default                               │
│  - Deployed: Vercel/Netlify                         │
└────────────────┬────────────────────────────────────┘
                 │ REST API / GraphQL
                 ↓
┌─────────────────────────────────────────────────────┐
│        FASTAPI BACKEND (Async Python)               │
│  - API Routes & Endpoints                           │
│  - Business Logic & Validation                       │
│  - AI/ML Integration (LLM, Embeddings)              │
│  - Database ORM Layer                               │
│  - Authentication & Authorization                    │
│  - Deployed: Azure/Railway/Render                   │
└────────────────┬────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────┐
│    DATABASE & EXTERNAL SERVICES                     │
│  - PostgreSQL (Primary)                             │
│  - Vector DB (Weaviate/Pinecone)                    │
│  - LLM APIs (OpenAI/Claude)                         │
│  - Redis (Caching)                                  │
└─────────────────────────────────────────────────────┘
```

### Key Design Principles

- **Separation of Concerns:** Frontend handles presentation, backend handles logic
- **Type Safety:** TypeScript (Frontend) + Pydantic (Backend)
- **API-First:** Build backend APIs independent of frontend
- **Performance First:** Astro's Zero JS by default + FastAPI async
- **Scalability:** Both frontend and backend scale independently

---

## Frontend Structure (Astro)

### Directory Organization

```
techpath-frontend/
├── src/
│   ├── layouts/
│   │   ├── MainLayout.astro          # Global layout wrapper
│   │   ├── BlogLayout.astro          # Blog post layout
│   │   └── DocumentationLayout.astro # Docs layout
│   │
│   ├── pages/
│   │   ├── index.astro                        # Homepage
│   │   ├── services/
│   │   │   ├── index.astro                    # Services listing
│   │   │   ├── [slug].astro                   # Service detail (dynamic)
│   │   │   └── _components/
│   │   │       ├── ServiceCard.astro
│   │   │       ├── ServiceHero.astro
│   │   │       └── ServiceCTA.astro
│   │   │
│   │   ├── solutions/
│   │   │   ├── index.astro
│   │   │   ├── [slug].astro
│   │   │   └── _components/
│   │   │
│   │   ├── blog/
│   │   │   ├── index.astro
│   │   │   ├── [slug].astro
│   │   │   └── _components/
│   │   │
│   │   ├── pricing.astro
│   │   ├── about.astro
│   │   ├── contact.astro
│   │   ├── case-studies.astro
│   │   ├── testimonials.astro
│   │   ├── careers.astro
│   │   │
│   │   └── api/
│   │       ├── contact.ts              # Form submissions
│   │       ├── newsletter.ts           # Email signup
│   │       └── inquiry.ts              # Service inquiries
│   │
│   ├── components/
│   │   ├── shared/
│   │   │   ├── Header.astro
│   │   │   ├── Navigation.astro
│   │   │   ├── Footer.astro
│   │   │   ├── Breadcrumb.astro
│   │   │   ├── CTA.astro
│   │   │   └── SearchBar.astro
│   │   │
│   │   ├── sections/
│   │   │   ├── HeroSection.astro      # Reusable hero component
│   │   │   ├── FeaturesGrid.astro     # Features showcase
│   │   │   ├── Testimonials.astro     # Client testimonials
│   │   │   ├── PricingTable.astro     # Pricing section
│   │   │   ├── FAQSection.astro       # FAQ accordion
│   │   │   ├── ContactForm.astro      # Contact form
│   │   │   ├── StatCounter.astro      # Stats display
│   │   │   └── ServiceShowcase.astro  # Service cards
│   │   │
│   │   ├── ui/
│   │   │   ├── Button.astro
│   │   │   ├── Card.astro
│   │   │   ├── Badge.astro
│   │   │   ├── Tag.astro
│   │   │   ├── Alert.astro
│   │   │   ├── Modal.astro
│   │   │   ├── Tabs.astro
│   │   │   └── Accordion.astro
│   │   │
│   │   └── forms/
│   │       ├── Input.astro
│   │       ├── TextArea.astro
│   │       ├── Select.astro
│   │       ├── Checkbox.astro
│   │       ├── RadioGroup.astro
│   │       └── FormError.astro
│   │
│   ├── styles/
│   │   ├── globals.css               # Global styles
│   │   ├── variables.css             # CSS custom properties
│   │   ├── typography.css            # Font definitions
│   │   ├── animations.css            # Reusable animations
│   │   └── accessibility.css         # A11y utilities
│   │
│   ├── utils/
│   │   ├── api.ts                    # API client functions
│   │   ├── constants.ts              # App constants
│   │   ├── helpers.ts                # Utility functions
│   │   ├── validators.ts             # Form validation
│   │   ├── seo.ts                    # SEO utilities
│   │   └── types.ts                  # TypeScript types
│   │
│   ├── content/
│   │   ├── blog/
│   │   │   ├── getting-started.md
│   │   │   ├── ai-solutions.md
│   │   │   └── ...
│   │   ├── services/
│   │   │   ├── web-development.md
│   │   │   ├── ai-consulting.md
│   │   │   └── ...
│   │   ├── config.ts                 # Content collection config
│   │   └── index.ts                  # Export collections
│   │
│   └── env.d.ts
│
├── public/
│   ├── images/
│   │   ├── logo.svg
│   │   ├── favicon.ico
│   │   ├── og-image.jpg              # OpenGraph image
│   │   ├── hero/
│   │   ├── services/
│   │   ├── testimonials/
│   │   └── case-studies/
│   │
│   ├── fonts/
│   │   ├── inter-var.woff2
│   │   └── ...
│   │
│   ├── robots.txt
│   └── sitemap.xml
│
├── docs/
│   ├── ARCHITECTURE.md               # System architecture
│   ├── API.md                        # API documentation
│   ├── COMPONENTS.md                 # Component catalog
│   ├── DEPLOYMENT.md                 # Deployment guide
│   └── TROUBLESHOOTING.md            # Common issues
│
├── astro.config.mjs
├── tsconfig.json
├── package.json
├── tailwind.config.js
├── .prettierrc
└── .cursorrules
```

### Astro Configuration (`astro.config.mjs`)

```javascript
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';
import robotsTxt from 'astro-robots-txt';
import compress from 'astro-compress';
import { loadEnv } from 'vite';

const env = loadEnv(process.env.NODE_ENV, process.cwd(), '');

export default defineConfig({
  site: 'https://techpath.biz',
  
  integrations: [
    react({ include: ['**/react-components/*.jsx'] }),
    tailwind({ applyBaseStyles: false }),
    sitemap(),
    robotsTxt(),
    compress(),
  ],

  output: 'hybrid', // Static + SSR support

  vite: {
    define: {
      __API_BASE_URL__: JSON.stringify(env.VITE_API_BASE_URL),
    },
  },

  // Prerender high-priority pages at build time
  prerender: {
    crawlLinks: true,
    routes: ['/', '/services', '/about', '/contact'],
  },

  // Dynamic routes rendered on-demand
  dynamicRoutes: {
    include: ['**/[slug].astro'],
  },

  image: {
    service: { entrypoint: 'astro/assets/services/sharp' },
  },

  markdown: {
    syntaxHighlight: 'shiki',
  },
});
```

### TypeScript Configuration (`tsconfig.json`)

```json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "module": "esnext",
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@layouts/*": ["src/layouts/*"],
      "@utils/*": ["src/utils/*"],
      "@types/*": ["src/types/*"],
      "@styles/*": ["src/styles/*"]
    },
    "verbatimModuleSyntax": true,
    "strict": true,
    "strictNullChecks": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "skipLibCheck": true,
    "target": "ES2020",
    "lib": ["ES2020", "dom", "dom.iterable"]
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### Content Collections Configuration

```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    author: z.string(),
    image: z.string().optional(),
    tags: z.array(z.string()),
    readingTime: z.number().optional(),
  }),
});

const services = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    description: z.string(),
    icon: z.string(),
    features: z.array(z.string()),
    price: z.string().optional(),
    cta: z.string(),
  }),
});

export const collections = { blog, services };
```

---

## Backend Structure (FastAPI)

### Directory Organization

```
techpath-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI app entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                # Configuration management
│   │   ├── security.py              # JWT, auth utilities
│   │   ├── constants.py             # App constants
│   │   └── exceptions.py            # Custom exceptions
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py            # Main router
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── services.py      # Service endpoints
│   │   │   │   ├── blog.py          # Blog endpoints
│   │   │   │   ├── contact.py       # Contact/inquiry endpoints
│   │   │   │   ├── inquiry.py       # Service inquiry endpoints
│   │   │   │   ├── auth.py          # Authentication endpoints
│   │   │   │   ├── admin.py         # Admin endpoints
│   │   │   │   └── ai.py            # AI/LLM endpoints
│   │   │   │
│   │   │   └── dependencies.py      # Shared dependencies
│   │   │
│   │   └── v2/                      # Future API versions
│   │       └── ...
│   │
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── base.py                  # Base CRUD operations
│   │   ├── service.py               # Service CRUD
│   │   ├── blog.py                  # Blog CRUD
│   │   ├── contact.py               # Contact CRUD
│   │   └── user.py                  # User CRUD
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── service.py               # SQLAlchemy models
│   │   ├── blog.py
│   │   ├── contact.py
│   │   ├── user.py
│   │   └── base.py                  # Base model class
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── service.py               # Pydantic schemas
│   │   ├── blog.py
│   │   ├── contact.py
│   │   ├── user.py
│   │   ├── ai.py                    # AI request/response schemas
│   │   └── common.py                # Shared schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── service_service.py       # Business logic
│   │   ├── blog_service.py
│   │   ├── contact_service.py
│   │   ├── email_service.py         # Email sending
│   │   ├── ai_service.py            # LLM integration
│   │   ├── embedding_service.py     # Vector embeddings
│   │   └── cache_service.py         # Caching logic
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py               # Database session
│   │   ├── base.py                  # Base class for models
│   │   └── migrations/              # Alembic migrations
│   │       ├── env.py
│   │       ├── script.py.mako
│   │       └── versions/
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── cors.py
│   │   ├── logging.py
│   │   └── error_handlers.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py            # Custom validators
│   │   ├── helpers.py               # Helper functions
│   │   ├── logger.py                # Logging setup
│   │   ├── enums.py                 # Enums
│   │   └── decorators.py            # Custom decorators
│   │
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py              # Pytest fixtures
│       ├── test_services.py
│       ├── test_blog.py
│       ├── test_contact.py
│       ├── test_auth.py
│       ├── test_api.py
│       └── integration/
│           └── ...
│
├── docs/
│   ├── API.md                       # API documentation
│   ├── DATABASE.md                  # Database schema
│   ├── SETUP.md                     # Local setup
│   └── DEPLOYMENT.md                # Deployment guide
│
├── .env.example
├── .env.local
├── requirements.txt
├── pyproject.toml
├── pytest.ini
├── .cursorrules
└── Makefile
```

### FastAPI Application Setup (`app/main.py`)

```python
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZIPMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.exceptions import APIException
from app.api.v1.router import router as v1_router
from app.middleware.error_handlers import setup_exception_handlers
from app.middleware.logging import LoggingMiddleware
from app.db.session import init_db

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting FastAPI application...")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down FastAPI application...")

app = FastAPI(
    title="TechPath API",
    description="API for TechPath Professional Services",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Compression middleware
app.add_middleware(GZIPMiddleware, minimum_size=1000)

# Logging middleware
app.add_middleware(LoggingMiddleware)

# Exception handlers
setup_exception_handlers(app)

# Include routers
app.include_router(v1_router, prefix="/api/v1")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "TechPath API",
        "docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Configuration Management (`app/core/config.py`)

```python
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    # App
    APP_NAME: str = "TechPath API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Server
    API_BASE_URL: str = Field(default="http://localhost:8000", env="API_BASE_URL")
    FRONTEND_URL: str = Field(default="http://localhost:3000", env="FRONTEND_URL")
    ALLOWED_HOSTS: List[str] = Field(default=["localhost", "techpath.biz"], env="ALLOWED_HOSTS")
    
    # CORS
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000"], env="CORS_ORIGINS")
    
    # Database
    DATABASE_URL: str = Field(env="DATABASE_URL")
    DATABASE_ECHO: bool = Field(default=False, env="DATABASE_ECHO")
    
    # Redis (optional for caching)
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # JWT
    SECRET_KEY: str = Field(env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # Email
    SMTP_SERVER: str = Field(env="SMTP_SERVER")
    SMTP_PORT: int = Field(default=587, env="SMTP_PORT")
    SMTP_USER: str = Field(env="SMTP_USER")
    SMTP_PASSWORD: str = Field(env="SMTP_PASSWORD")
    FROM_EMAIL: str = Field(env="FROM_EMAIL")
    
    # OpenAI/LLM
    OPENAI_API_KEY: str = Field(env="OPENAI_API_KEY")
    OPENAI_MODEL: str = Field(default="gpt-4-turbo", env="OPENAI_MODEL")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    class Config:
        env_file = ".env.local"
        case_sensitive = True

settings = Settings()
```

### API Router (`app/api/v1/router.py`)

```python
from fastapi import APIRouter
from app.api.v1.endpoints import services, blog, contact, inquiry, auth, ai

router = APIRouter()

# Include endpoint routers
router.include_router(services.router, prefix="/services", tags=["services"])
router.include_router(blog.router, prefix="/blog", tags=["blog"])
router.include_router(contact.router, prefix="/contact", tags=["contact"])
router.include_router(inquiry.router, prefix="/inquiries", tags=["inquiries"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(ai.router, prefix="/ai", tags=["ai"])
```

### Custom Exceptions (`app/core/exceptions.py`)

```python
from fastapi import status
from typing import Any, Dict, Optional

class APIException(Exception):
    """Base exception for API errors."""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or "API_ERROR"
        self.details = details or {}
        super().__init__(self.message)

class ValidationError(APIException):
    """Validation error exception."""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            details=details,
        )

class NotFoundError(APIException):
    """Resource not found exception."""
    def __init__(self, resource: str):
        super().__init__(
            f"{resource} not found",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
        )

class UnauthorizedError(APIException):
    """Unauthorized access exception."""
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED",
        )

class ForbiddenError(APIException):
    """Forbidden access exception."""
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(
            message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN",
        )
```

---

## Cursor IDE Configuration

### `.cursorrules` File (Project Root)

```
# Cursor AI Development Rules for TechPath Project

## Core Principles
- Write clean, maintainable, type-safe code
- Follow REST principles for API design
- Optimize for performance and SEO
- Write tests alongside features (TDD approach)
- Keep conversations focused and short

## Project Context
- Project: TechPath Professional Services Website
- Tech Stack: Astro 5 + FastAPI + PostgreSQL
- Target: IT Services, Gen AI Solutions provider
- SEO Focus: High ranking on Google for tech services
- Deployment: Astro on Vercel, FastAPI on Azure/Railway

## Frontend (Astro) Guidelines

### File Organization
- Keep page components minimal and composable
- Extract reusable components to /components directory
- Use page-specific components in _components subfolder
- Never create deeply nested component directories

### TypeScript
- Always use TypeScript (.ts, .tsx, .astro)
- Use strict mode: `extends: "astro/tsconfigs/strict"`
- Explicitly type function parameters and return values
- Use `import type` for type-only imports
- Never use `any` type - use `unknown` with type guards instead

### Astro Components
- Keep .astro files focused (max 200 lines)
- Separate frontmatter (---) logic from HTML clearly
- Use CSS modules for component-scoped styles
- Leverage Astro Islands for interactive elements only
- Default to static/zero-JavaScript components
- Add `server:defer` only when server-side rendering is needed

### Styling & Design
- Use Tailwind CSS for styling (configured in astro.config.mjs)
- Maintain consistent spacing using Tailwind scale (4px base unit)
- Use CSS custom properties for theming
- Follow mobile-first responsive design approach
- Ensure WCAG AA accessibility standards

### Content Collections
- Use Astro Content Collections for blog, services, documentation
- Define strict Zod schemas for all content types
- Validate content at build time, not runtime
- Use frontmatter for metadata (title, date, tags, etc.)

## Backend (FastAPI) Guidelines

### Project Structure
- Organize by feature (services, blog, contact, etc.)
- Keep routes in /api/v{version}/endpoints/ directory
- Separate business logic in /services/ directory
- Use CRUD operations from /crud/ directory
- Database models in /models/, Pydantic schemas in /schemas/

### Async/Await Patterns
- Always use `async def` for all endpoint handlers
- Use `await` for database operations and I/O calls
- Never block the event loop with synchronous operations
- Use `asyncio.gather()` for parallel operations when appropriate

### Type Safety
- All function parameters must have type hints
- All functions must have return type hints
- Use Pydantic models for request/response validation
- Use type aliases for complex types
- Never use `Any` - use `Unknown` with type guards

### Error Handling
- Create custom exceptions inheriting from APIException
- Use appropriate HTTP status codes (400, 401, 404, 422, 500)
- Include error_code in JSON responses for frontend mapping
- Log errors with full context (request info, user info, etc.)
- Never expose internal errors to clients

### Database Design
- Use async SQLAlchemy (async engine) for all DB operations
- Define models with proper typing in /models/ directory
- Use alembic for database migrations (versioned and traceable)
- Add timestamps (created_at, updated_at) to all models
- Use relationships with proper cascading rules
- Index frequently queried columns

### API Design
- RESTful endpoints: GET, POST, PUT, DELETE
- Use query parameters for filtering/pagination
- Use request bodies for creating/updating resources
- Return consistent JSON response format:
  ```json
  {
    "success": true,
    "data": { ... },
    "message": "Optional message",
    "timestamp": "2025-12-15T18:30:00Z"
  }
  ```
- Implement pagination with limit/offset for list endpoints
- Return 201 for creation, 200 for success, 204 for delete

### AI/LLM Integration
- Isolate LLM calls in /services/ai_service.py
- Implement retry logic with exponential backoff
- Cache embeddings in vector database (Weaviate/Pinecone)
- Validate LLM responses before returning to frontend
- Log all LLM interactions for monitoring and debugging
- Never expose API keys in logs or error messages

## Testing Guidelines

### Frontend Tests
- Write Playwright tests for critical user journeys
- Test page load performance (Lighthouse scores)
- Test form submissions and validation
- Test responsive design on mobile/tablet/desktop
- Use `@testing-library/astro` for component testing

### Backend Tests
- Write unit tests for business logic (services/)
- Write integration tests for API endpoints
- Use pytest with fixtures for database setup/teardown
- Mock external services (LLM, email, etc.)
- Aim for 80%+ code coverage on critical paths
- Test error scenarios and edge cases

### Pre-commit Checks
- Run TypeScript compiler (`astro check`)
- Run linter (ESLint for frontend, Ruff for backend)
- Run formatter (Prettier for frontend, Black for backend)
- Run tests (playwright for frontend, pytest for backend)

## Documentation Requirements

### Code Documentation
- Add JSDoc comments for complex functions
- Document API endpoints with OpenAPI/Swagger
- Include type signatures in all documentation
- Add examples for non-obvious functionality
- Keep docs updated with code changes

### Project Documentation
- Maintain ARCHITECTURE.md for system design
- Keep API.md current with endpoint documentation
- Document database schema in DATABASE.md
- Provide setup instructions in SETUP.md
- Include troubleshooting guide in TROUBLESHOOTING.md

## Performance & Optimization

### Frontend
- Target Lighthouse scores: 95+ (Performance, Accessibility, SEO)
- Use image optimization (WebP, srcset, lazy loading)
- Minimize JavaScript (Astro's zero-JS by default)
- Implement pagination for content-heavy pages
- Use ISR (Incremental Static Regeneration) for dynamic content
- Cache static assets aggressively (Cache-Control headers)
- Monitor Core Web Vitals (LCP, FID, CLS)

### Backend
- Use database query optimization (select only needed columns)
- Implement Redis caching for expensive operations
- Use async operations for all I/O
- Monitor API response times (target: <200ms p95)
- Use connection pooling for database
- Implement rate limiting for public endpoints
- Monitor memory usage and database connections

## SEO Best Practices

### On-Page SEO
- Every page needs unique H1, title, meta description
- Use semantic HTML (header, main, article, section)
- Structure data with schema.org JSON-LD
- Optimize images with alt text and proper sizes
- Create XML sitemap and robots.txt
- Use clean, descriptive URLs

### Content SEO
- Target 2000+ words for service pages
- Use natural keyword placement (2-3% density)
- Create internal linking structure (related articles, services)
- Build backlinks through content marketing
- Use descriptive headers (H1, H2, H3 hierarchy)
- Optimize for featured snippets

### Technical SEO
- Achieve 90%+ Lighthouse score
- Implement mobile-responsive design
- Use HTTPS everywhere
- Setup proper redirects for URL changes
- Implement breadcrumb navigation
- Monitor Core Web Vitals in production

## Deployment & DevOps

### Frontend Deployment (Vercel)
- Automatic deployments from main branch
- Preview deployments for pull requests
- Environment variables for API endpoint
- Image optimization automatically
- Edge caching for static assets
- Monitoring via Vercel Analytics

### Backend Deployment (Railway/Azure)
- Use Docker for containerization
- Implement health check endpoints
- Use environment-specific configurations
- Setup auto-scaling based on load
- Monitor application logs and metrics
- Implement zero-downtime deployments

## Cursor-Specific Tips

### Using Cursor Effectively
- Start with `/docs` folder with architecture and requirements
- Use Agent mode (@agent) for multi-file changes
- Reference files with @ symbol to provide context
- Keep conversations short and focused
- Commit early and often (`git commit -m "feature: ..."`)
- Use test-driven approach: write test, then implementation
- Let AI generate tests alongside feature code
- Use images to show design references

### .cursorrules Structure
- Place rules at project root for global application
- Can override with .cursor/rules/* for specific directories
- Keep rules concise but comprehensive
- Update rules as project evolves
- Use rules to enforce consistency across team

### Workflow Pattern
1. Read existing documentation (ARCHITECTURE.md, API.md)
2. Understand context with @file references
3. Write failing test (TDD approach)
4. Implement feature to pass test
5. Commit changes with clear message
6. Move to next feature

## Code Style Preferences

### Frontend (Astro/TypeScript)
- Use const for variables, never var
- Use arrow functions for callbacks
- Destructure imports: `import { Component } from "astro"`
- Max line length: 100 characters
- Use template literals for strings
- Sort imports: external, then internal, then types
- Use trailing commas in multi-line objects/arrays

### Backend (Python/FastAPI)
- Use type hints for all functions
- Use Pydantic for validation
- Use async/await consistently
- Function names: snake_case
- Class names: PascalCase
- Constants: UPPER_SNAKE_CASE
- Use context managers (async with) for resource management
- Sort imports: stdlib, third-party, local
- Max line length: 100 characters

## Security Requirements

### Frontend
- Sanitize user input before display
- Use Content Security Policy headers
- Validate forms on client and server
- Store sensitive data securely (never in localStorage for auth tokens)
- Use httpOnly cookies for session tokens

### Backend
- Hash passwords with bcrypt (never store plaintext)
- Use JWT with expiration for API auth
- Implement rate limiting on public endpoints
- Validate all inputs with Pydantic
- Use parameterized queries to prevent SQL injection
- Never log sensitive data (passwords, tokens, API keys)
- Implement CORS properly (whitelist allowed origins)
- Use environment variables for secrets

## Monitoring & Debugging

### Frontend
- Use browser DevTools for debugging
- Monitor performance with Chrome DevTools
- Use Sentry for error tracking
- Monitor user experience metrics (Core Web Vitals)
- Setup Google Analytics for user behavior

### Backend
- Use structured logging (JSON format)
- Monitor error rates and latency
- Setup alerts for high error rates (>1%)
- Use OpenTelemetry for distributed tracing
- Monitor database query performance
- Track API endpoint response times

## Problem-Solving Approach

When facing issues:
1. Check existing documentation first (/docs folder)
2. Review error logs and stack traces carefully
3. Isolate the problem (frontend, backend, or integration)
4. Write a minimal test case to reproduce
5. Implement fix with test coverage
6. Update documentation if pattern is new
7. Commit with clear message explaining the fix

## References & Resources

- Astro Documentation: https://docs.astro.build
- FastAPI Documentation: https://fastapi.tiangolo.com
- Cursor Tips: https://cursor.sh/docs
- TypeScript Handbook: https://www.typescriptlang.org/docs
- Pydantic Documentation: https://docs.pydantic.dev
- SEO Best Practices: https://developers.google.com/search/docs
```

### Cursor Global Settings (`.cursor/rules/architecture.md`)

```markdown
# TechPath Full-Stack Architecture Rules

## Development Workflow

1. **Always check /docs folder first** - Architecture.md, API.md exist
2. **Use @file references** - Provide context to Cursor about related files
3. **Keep changes focused** - One feature at a time
4. **Test-driven development** - Write failing test → implement → pass test
5. **Commit frequently** - Small, atomic commits with clear messages

## Code Organization Principles

### Separation of Concerns
- Frontend (Astro) = Presentation layer
- Backend (FastAPI) = Business logic layer
- Database = Data persistence layer

### Feature-Based Organization
- Group related files by feature (services, blog, contact)
- Each feature has: endpoints, models, schemas, CRUD, services
- Keep concerns isolated and testable

### Type Safety First
- TypeScript for frontend (strict mode)
- Pydantic for backend (type hints everywhere)
- Never use 'any' - use specific types or unions

## Frontend Principles

### Astro-Specific
- Default to zero JavaScript (no JS unless interactive)
- Use Islands for interactive components only
- Leverage static generation for SEO
- One .astro file per route/component

### Component Design
- Small, focused components (max 150 lines)
- Props are fully typed
- CSS scoped to component
- Reusable sections in /components/sections/

### SEO Focus
- Every page: unique title, meta description, H1
- Use semantic HTML
- Structure data (JSON-LD)
- Image optimization

## Backend Principles

### API Design
- RESTful endpoints
- Consistent response format
- Proper HTTP status codes
- Comprehensive error handling

### Async First
- All endpoints are async
- No blocking operations
- Parallel operations with asyncio

### Data Validation
- Pydantic for all requests/responses
- Type hints on all functions
- Database constraints
- Input sanitization

## Integration Points

### Frontend to Backend
- REST API calls via /utils/api.ts
- Environment variable for API base URL
- Error handling and retry logic
- Request/response types match schemas

### Database Operations
- Async SQLAlchemy ORM
- Alembic migrations
- Indexes on key fields
- Proper relationships and constraints

## Performance Targets

### Frontend
- Lighthouse Performance: >90
- Largest Contentful Paint (LCP): <2.5s
- Cumulative Layout Shift (CLS): <0.1
- First Input Delay (FID): <100ms

### Backend
- API Response Time: <200ms (p95)
- Database Query Time: <50ms (p95)
- Throughput: >1000 req/sec
- Error Rate: <0.1%

## Deployment Strategy

### Frontend (Vercel)
- Automatic deployments from main
- Preview deploys for PRs
- Edge caching for assets
- Image optimization

### Backend (Railway/Azure)
- Docker containerization
- Environment-based config
- Health checks and monitoring
- Auto-scaling rules

## Testing Strategy

### Frontend
- Playwright for user journeys
- Lighthouse for performance
- Component testing for complex components
- Visual regression testing

### Backend
- Unit tests for services
- Integration tests for endpoints
- Mock external services
- Load testing for critical endpoints

## Documentation Requirements

### Keep Updated
- ARCHITECTURE.md - system design
- API.md - all endpoints
- DATABASE.md - schema and relationships
- SETUP.md - local development
- DEPLOYMENT.md - production process

### Code Comments
- Complex algorithms
- Non-obvious business logic
- Integration points
- Known limitations

## Error Handling Strategy

### Frontend
- Try-catch for async operations
- User-friendly error messages
- Fallback UI for errors
- Error logging to Sentry

### Backend
- Custom exception hierarchy
- Proper HTTP status codes
- Detailed error responses
- Structured logging

## Security Checklist

- [ ] No hardcoded secrets
- [ ] CORS properly configured
- [ ] Input validation everywhere
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (sanitize output)
- [ ] CSRF tokens for forms
- [ ] Rate limiting on public endpoints
- [ ] Password hashing (bcrypt)
- [ ] JWT with expiration
- [ ] HTTPS everywhere
```

---

## Coding Guidelines

### Frontend Code Example (Astro Component)

```astro
---
// src/components/sections/ServiceShowcase.astro
import type { Service } from '@types/service';
import ServiceCard from '@components/ui/ServiceCard.astro';
import { getServices } from '@utils/api';

interface Props {
  limit?: number;
  featured?: boolean;
}

const { limit = 6, featured = false } = Astro.props;

// Fetch services at build time (static generation)
const services: Service[] = await getServices({
  limit,
  featured,
});
---

<section class="py-24 bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    {/* Header */}
    <div class="mb-16 text-center">
      <h2 class="text-4xl font-bold text-slate-900 dark:text-white sm:text-5xl">
        Our Professional Services
      </h2>
      <p class="mt-4 text-xl text-slate-600 dark:text-slate-300">
        Cutting-edge solutions for digital transformation and AI integration
      </p>
    </div>

    {/* Services Grid */}
    <div class="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
      {services.map((service) => (
        <ServiceCard
          title={service.title}
          description={service.description}
          icon={service.icon}
          slug={service.slug}
          features={service.features}
          cta={service.cta}
        />
      ))}
    </div>

    {/* CTA */}
    <div class="mt-16 text-center">
      <a
        href="/contact"
        class="inline-block rounded-lg bg-blue-600 px-8 py-4 font-semibold text-white hover:bg-blue-700 transition-colors"
      >
        Get Started Today
      </a>
    </div>
  </div>
</section>

<style>
  section {
    scroll-margin-top: 5rem;
  }
</style>
```

### Backend Code Example (FastAPI Endpoint)

```python
# app/api/v1/endpoints/services.py
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.crud.service import service_crud
from app.db.session import get_db
from app.schemas.service import ServiceResponse, ServiceCreate
from app.core.exceptions import NotFoundError

router = APIRouter()

@router.get("/", response_model=List[ServiceResponse])
async def list_services(
    skip: int = Query(0, ge=0, le=100),
    limit: int = Query(10, ge=1, le=100),
    featured: bool = Query(False),
    db: AsyncSession = Depends(get_db),
) -> List[ServiceResponse]:
    """
    List all services with pagination and filtering.
    
    - **skip**: Number of records to skip
    - **limit**: Maximum records to return
    - **featured**: Filter featured services only
    """
    try:
        services = await service_crud.get_multi(
            db,
            skip=skip,
            limit=limit,
            featured=featured,
        )
        return services
    except Exception as e:
        logger.error(f"Error listing services: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to list services")

@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(
    service_id: int,
    db: AsyncSession = Depends(get_db),
) -> ServiceResponse:
    """Get a single service by ID."""
    service = await service_crud.get(db, id=service_id)
    if not service:
        raise NotFoundError("Service")
    return service

@router.post("/", response_model=ServiceResponse, status_code=201)
async def create_service(
    service_in: ServiceCreate,
    db: AsyncSession = Depends(get_db),
) -> ServiceResponse:
    """Create a new service."""
    service = await service_crud.create(db, obj_in=service_in)
    return service
```

---

## Design System & UI Components

### Tailwind Configuration (`tailwind.config.js`)

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        },
        secondary: {
          50: '#f8fafc',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
        },
        accent: {
          50: '#fef3c7',
          500: '#f59e0b',
          600: '#d97706',
          700: '#b45309',
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
      },
      fontSize: {
        xs: ['0.75rem', { lineHeight: '1rem' }],
        sm: ['0.875rem', { lineHeight: '1.25rem' }],
        base: ['1rem', { lineHeight: '1.5rem' }],
        lg: ['1.125rem', { lineHeight: '1.75rem' }],
        xl: ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
        '5xl': ['3rem', { lineHeight: '1' }],
      },
      spacing: {
        gutter: '1rem',
      },
      animation: {
        fadeIn: 'fadeIn 0.3s ease-in-out',
        slideUp: 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
```

### Reusable Component Library

```astro
---
// src/components/ui/Button.astro
import type { HTMLAttributes } from 'astro/types';

interface Props extends HTMLAttributes<'button'> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
}

const {
  variant = 'primary',
  size = 'md',
  disabled = false,
  class: className = '',
  ...rest
} = Astro.props;

const baseStyles = 'inline-flex items-center justify-center font-semibold rounded-lg transition-colors';

const variants = {
  primary: 'bg-primary-500 text-white hover:bg-primary-600 disabled:opacity-50',
  secondary: 'bg-secondary-100 text-secondary-700 hover:bg-secondary-200',
  outline: 'border-2 border-primary-500 text-primary-500 hover:bg-primary-50',
  ghost: 'text-primary-600 hover:bg-primary-50',
};

const sizes = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-base',
  lg: 'px-6 py-3 text-lg',
};

const finalClass = `${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`;
---

<button class={finalClass} disabled={disabled} {...rest}>
  <slot />
</button>
```

---

## Performance & SEO Optimization

### Core Web Vitals Targets

| Metric | Target | Tool |
|--------|--------|------|
| Largest Contentful Paint (LCP) | < 2.5s | Google DevTools |
| Cumulative Layout Shift (CLS) | < 0.1 | Lighthouse |
| First Input Delay (FID) | < 100ms | Web Vitals API |
| Time to First Byte (TTFB) | < 600ms | Chrome DevTools |

### SEO Checklist

- [ ] Meta title: 50-60 characters, includes primary keyword
- [ ] Meta description: 150-160 characters, action-oriented
- [ ] H1: One per page, includes primary keyword
- [ ] Internal links: Related articles/services
- [ ] Images: Optimized, WebP format, alt text
- [ ] Schema markup: Organization, LocalBusiness, Service
- [ ] Mobile responsive: 320px - 4K
- [ ] Page speed: 90+ Lighthouse score
- [ ] XML sitemap: Submitted to Google Search Console
- [ ] Robots.txt: Configured correctly
- [ ] Structured data: Tested with Rich Results Test

### Image Optimization Strategy

```astro
---
// src/components/OptimizedImage.astro
import { Image } from 'astro:assets';
import type { ImageMetadata } from 'astro';

interface Props {
  src: ImageMetadata | string;
  alt: string;
  title?: string;
  width?: number;
  height?: number;
  loading?: 'lazy' | 'eager';
}

const { src, alt, title, width, height, loading = 'lazy' } = Astro.props;
---

{typeof src === 'string' ? (
  <img
    src={src}
    alt={alt}
    title={title}
    width={width}
    height={height}
    loading={loading}
    decoding="async"
  />
) : (
  <Image
    src={src}
    alt={alt}
    title={title}
    width={width}
    height={height}
    loading={loading}
    decoding="async"
    format="webp"
  />
)}
```

---

## Database & API Design

### Database Schema Design

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Services table
CREATE TABLE services (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(255),
    featured BOOLEAN DEFAULT FALSE,
    price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Blog posts table
CREATE TABLE blog_posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER REFERENCES users(id),
    featured BOOLEAN DEFAULT FALSE,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contact inquiries table
CREATE TABLE contact_inquiries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    subject VARCHAR(255),
    message TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'new',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_services_slug ON services(slug);
CREATE INDEX idx_blog_posts_slug ON blog_posts(slug);
CREATE INDEX idx_blog_posts_published ON blog_posts(published_at);
CREATE INDEX idx_contact_status ON contact_inquiries(status);
CREATE INDEX idx_users_email ON users(email);
```

### API Response Format

```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Web Development Services",
    "description": "...",
    "slug": "web-development",
    "featured": true
  },
  "meta": {
    "timestamp": "2025-12-15T18:30:00Z",
    "version": "1.0.0"
  }
}
```

### Pagination Response

```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "total": 45,
    "page": 1,
    "per_page": 10,
    "pages": 5
  }
}
```

---

## Testing & Quality Assurance

### Frontend Testing Example (Playwright)

```typescript
// tests/e2e/homepage.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Homepage', () => {
  test('should load homepage', async ({ page }) => {
    await page.goto('/');
    const heading = page.locator('h1');
    await expect(heading).toBeVisible();
  });

  test('should display services section', async ({ page }) => {
    await page.goto('/');
    const services = page.locator('[data-testid="service-card"]');
    await expect(services).toHaveCount(6);
  });

  test('should meet performance targets', async ({ page }) => {
    await page.goto('/');
    const metrics = await page.evaluate(() => {
      const paint = performance.getEntriesByType('paint');
      const nav = performance.getEntriesByType('navigation')[0];
      return {
        fcp: paint.find(p => p.name === 'first-contentful-paint')?.startTime,
        lcp: performance.getEntriesByType('largest-contentful-paint')[0]?.startTime,
        loadTime: nav.loadEventEnd - nav.fetchStart,
      };
    });

    expect(metrics.fcp!).toBeLessThan(1800);
    expect(metrics.lcp!).toBeLessThan(2500);
    expect(metrics.loadTime).toBeLessThan(3000);
  });
});
```

### Backend Testing Example (pytest)

```python
# tests/test_services.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def sample_service():
    return {
        "title": "Web Development",
        "description": "Professional web development services",
        "slug": "web-development",
        "featured": True,
    }

def test_list_services():
    response = client.get("/api/v1/services/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_service(sample_service):
    response = client.post("/api/v1/services/", json=sample_service)
    assert response.status_code == 201
    assert response.json()["title"] == sample_service["title"]

def test_get_service(sample_service):
    # Create service
    create_response = client.post("/api/v1/services/", json=sample_service)
    service_id = create_response.json()["id"]

    # Get service
    response = client.get(f"/api/v1/services/{service_id}")
    assert response.status_code == 200
    assert response.json()["slug"] == sample_service["slug"]

def test_service_not_found():
    response = client.get("/api/v1/services/9999")
    assert response.status_code == 404
```

---

## Deployment & DevOps

### Frontend Deployment (Vercel)

Create `vercel.json`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "astro",
  "env": {
    "VITE_API_BASE_URL": "@vite_api_base_url"
  },
  "regions": ["iad1", "sfo1", "dfw1", "sin1"],
  "functions": {
    "api/**/*.ts": {
      "memory": 1024,
      "maxDuration": 30
    }
  }
}
```

### Backend Deployment (Railway/Azure)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app ./app
COPY .env.local .

# Run migrations
RUN alembic upgrade head

# Start server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Create `docker-compose.yml` for local development:

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/techpath
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - .:/app

  db:
    image: postgres:15
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=techpath
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

---

## Website Structure for TechPath

### Homepage Sections

```
1. Hero Section
   - Headline: "AI-Powered IT Solutions for Modern Enterprises"
   - Subheading: "Cutting-edge development, Gen AI consulting, and managed support"
   - CTA: "Get Started" + "View Services"
   - Background: Gradient with subtle animation

2. Trust Indicators
   - Client logos (6-8 companies)
   - Stats: "200+ Projects", "50+ Happy Clients", "15+ Years Experience"

3. Services Showcase
   - 6 service cards: Web Dev, AI Solutions, Cloud, DevOps, Training, Support
   - Icons, descriptions, CTAs

4. Why Choose Us
   - Value propositions (5-6 points)
   - Icons and descriptions
   - Compare with competitors (if applicable)

5. Case Studies / Testimonials
   - 3-4 successful projects
   - Client testimonials with photos
   - Metrics and results

6. Pricing Section
   - 3 pricing tiers
   - Feature comparison table
   - Popular badge on recommended tier

7. FAQ Section
   - 8-10 common questions
   - Expandable accordion
   - Contact CTA at bottom

8. Latest Blog Posts
   - 3 featured articles
   - "Read more" CTA

9. Contact/CTA Section
   - Form or contact details
   - "Let's Work Together" message
   - Multiple CTAs (call, email, chat)

10. Footer
    - Company info
    - Quick links
    - Services (with links)
    - Resources
    - Social media
    - Newsletter signup
    - Contact info
```

---

## Quick Reference Checklist

### Before Starting Development
- [ ] Read ARCHITECTURE.md and API.md in /docs folder
- [ ] Setup Cursor .cursorrules file
- [ ] Install dependencies: `npm install` (frontend), `pip install -r requirements.txt` (backend)
- [ ] Setup .env files with required variables
- [ ] Start Docker containers: `docker-compose up`
- [ ] Run database migrations: `alembic upgrade head`
- [ ] Verify localhost:3000 (frontend) and localhost:8000 (backend)

### During Development
- [ ] Commit frequently with clear messages
- [ ] Reference @files in Cursor for context
- [ ] Keep code focused and testable
- [ ] Write tests alongside code
- [ ] Update documentation as you code
- [ ] Run linters and formatters before commit

### Before Deployment
- [ ] Run all tests locally
- [ ] Check Lighthouse score (>90)
- [ ] Verify API endpoints in Swagger UI
- [ ] Test form submissions
- [ ] Check mobile responsiveness
- [ ] Verify error handling
- [ ] Update .env files
- [ ] Create database backups
- [ ] Setup monitoring and alerts

### Post-Deployment
- [ ] Monitor error rates
- [ ] Track Core Web Vitals
- [ ] Monitor API response times
- [ ] Setup uptime monitoring
- [ ] Configure log aggregation
- [ ] Setup performance alerts
- [ ] Regular security audits

---

## Resources & Documentation Templates

### Create these documentation files in /docs folder:

1. **ARCHITECTURE.md** - System design and technology choices
2. **API.md** - Complete API endpoint documentation
3. **DATABASE.md** - Database schema and relationships
4. **COMPONENTS.md** - Reusable component catalog
5. **SETUP.md** - Local development setup guide
6. **DEPLOYMENT.md** - Deployment process and checklist
7. **TROUBLESHOOTING.md** - Common issues and solutions
8. **SECURITY.md** - Security guidelines and best practices
9. **PERFORMANCE.md** - Performance optimization strategies
10. **CONTRIBUTING.md** - Contribution guidelines

---

## Conclusion

This comprehensive guideline document provides everything needed to build a professional, scalable, SEO-optimized website using Astro + FastAPI with industry best practices.

**Key Takeaways:**
- Astro for zero-JS frontend with superior SEO
- FastAPI for async, type-safe backend
- Clear separation of concerns and architecture
- Cursor IDE configuration for productive development
- Comprehensive testing and deployment strategies
- Performance and SEO optimizations built-in
- Professional design system with reusable components

**Next Steps:**
1. Setup project structure as outlined
2. Configure Cursor IDE with .cursorrules
3. Setup database and migrations
4. Create core components (Header, Footer, Hero, etc.)
5. Build API endpoints and database models
6. Implement authentication and security
7. Add comprehensive tests
8. Deploy to Vercel (frontend) and Railway/Azure (backend)
9. Monitor and optimize performance
10. Gather analytics and user feedback

---

**Document Version:** 1.0
**Last Updated:** December 15, 2025
**Maintained By:** TechPath Development Team
**For Updates:** Refer to /docs folder in project root

