# Cloud Databases — Supabase & Neon

**Module 15 — Cloud Deployment | Topic 2**

---

## Why Cloud Databases?

When you deploy to platforms like Render or Fly.io, your app needs a database. But free-tier platforms often do not include persistent storage — data disappears on every redeploy.

**Cloud databases solve this** by hosting your database separately from your application. Your app connects to the database over the internet.

> **Analogy:** Running SQLite on your deployed app is like keeping cash in your pocket — convenient but risky (you could lose it). A cloud database is like a bank account — your data is safe, accessible from anywhere, and backed up automatically.

---

## Database Options

| Service | Type | Free Tier | Best For |
|---------|------|-----------|----------|
| **Supabase** | PostgreSQL + extras | 500 MB, 2 projects | Full-featured, auth built-in |
| **Neon** | Serverless PostgreSQL | 512 MB, auto-suspend | Serverless apps, fast cold starts |
| **Railway** | PostgreSQL | Within $5 credit | Already using Railway |
| **PlanetScale** | MySQL (Vitess) | 5 GB, 1 billion reads | MySQL projects |
| **Turso** | SQLite (libSQL) | 9 GB, 500 DBs | Edge/serverless |
| **ElephantSQL** | PostgreSQL | 20 MB (tiny) | Very small projects |

**For this course, we focus on Supabase and Neon** — both offer generous free PostgreSQL hosting.

---

## Supabase — PostgreSQL with Superpowers

Supabase is an open-source alternative to Firebase. It gives you a full PostgreSQL database plus:
- Authentication (users, login)
- Real-time subscriptions
- Storage (file uploads)
- Edge Functions
- REST API auto-generated from your tables

### Setting Up Supabase

#### Step 1: Create Account

1. Go to supabase.com
2. Sign up with GitHub
3. Click **New Project**

#### Step 2: Configure Project

| Setting | Value |
|---------|-------|
| Organization | Your name |
| Project name | `techpath-api` |
| Database password | (generate a strong one — save it!) |
| Region | Mumbai (ap-south-1) — closest to India |

#### Step 3: Get Connection String

1. Go to Project Settings → Database
2. Find the **Connection string** section
3. Choose "URI" and copy it

```
postgresql://postgres.[project-ref]:[password]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

#### Step 4: Configure Your FastAPI App

```bash
# .env.production
DATABASE_URL=postgresql+asyncpg://postgres.[ref]:[password]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

### Supabase Connection Pooling

Supabase provides two connection methods:

| Method | Port | Use Case |
|--------|------|----------|
| Direct connection | 5432 | Migrations, admin tasks |
| Connection pooler (Supavisor) | 6543 | Application connections |

**Always use port 6543 (pooler) for your app.** Direct connections are limited and should only be used for running migrations.

```python
# For app connections (pooled)
DATABASE_URL = "postgresql+asyncpg://...@pooler.supabase.com:6543/postgres"

# For migrations only (direct)
MIGRATION_URL = "postgresql+asyncpg://...@supabase.com:5432/postgres"
```

### Supabase Free Tier Limits

| Feature | Limit |
|---------|-------|
| Database size | 500 MB |
| Projects | 2 active |
| Bandwidth | 5 GB/month |
| Edge Functions | 500,000 invocations |
| Auth users | 50,000 monthly active |
| Storage | 1 GB |

---

## Neon — Serverless PostgreSQL

Neon is a serverless PostgreSQL service. "Serverless" means:
- The database starts when you connect
- It pauses when idle (saves resources)
- Scales automatically based on demand
- You pay only for what you use

### Setting Up Neon

#### Step 1: Create Account

1. Go to neon.tech
2. Sign up with GitHub

#### Step 2: Create a Project

1. Click **New Project**
2. Configure:

| Setting | Value |
|---------|-------|
| Project name | `techpath-api` |
| Region | Asia Pacific (Singapore) |
| PostgreSQL version | 16 |

#### Step 3: Get Connection String

Neon immediately shows you the connection string:

```
postgresql://techpath_owner:[password]@ep-cool-river-123456.ap-southeast-1.aws.neon.tech/techpath_db?sslmode=require
```

#### Step 4: Use in Your App

```bash
# .env.production
DATABASE_URL=postgresql+asyncpg://techpath_owner:[password]@ep-cool-river-123456.ap-southeast-1.aws.neon.tech/techpath_db?sslmode=require
```

### Neon Branching — Database Branches

Neon's killer feature is **database branching** — just like Git branches for code.

```bash
# Main database (production data)
main → https://api.techpath.biz

# Branch database (copy of production for testing)
feature/new-schema → Used by staging app
```

**How it works:**
1. Create a branch from your production database
2. The branch gets a full copy of the data (instant, no storage duplication)
3. Test your migrations on the branch
4. If everything works, merge changes to main
5. Delete the branch

This is incredibly useful for testing database migrations safely.

### Neon Free Tier Limits

| Feature | Limit |
|---------|-------|
| Storage | 512 MB |
| Compute hours | 191 hours/month |
| Branches | 10 |
| Projects | 1 |
| Auto-suspend | After 5 min of inactivity |
| History retention | 24 hours |

---

## Connecting Your FastAPI App

### SQLAlchemy Async Configuration

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./data/app.db"

    @property
    def async_database_url(self) -> str:
        """Ensure the URL uses the async driver."""
        url = self.database_url
        if url.startswith("postgresql://"):
            return url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

settings = Settings()
```

```python
# app/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(
    settings.async_database_url,
    pool_size=5,           # Max connections in pool
    max_overflow=10,       # Extra connections if pool is full
    pool_timeout=30,       # Wait time for a connection
    pool_recycle=1800,     # Recycle connections every 30 min
    echo=False,            # Set True for SQL logging
)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```

### SSL Configuration (Required for Cloud DBs)

Most cloud databases require SSL. Add `sslmode=require` to your URL:

```
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db?sslmode=require
```

### Running Migrations

```bash
# Run Alembic migrations against cloud database
DATABASE_URL="postgresql+asyncpg://..." alembic upgrade head
```

---

## SQLite vs PostgreSQL — Key Differences

Moving from SQLite (development) to PostgreSQL (production) requires awareness of differences:

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| Concurrent writes | One at a time | Many simultaneously |
| Data types | Flexible | Strict |
| JSON support | Basic | Full (JSONB) |
| Full-text search | Simple | Advanced |
| Scalability | Single file | Distributed |
| Backup | Copy the file | pg_dump, streaming |

### Common Migration Gotchas

| Issue | SQLite Behavior | PostgreSQL Behavior |
|-------|----------------|-------------------|
| Auto-increment | `AUTOINCREMENT` | `SERIAL` or `IDENTITY` |
| Boolean | Stored as 0/1 integer | Native `BOOLEAN` |
| Date/time | Stored as text | Native types |
| String comparison | Case-insensitive by default | Case-sensitive |
| Array columns | Not supported | Native `ARRAY` type |

---

## Backup Strategies

### Supabase

Supabase automatically backs up your database daily (Pro plan). On the free plan, you should manually backup:

```bash
# Manual backup using pg_dump
pg_dump "postgresql://...@supabase.com:5432/postgres" > backup.sql
```

### Neon

Neon keeps a 24-hour history on the free plan. You can restore to any point within that window.

---

## Practice Exercise

1. Create a free Supabase project (Mumbai region)
2. Get the pooled connection string (port 6543)
3. Update your FastAPI app's DATABASE_URL to use Supabase
4. Run Alembic migrations against the cloud database
5. Deploy your app to Render with the Supabase connection string
6. Repeat with Neon and compare the experience

---

*Next Topic: Static Frontend Deployment — Vercel, Netlify, custom domains, and SSL.*
