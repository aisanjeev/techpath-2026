# Static Frontend Deployment

**Module 15 — Cloud Deployment | Topic 3**

---

## Frontend Deployment Options

Your frontend (Astro, React, Next.js) needs to be deployed separately from the backend. Frontend hosting is easier and often completely free.

| Platform | Free Tier | Best For |
|----------|-----------|----------|
| **Vercel** | Unlimited sites, 100 GB bandwidth | Next.js, Astro, React |
| **Netlify** | 100 GB bandwidth, 300 min builds | Static sites, JAMstack |
| **GitHub Pages** | 1 GB storage, 100 GB bandwidth | Static HTML, docs |
| **Cloudflare Pages** | Unlimited bandwidth | Performance-critical sites |

---

## Vercel — The Default Choice for Modern Frontends

Vercel is created by the team behind Next.js. It provides the best experience for deploying JavaScript frontends.

### Deploying to Vercel

#### Step 1: Sign Up

1. Go to vercel.com
2. Sign up with GitHub

#### Step 2: Import Project

1. Click **Add New** → **Project**
2. Import your GitHub repository
3. Vercel auto-detects the framework (Astro, Next.js, React)

#### Step 3: Configure

| Setting | Value |
|---------|-------|
| Framework | Auto-detected (Astro, Next.js, etc.) |
| Root Directory | `./` (or `./frontend` for monorepos) |
| Build Command | Auto-detected (`npm run build`) |
| Output Directory | Auto-detected |

#### Step 4: Environment Variables

Add your frontend environment variables:

```
PUBLIC_API_URL=https://api.techpath.biz
SITE_URL=https://techpath.biz
PUBLIC_SITE_ENV=production
```

#### Step 5: Deploy

Click **Deploy**. Vercel:
1. Clones your repo
2. Installs dependencies (`npm install`)
3. Runs the build command
4. Deploys to its global CDN
5. Gives you a URL: `https://your-app.vercel.app`

### Auto-Deploy on Push

Once connected, Vercel automatically redeploys when you push to the connected branch:

| Branch | Deployment |
|--------|-----------|
| `main` | Production (your-app.vercel.app) |
| Any other branch | Preview deployment (unique URL) |
| Pull Request | Preview with comment on PR |

### Preview Deployments

Every PR gets a unique preview URL. This is incredibly useful for code reviews:

```
PR #42: "Add user registration page"
Preview: https://your-app-pr-42.vercel.app
```

Reviewers can click the link to test the changes without running anything locally.

### Vercel Free Tier

| Feature | Limit |
|---------|-------|
| Deployments | Unlimited |
| Bandwidth | 100 GB/month |
| Build time | 6000 min/month |
| Serverless functions | 100 GB-hours |
| Team members | 1 (personal hobby plan) |

---

## Netlify — The JAMstack Pioneer

Netlify is another excellent choice, especially for static sites and sites with serverless functions.

### Deploying to Netlify

#### Step 1: Sign Up and Import

1. Go to netlify.com
2. Sign up with GitHub
3. Click **Add new site** → **Import an existing project**
4. Select your GitHub repo

#### Step 2: Configure

| Setting | Value |
|---------|-------|
| Build command | `npm run build` |
| Publish directory | `dist` (Astro) or `out` (Next.js static) or `.next` |
| Branch | `main` |

#### Step 3: Environment Variables

Add in Site settings → Environment variables:

```
PUBLIC_API_URL=https://api.techpath.biz
```

### Netlify Features

| Feature | Description |
|---------|-------------|
| Forms | Built-in form handling (no backend needed) |
| Functions | Serverless functions (AWS Lambda) |
| Identity | Built-in authentication |
| Split testing | A/B test different branches |
| Analytics | Server-side analytics |

---

## Custom Domains

### Why Custom Domains?

Default URLs like `your-app.vercel.app` work but look unprofessional. A custom domain like `techpath.biz` builds credibility.

### Getting a Domain

Popular domain registrars for Indian developers:

| Registrar | .com Price | .in Price |
|-----------|-----------|-----------|
| Namecheap | ~₹800/year | ~₹400/year |
| GoDaddy | ~₹900/year | ~₹500/year |
| Google Domains | ~₹1000/year | ~₹500/year |
| Cloudflare | ~₹750/year (at cost) | ~₹350/year |

### Setting Up a Custom Domain on Vercel

#### Step 1: Add Domain in Vercel

1. Project → Settings → Domains
2. Enter your domain: `techpath.biz`
3. Click **Add**

#### Step 2: Configure DNS

Vercel tells you to add DNS records. Go to your domain registrar and add:

| Type | Name | Value |
|------|------|-------|
| A | @ | 76.76.21.21 |
| CNAME | www | cname.vercel-dns.com |

#### Step 3: Wait for Propagation

DNS changes take 5 minutes to 48 hours to propagate. Usually it is under 30 minutes.

#### Step 4: SSL Certificate

Vercel automatically provisions a free SSL certificate (HTTPS) for your domain. No configuration needed.

### Setting Up on Netlify

Similar process:

1. Site settings → Domain management → Add custom domain
2. Add DNS records as instructed
3. SSL is automatic via Let's Encrypt

---

## SSL/HTTPS

**SSL (HTTPS) is mandatory** for modern websites. It encrypts data between the browser and server.

### Why HTTPS Matters

| Without HTTPS | With HTTPS |
|---------------|------------|
| Browser shows "Not Secure" warning | Green padlock icon |
| Data sent in plain text (hackable) | Data encrypted |
| Lower Google search ranking | Higher search ranking |
| Cannot use modern APIs (webcam, location) | Full API access |

### Free SSL Options

| Service | How |
|---------|-----|
| Vercel | Automatic, zero config |
| Netlify | Automatic via Let's Encrypt |
| Cloudflare | Free plan includes SSL |
| Let's Encrypt | Free certificates (manual renewal) |
| Certbot | Auto-renewal tool for Let's Encrypt |

---

## Monorepo Deployment

If your frontend and backend are in the same repository (monorepo), you need to configure the root directory.

### Vercel — Monorepo Setup

```
my-project/
├── frontend/          ← Deploy this to Vercel
├── backend/           ← Deploy this to Render/VPS
├── admin/             ← Deploy this to Vercel (separate project)
└── README.md
```

In Vercel project settings:
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`

### Ignoring Builds for Irrelevant Changes

Create a script to skip builds when only backend code changes:

```bash
# frontend/vercel-ignore-step.sh
#!/bin/bash

# Only build if frontend files changed
git diff HEAD^ HEAD --quiet -- frontend/
```

In Vercel: Settings → Git → Ignored Build Step → `bash vercel-ignore-step.sh`

---

## Comparing Deployment Approaches

| Approach | Complexity | Cost | Performance |
|----------|-----------|------|-------------|
| Vercel/Netlify | Very easy | Free | Excellent (global CDN) |
| VPS (Nginx) | Medium | ₹400-1000/month | Good |
| S3 + CloudFront | Medium | Pay per use | Excellent |
| GitHub Pages | Easy | Free | Good |

### For Students

Start with **Vercel** for frontends. It is free, fast, and provides the best developer experience. Move to VPS-based hosting when you need more control.

---

## Practice Exercise

1. Deploy your Astro/React frontend to Vercel
2. Test the auto-deploy by pushing a change
3. Open a PR and check the preview deployment
4. (Optional) Buy a cheap domain (.in or .xyz) and add it to Vercel
5. Verify HTTPS is working

---

*Next Topic: Azure Core Concepts — App Service, Container Apps, and Azure DB.*
