# Module 13 — Assignment: Docker & Containerization

**Deadline:** End of Week 22
**Submission:** Dockerfile, docker-compose.yml, screenshots of running containers + Docker Hub link

---

## Containerize and Deploy a Full-Stack Python Application

### Task 1: Dockerize a FastAPI App — 25 marks

Create a Dockerfile for a FastAPI Student Management API:

**Requirements:**
- Use `python:3.12-slim` as base image
- Set proper environment variables (`PYTHONDONTWRITEBYTECODE`, `PYTHONUNBUFFERED`)
- Copy and install requirements first (layer caching)
- Expose port 8000
- Use `uvicorn` CMD to start the server

**Verify:**
```bash
docker build -t student-api .
docker run -d -p 8000:8000 --name my-api student-api
# Open http://localhost:8000/docs — Swagger UI should load
```

**Submit:** Dockerfile + screenshot of Swagger UI running in Docker container

---

### Task 2: Multi-Service App with Docker Compose — 30 marks

Create a `docker-compose.yml` that runs:

| Service | Image/Build | Port | Purpose |
|---------|-------------|------|---------|
| `web` | Build from Dockerfile | 8000 | FastAPI application |
| `db` | `postgres:16` | 5432 | PostgreSQL database |
| `cache` | `redis:7-alpine` | 6379 | Redis caching |

**Requirements:**
- Web service connects to PostgreSQL (use environment variables)
- Use named volumes for database persistence
- Use `depends_on` with health checks
- Web service has a health check endpoint
- Use a custom network for all services

**Verify:**
```bash
docker compose up -d
docker compose ps          # All services should be "running"
docker compose logs web    # No errors
# http://localhost:8000/docs should work with database connected
```

**Submit:** docker-compose.yml + screenshot of `docker compose ps` output

---

### Task 3: Optimize the Docker Image — 20 marks

Optimize your Dockerfile from Task 1:

| Optimization | What to Do |
|-------------|------------|
| Multi-stage build | Separate builder and runtime stages |
| .dockerignore | Exclude `.git`, `__pycache__`, `.env`, `tests/`, `*.md` |
| Non-root user | Create and switch to a non-root user |
| Slim base | Use `python:3.12-slim` (not full image) |

**Compare sizes:**
```bash
docker images | grep student-api
# Show before and after image sizes
```

**Submit:** Optimized Dockerfile + .dockerignore + screenshot showing image size reduction

---

### Task 4: Push to Docker Hub — 25 marks

Push your optimized image to Docker Hub:

1. Create a Docker Hub account (free) at https://hub.docker.com/
2. Login: `docker login`
3. Tag: `docker tag student-api YOUR_USERNAME/student-api:v1.0`
4. Push: `docker push YOUR_USERNAME/student-api:v1.0`
5. Verify: Visit `https://hub.docker.com/r/YOUR_USERNAME/student-api`

**Also tag as latest:**
```bash
docker tag student-api YOUR_USERNAME/student-api:latest
docker push YOUR_USERNAME/student-api:latest
```

**Submit:** Docker Hub URL + screenshot of the repository page showing your pushed image

---

## Project Structure

```
student-api/
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── app/
    ├── __init__.py
    ├── main.py
    ├── models.py
    ├── database.py
    └── routes/
        └── students.py
```

---

## Rubric

| Criteria | Excellent (Full) | Good (75%) | Needs Work (50%) |
|----------|-----------------|------------|------------------|
| Dockerfile | Correct, builds and runs, proper layering | Builds but issues with CMD or EXPOSE | Syntax errors, won't build |
| Docker Compose | All 3 services run, health checks, volumes | Services run but missing health checks | Only web service works |
| Optimization | Multi-stage + .dockerignore + non-root user | Some optimizations applied | No optimization |
| Docker Hub | Image pushed, proper tags, public repo | Image pushed but wrong tags | Not pushed |
