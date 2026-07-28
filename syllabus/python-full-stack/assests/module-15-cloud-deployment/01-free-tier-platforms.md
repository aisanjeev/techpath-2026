# Free-Tier Deployment Platforms

**Module 15 — Cloud Deployment | Topic 1**

---

## Deploy Your App in 10 Minutes

You have built a FastAPI application, Dockerized it, and set up CI/CD. Now you need to put it on the internet so anyone can access it.

The good news — several platforms let you deploy for free. No credit card, no complex setup. Perfect for learning, portfolios, and small projects.

> **Analogy:** Think of deployment platforms like moving from cooking at home to opening a food stall. You could rent an entire shop (VPS), or you could set up at a food court where the space, electricity, and furniture are already provided — you just bring your food (code).

---

## Platform Comparison

| Platform | Free Tier | Best For | Language Support |
|----------|-----------|----------|-----------------|
| **Render** | 750 hours/month, sleeps after 15 min | Python APIs, full-stack | Python, Node, Docker |
| **Railway** | $5 credit/month | Fast prototyping | Python, Node, Docker |
| **Fly.io** | 3 shared VMs, 3 GB storage | Edge deployment, Docker | Any (Docker) |
| **Vercel** | Unlimited (serverless) | Static sites, Next.js | Node, static |
| **Netlify** | 100 GB bandwidth | Static sites, JAMstack | Static, serverless |

---

## Render — The Easiest Start

Render is the most beginner-friendly platform for Python backends. It detects your project type and deploys automatically.

### How It Works

1. Connect your GitHub repository
2. Render detects Python/Docker
3. It builds and deploys automatically
4. You get a URL like `https://my-api.onrender.com`

### Deploying a FastAPI App

#### Step 1: Prepare Your Project

Your project needs a `requirements.txt` and a start command.

```
project/
├── app/
│   ├── __init__.py
│   └── main.py
├── requirements.txt
└── render.yaml          ← Optional (Infrastructure as Code)
```

**requirements.txt:**
```
fastapi==0.115.0
uvicorn[standard]==0.30.0
sqlalchemy==2.0.35
```

#### Step 2: Create a Render Account

1. Go to render.com
2. Sign up with GitHub (recommended — enables auto-deploy)

#### Step 3: Create a New Web Service

1. Click **New** → **Web Service**
2. Connect your GitHub repo
3. Configure:

| Setting | Value |
|---------|-------|
| Name | `my-fastapi-api` |
| Region | Singapore (closest to India) |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Plan | Free |

4. Click **Create Web Service**

#### Step 4: Add Environment Variables

In the Render dashboard → Environment:

```
DATABASE_URL=sqlite+aiosqlite:///./data/app.db
SECRET_KEY=your-production-secret
```

### Render Auto-Deploy

When you push to your connected branch, Render automatically:
1. Pulls the latest code
2. Runs the build command
3. Restarts the service

### Free Tier Limitations

| Limitation | Detail |
|------------|--------|
| Sleep after inactivity | Service sleeps after 15 minutes of no requests |
| Cold start | First request after sleep takes 30-60 seconds |
| Monthly hours | 750 hours (enough for 1 always-on service) |
| No persistent disk | Data is lost on redeploy (use external DB) |
| Bandwidth | 100 GB/month |

### render.yaml (Infrastructure as Code)

```yaml
# render.yaml
services:
  - type: web
    name: techpath-api
    runtime: python
    region: singapore
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: DATABASE_URL
        value: sqlite+aiosqlite:///./data/app.db
      - key: SECRET_KEY
        generateValue: true        # Auto-generate a random value
```

---

## Railway — Fast Prototyping

Railway is like Render but with a simpler interface and a small free credit.

### Deploying to Railway

#### Step 1: Create Account

1. Go to railway.app
2. Sign up with GitHub

#### Step 2: New Project

1. Click **New Project** → **Deploy from GitHub repo**
2. Select your repository
3. Railway auto-detects Python and deploys

#### Step 3: Configure

Railway usually detects everything automatically. If not, add a `Procfile`:

```
# Procfile
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Or a `railway.toml`:

```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
```

### Railway Free Tier

| Feature | Limit |
|---------|-------|
| Monthly credit | $5 (enough for a small app running 24/7) |
| Execution hours | ~500 hours/month |
| Memory | 512 MB |
| Storage | 1 GB |

### Railway Advantages

- Built-in PostgreSQL database (one-click add)
- Built-in Redis (one-click add)
- No cold starts on free tier
- Environment variable management in UI

---

## Fly.io — Docker-Based Edge Deployment

Fly.io runs Docker containers on servers around the world (edge deployment). Your app runs close to your users.

### Deploying to Fly.io

#### Step 1: Install flyctl CLI

```bash
# Windows (PowerShell)
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

#### Step 2: Login and Launch

```bash
# Login
fly auth login

# Initialize (creates fly.toml)
fly launch

# It asks:
# App name: techpath-api
# Region: maa (Chennai — closest to India)
# Database: Yes/No
```

#### Step 3: Deploy

```bash
fly deploy
```

Fly.io builds your Docker image and deploys it.

### fly.toml Configuration

```toml
# fly.toml
app = "techpath-api"
primary_region = "maa"    # Chennai, India

[build]
  dockerfile = "Dockerfile"

[env]
  APP_ENV = "production"
  PORT = "8000"

[http_service]
  internal_port = 8000
  force_https = true
  auto_start_machines = true
  auto_stop_machines = true
  min_machines_running = 0

[[vm]]
  size = "shared-cpu-1x"
  memory = "256mb"
```

### Fly.io Free Tier

| Feature | Limit |
|---------|-------|
| Shared VMs | 3 free |
| Memory | 256 MB per VM |
| Storage | 3 GB total |
| Bandwidth | 160 GB/month |
| Regions | Deploy anywhere |

---

## Which Platform Should You Choose?

| Scenario | Best Platform |
|----------|--------------|
| First deployment ever | **Render** (easiest) |
| Need a database included | **Railway** (one-click PostgreSQL) |
| Docker-based deployment | **Fly.io** (Docker native) |
| Static frontend | **Vercel** or **Netlify** |
| Portfolio project | **Render** (free, auto-deploy) |
| Production app (small scale) | **Railway** or **Fly.io** |
| Learning cloud deployment | Start with **Render**, then try **Fly.io** |

---

## Important: Free Tier Limitations

All free tiers have limitations. For production apps, you will eventually need paid plans or a VPS.

| Limitation | Impact | Solution |
|------------|--------|----------|
| Cold starts | First request is slow | Use a paid plan or health check pinger |
| No persistent storage | Data lost on redeploy | Use external database (Supabase, Neon) |
| Limited resources | Slow under load | Scale up or use a VPS |
| Shared infrastructure | Noisy neighbors | Use dedicated resources |

---

## Practice Exercise

1. Deploy your FastAPI app to Render (free tier)
2. Test the deployed URL with curl or your browser
3. Push a code change and watch auto-deploy
4. Compare cold start time vs warm request time
5. Try deploying the same app to Railway or Fly.io

---

*Next Topic: Cloud Databases — Supabase and Neon serverless PostgreSQL.*
