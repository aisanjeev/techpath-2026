# Cheat Sheet: Full-Stack AI Product — Capstone Development

**Module 17 — Quick Reference**

---

## 1. Project Idea Validation Checklist

| Check | Question to Ask |
|-------|----------------|
| Real Problem | Does this solve an actual pain point someone has? |
| Existing Users | Can I name 5 people who would use this? |
| Achievable | Can I build the core feature in Week 1? |
| Learnable | Does this project use full-stack + AI skills? |
| One Sentence | Can I explain the project in one sentence? |
| MVP Scope | Have I cut features to fit 4 weeks? |

### Scope Decision Table

| Build (MVP) | Skip (Full Product) |
|-------------|---------------------|
| Email + password auth | Social logins (Google, Facebook) |
| Basic text search | AI-powered semantic search |
| One AI feature | Multiple AI agents |
| Single server deploy | Kubernetes + load balancing |
| Simple admin CRUD | Role-based access + analytics |

---

## 2. Backend Setup Commands

### FastAPI Project Init

```bash
# Create project
mkdir my-capstone && cd my-capstone
poetry init --name my-capstone --python "^3.11"

# Core dependencies
poetry add fastapi uvicorn[standard] sqlalchemy[asyncio] asyncpg alembic
poetry add pydantic-settings python-dotenv

# Dev dependencies
poetry add --group dev pytest pytest-asyncio httpx black ruff mypy

# AI dependencies
poetry add openai langchain langchain-openai langchain-community chromadb

# Redis
poetry add redis

# Create folders
mkdir -p app/{models,schemas,api/v1,crud,services,core} tests alembic

# Init Alembic
poetry run alembic init alembic

# Run server
poetry run uvicorn app.main:app --reload --port 8000
```

### PostgreSQL Setup

```bash
sudo -u postgres psql
CREATE USER capstone_user WITH PASSWORD 'your_password';
CREATE DATABASE capstone_db OWNER capstone_user;
\q
```

### Database Connection String

```
postgresql+asyncpg://user:password@localhost:5432/database_name
```

### Essential .env Variables

```
DATABASE_URL=postgresql+asyncpg://capstone_user:password@localhost:5432/capstone_db
SECRET_KEY=your-random-secret-key
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-your-key-here
DEBUG=true
```

---

## 3. Frontend Integration Patterns

### HTMX Quick Reference

| Attribute | Purpose | Example |
|-----------|---------|---------|
| `hx-get` | GET request | `hx-get="/api/items"` |
| `hx-post` | POST request | `hx-post="/api/items"` |
| `hx-target` | Where to put response | `hx-target="#results"` |
| `hx-trigger` | Event trigger | `hx-trigger="click"` |
| `hx-swap` | How to insert HTML | `hx-swap="innerHTML"` |
| `hx-indicator` | Loading spinner | `hx-indicator="#loading"` |

### Vanilla JS Fetch Template

```javascript
const API_BASE = "http://localhost:8000/api/v1";

async function apiGet(endpoint) {
    const token = localStorage.getItem("token");
    const res = await fetch(`${API_BASE}${endpoint}`, {
        headers: { "Authorization": `Bearer ${token}` },
    });
    if (!res.ok) throw new Error(`API error: ${res.status}`);
    return res.json();
}

async function apiPost(endpoint, data) {
    const token = localStorage.getItem("token");
    const res = await fetch(`${API_BASE}${endpoint}`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    return res.json();
}
```

### Essential Tailwind Classes

| Purpose | Classes |
|---------|---------|
| Card | `bg-white rounded-lg shadow p-6` |
| Button | `bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700` |
| Input | `w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500` |
| Grid | `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6` |
| Center | `flex items-center justify-center` |

---

## 4. AI Feature Checklist

### RAG Pipeline Steps

```
1. Load documents  -->  TextLoader / PyPDFLoader
2. Split into chunks  -->  RecursiveCharacterTextSplitter(chunk_size=500)
3. Create embeddings  -->  OpenAIEmbeddings(model="text-embedding-3-small")
4. Store in vector DB  -->  Chroma.from_documents(chunks, embeddings)
5. User asks question  -->  Embed the question
6. Retrieve similar chunks  -->  vector_store.as_retriever(search_kwargs={"k": 3})
7. Build prompt  -->  System + Context + Question
8. Send to LLM  -->  ChatOpenAI(model="gpt-3.5-turbo")
9. Return answer  -->  With source references
```

### Prompt Template

```python
"""You are a helpful assistant for [your app].
Answer based ONLY on the provided context.
If the answer is not in the context, say "I do not have enough information."

Context: {context}
Question: {question}
Answer:"""
```

### AI Safety Checklist

| Check | Action |
|-------|--------|
| Rate limiting | Max 10 requests/min per user |
| Response caching | Cache in Redis (1-24 hours) |
| Error handling | try/except with fallback message |
| API key security | Backend only, never in frontend |
| Token limits | Use RAG, not full documents |

---

## 5. CI/CD Workflow Template

### Minimal GitHub Actions CI

```yaml
name: CI
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
          POSTGRES_DB: test_db
        ports: ["5432:5432"]
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install poetry && poetry install
      - run: poetry run ruff check app
      - run: poetry run pytest tests/ -v
        env:
          DATABASE_URL: postgresql+asyncpg://test_user:test_pass@localhost:5432/test_db
          SECRET_KEY: test-key
```

### Required GitHub Secrets

| Secret | Value |
|--------|-------|
| `OPENAI_API_KEY` | Your OpenAI key |
| `SERVER_HOST` | Server IP address |
| `SERVER_USER` | SSH username |
| `SSH_PRIVATE_KEY` | SSH private key |

---

## 6. Documentation Checklist

| Document | Must Have |
|----------|----------|
| README.md | Project description, screenshot, tech stack, setup steps |
| .env.example | Template with placeholder values |
| /docs endpoint | Swagger UI (automatic in FastAPI) |
| Architecture diagram | Mermaid or PNG showing system components |
| API endpoint table | Method, URL, description for key endpoints |
| Test instructions | How to run tests |
| LICENSE | MIT for capstone projects |

### README Sections (in order)

```
1. Project name + one-sentence description
2. Screenshot or demo GIF
3. Key features (bullet list)
4. Tech stack (table)
5. Architecture diagram
6. Getting started (step-by-step)
7. API documentation link
8. Running tests
9. Project structure
10. License
```

---

## 7. Demo Preparation Checklist

### Before the Demo

| Task | Done? |
|------|-------|
| App deployed to public URL | _ |
| Test data loaded in database | _ |
| Tested exact demo flow 3 times | _ |
| Browser tabs pre-opened (app, Swagger, GitHub) | _ |
| No personal bookmarks/history visible | _ |
| Phone on silent | _ |
| Backup internet (mobile hotspot) ready | _ |
| Demo script/outline written | _ |
| Backup screenshots ready | _ |

### 15-Minute Demo Structure

| Time | Section | Content |
|------|---------|---------|
| 0-2 min | Problem | Who has this problem? Why does it matter? |
| 2-5 min | Core Demo | Show main feature (happy path) |
| 5-7 min | AI Demo | Show AI feature working |
| 7-9 min | Admin Demo | Show management features |
| 9-12 min | Code | Project structure + key file + tests |
| 12-13 min | CI/CD | Show pipeline or deployment |
| 13-15 min | Wrap-up | Tech stack, learnings, Q&A |

### Q&A Preparation

| Likely Question | Prepare Answer About |
|----------------|---------------------|
| Why this tech stack? | Compare with alternatives |
| How does auth work? | JWT flow explanation |
| What was hardest? | Specific challenge + how you solved it |
| What would you add? | 2-3 realistic next features |
| How does the AI feature work? | RAG pipeline explanation |

---

*TechPath Institute — Full-Stack AI Product: Capstone Development*
