# Cheat Sheet: Spec-Kit & Deployment

**Module 15 — Quick Reference**

---

## Spec-Kit Checklist

- [ ] README.md with screenshots
- [ ] Tech spec (architecture + stack)
- [ ] .env.example (no real secrets)
- [ ] .gitignore (hide sensitive files)
- [ ] Setup instructions (step by step)
- [ ] Folder structure map
- [ ] Live demo link

---

## Free Hosting

| Platform | For | Deploy |
|----------|-----|--------|
| Vercel | Frontend | Git push |
| Netlify | Static sites | Git/drag-drop |
| Render | Backend/API | Git push |
| Railway | Full-stack | Git push |
| GitHub Pages | HTML sites | gh-pages branch |

---

## Docker Commands

```bash
docker build -t myapp .       # Build image
docker run -p 8000:8000 myapp  # Run container
docker ps                      # List running
docker stop <id>               # Stop container
docker-compose up              # Start all services
docker-compose down            # Stop all services
```

---

## Dockerfile Template

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## .gitignore Essentials

```
.env
.env.local
node_modules/
__pycache__/
*.db
.venv/
dist/
```

---

## DNS Records

| Record | Maps To |
|--------|---------|
| A | IP address |
| CNAME | Another domain |
| MX | Mail server |

---

## GitHub Actions Template

```yaml
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: pytest
```
