# Deployment & DevOps Basics

**Module 15 — Spec-Kit Development | Topic 2**

---

## What is Deployment?

**Deployment** = making your project live on the internet so anyone can access it.

```
Your Computer (localhost) → Deploy → Live URL (https://myapp.com)
```

| Term | Meaning |
|------|---------|
| **Localhost** | Your project running on your own computer |
| **Production** | The live version users access |
| **Staging** | A test version before going live |
| **Deploy** | Uploading your code to a server |

---

## Free Hosting Platforms

### Frontend / Static Sites

| Platform | Best For | Deploy Method |
|----------|----------|---------------|
| **Vercel** | React, Next.js, Astro | Git push → auto deploy |
| **Netlify** | Static sites, HTML/CSS | Git push or drag-drop |
| **GitHub Pages** | Simple HTML sites | Push to gh-pages branch |
| **Cloudflare Pages** | Fast global CDN | Git push |

### Backend / Full-Stack

| Platform | Best For | Free Tier |
|----------|----------|-----------|
| **Render** | FastAPI, Django, Node.js | Free (sleeps after 15 min) |
| **Railway** | Any backend + database | $5 free credit |
| **Fly.io** | Docker apps | Free (3 machines) |
| **PythonAnywhere** | Python/Django | Free (limited) |

---

## Deploy to Vercel (Frontend)

```bash
# Step 1: Install Vercel CLI
npm install -g vercel

# Step 2: Login
vercel login

# Step 3: Deploy
vercel

# Or just connect your GitHub repo on vercel.com
# Every push to main = auto deploy
```

### Vercel Settings

| Setting | Value |
|---------|-------|
| Framework | Auto-detected |
| Build Command | `npm run build` |
| Output Directory | `dist` or `.next` |
| Environment Variables | Add in dashboard |

---

## Deploy to Render (Backend)

1. Go to render.com → New Web Service
2. Connect your GitHub repo
3. Settings:

| Setting | Value |
|---------|-------|
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Environment Variables | Add DATABASE_URL, SECRET_KEY |

4. Click Deploy — your API is live!

---

## Docker Basics

**Docker** = a way to package your entire app (code + dependencies + settings) into a container that runs the same everywhere.

### Why Docker?

| Problem | Docker Solution |
|---------|----------------|
| "Works on my machine" | Same container everywhere |
| Different Python versions | Container has exact version |
| Complex setup steps | One command to start |
| Conflicts between projects | Each project isolated |

### Key Concepts

| Term | Meaning |
|------|---------|
| **Image** | Blueprint/recipe for your app |
| **Container** | Running instance of an image |
| **Dockerfile** | Instructions to build an image |
| **Docker Compose** | Run multiple containers together |
| **Docker Hub** | Store/share images (like GitHub for images) |

### Dockerfile Example

```dockerfile
# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy rest of code
COPY . .

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Commands

```bash
# Build image
docker build -t myapp .

# Run container
docker run -p 8000:8000 myapp

# List running containers
docker ps

# Stop container
docker stop <container-id>
```

### Docker Compose (Multiple Services)

```yaml
# docker-compose.yml
version: "3.8"
services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
```

```bash
# Start everything
docker-compose up

# Stop everything
docker-compose down
```

---

## CI/CD with GitHub Actions

**CI/CD** = Continuous Integration / Continuous Deployment — automate testing and deployment.

```
Push Code → GitHub Actions runs → Tests pass → Auto deploy
```

### Simple GitHub Action

Create `.github/workflows/deploy.yml`:

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

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest

      - name: Deploy to Render
        run: curl ${{ secrets.RENDER_DEPLOY_HOOK }}
```

---

## Domain, Hosting & SSL

### Custom Domain

| Step | Action |
|------|--------|
| 1 | Buy domain (GoDaddy, Namecheap, Hostinger) |
| 2 | Point DNS to your hosting (A record or CNAME) |
| 3 | Add domain in hosting dashboard |
| 4 | Wait for DNS to propagate (up to 48 hours) |

### DNS Records

| Record | Purpose | Example |
|--------|---------|---------|
| **A** | Points to IP address | `@ → 76.76.21.21` |
| **CNAME** | Points to another domain | `www → myapp.vercel.app` |
| **MX** | Email routing | `@ → mail.google.com` |

### SSL Certificate (HTTPS)

- **SSL** = Secure Sockets Layer — encrypts data between browser and server
- **HTTPS** = HTTP + SSL — the padlock icon in browser
- Most free hosts (Vercel, Netlify, Render) give **free SSL automatically**
- For VPS: use **Let's Encrypt** (free) with `certbot`

---

## Cloud Services Overview

| Service | AWS | Azure | GCP |
|---------|-----|-------|-----|
| **Compute (VMs)** | EC2 | Virtual Machines | Compute Engine |
| **Storage** | S3 | Blob Storage | Cloud Storage |
| **Database** | RDS | Azure SQL | Cloud SQL |
| **Serverless** | Lambda | Functions | Cloud Functions |
| **Deploy Apps** | Elastic Beanstalk | App Service | App Engine |

> At this level, you just need to **know what these services do** — not master them.

---

## Summary

- **Deployment** = making your project live on the internet
- **Vercel/Netlify** = best for frontend (free, auto-deploy from Git)
- **Render/Railway** = best for backend (free tier available)
- **Docker** = package app + dependencies into portable container
- **Dockerfile** = recipe to build your container
- **CI/CD** = auto-test and deploy when you push code
- **GitHub Actions** = free CI/CD for GitHub repos
- **SSL** = HTTPS encryption — free on most platforms
- **Custom domain** = buy + point DNS to your hosting
