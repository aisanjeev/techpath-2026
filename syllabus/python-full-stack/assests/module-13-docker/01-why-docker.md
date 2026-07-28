# Why Docker? — Containers, Images & Layers

**Module 13 — Docker & Containerization | Topic 1**

---

## The Problem Docker Solves

Imagine Rahul builds a FastAPI app on his laptop. Everything works perfectly. He sends the code to his teammate Priya, and she gets errors — wrong Python version, missing libraries, different OS settings.

This is the classic **"It works on my machine"** problem.

**Docker solves this by packaging your app along with everything it needs** — Python version, libraries, OS dependencies, config files — into a single portable unit called a **container**.

> **Analogy:** Think of a container like a tiffin box. No matter which office canteen you take it to, your food (app) stays exactly the same inside. The tiffin (container) carries everything your meal needs.

---

## Containers vs Virtual Machines (VMs)

Both containers and VMs let you run isolated applications, but they work very differently.

### Virtual Machine

A VM is like renting an entire apartment. You get your own kitchen, bathroom, bedroom — even if you only need a small room. Each VM runs a **full operating system** on top of a hypervisor.

### Container

A container is like renting a room in a co-living space. You get your own private room (isolated app), but share the building's plumbing and electricity (OS kernel). Containers share the host OS kernel, making them much lighter.

| Feature | Virtual Machine | Container |
|---------|----------------|-----------|
| Size | 1-20 GB | 50-500 MB |
| Startup time | Minutes | Seconds |
| OS | Full OS per VM | Shares host OS kernel |
| Isolation | Complete (hardware-level) | Process-level |
| Resource usage | Heavy | Lightweight |
| Example | VMware, VirtualBox | Docker, Podman |
| Use case | Running Windows on a Mac | Running microservices |

### When to Use What

| Scenario | Best Choice |
|----------|-------------|
| Running a different OS (e.g., Linux on Windows) | VM |
| Running 10 microservices on one server | Containers |
| Testing your app in a clean environment | Container |
| Complete security isolation for sensitive workloads | VM |

---

## What Is a Docker Image?

A **Docker image** is a read-only template that contains everything needed to run an application:
- Base operating system (like Ubuntu or Alpine Linux)
- Programming language runtime (Python 3.12)
- Your application code
- All dependencies (pip packages)
- Configuration files

> **Analogy:** An image is like a recipe card. You can create as many dishes (containers) as you want from the same recipe (image). The recipe itself never changes.

### Image vs Container

| Concept | Image | Container |
|---------|-------|-----------|
| What is it? | A template/blueprint | A running instance |
| State | Read-only | Read-write |
| Analogy | Recipe | The cooked dish |
| Created by | `docker build` | `docker run` |
| Can there be many? | One image → many containers | Each container is independent |

```
Image (read-only blueprint)
    ├── Container 1 (running instance)
    ├── Container 2 (another instance)
    └── Container 3 (yet another)
```

---

## Understanding Layers

Docker images are built in **layers**. Each instruction in a Dockerfile creates a new layer on top of the previous one. Layers are cached — if nothing changes in a layer, Docker reuses it instead of rebuilding.

### How Layers Work

```
Layer 5: CMD ["uvicorn", "main:app"]      ← Your start command
Layer 4: COPY . /app                       ← Your code
Layer 3: RUN pip install -r requirements   ← Dependencies
Layer 2: RUN apt-get install -y curl       ← System packages
Layer 1: python:3.12-slim                  ← Base image
```

Each layer is like a transparent sheet. Stack them all together, and you get the complete image.

### Why Layers Matter

1. **Caching**: If you only change your code (Layer 4), Docker reuses Layers 1-3 from cache. This makes builds fast.
2. **Sharing**: If two images use the same base `python:3.12-slim`, that layer is stored only once on disk.
3. **Size**: Each layer adds to the total image size. Fewer and smaller layers = smaller images.

**Example — How caching saves time:**

```
First build:  Layer 1 (download python:3.12-slim) — 2 min
              Layer 2 (install curl) — 30 sec
              Layer 3 (pip install) — 1 min
              Layer 4 (copy code) — 1 sec
              Total: ~3.5 min

Second build (only code changed):
              Layer 1 — CACHED
              Layer 2 — CACHED
              Layer 3 — CACHED
              Layer 4 (copy code) — 1 sec
              Total: ~1 sec
```

---

## Docker Hub — The Image Marketplace

**Docker Hub** (hub.docker.com) is the default public registry for Docker images. Think of it as the "npm" or "PyPI" for containers.

### Official Images

These are maintained by Docker or the software creators:

| Image | What It Is | Size |
|-------|-----------|------|
| `python:3.12` | Full Python with Debian | ~900 MB |
| `python:3.12-slim` | Smaller Python with minimal Debian | ~150 MB |
| `python:3.12-alpine` | Tiny Python with Alpine Linux | ~50 MB |
| `node:20` | Node.js runtime | ~1 GB |
| `postgres:16` | PostgreSQL database | ~400 MB |
| `redis:7` | Redis cache | ~130 MB |
| `nginx:latest` | Nginx web server | ~140 MB |

### Image Naming Convention

```
registry/username/image:tag

Examples:
  python:3.12-slim          ← Official image, specific tag
  python:latest             ← Official image, latest tag (avoid in production)
  rahul2024/my-fastapi:v1.0 ← Custom image by user "rahul2024"
  ghcr.io/priya/app:main    ← Image on GitHub Container Registry
```

### Pulling an Image

```bash
# Pull an image from Docker Hub
docker pull python:3.12-slim

# List all images on your machine
docker images
```

---

## Installing Docker

### Windows

1. Download **Docker Desktop** from docker.com
2. Run the installer
3. Enable **WSL 2** when prompted (Windows Subsystem for Linux)
4. Restart your computer
5. Open terminal and verify:

```bash
docker --version
# Docker version 27.x.x

docker run hello-world
# Should print "Hello from Docker!"
```

### Linux (Ubuntu)

```bash
# Install Docker
sudo apt update
sudo apt install docker.io -y

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to the docker group (so you don't need sudo)
sudo usermod -aG docker $USER

# Log out and back in, then verify
docker --version
docker run hello-world
```

### Mac

1. Download Docker Desktop for Mac from docker.com
2. Drag to Applications folder
3. Open Docker Desktop
4. Verify in terminal: `docker --version`

---

## Your First Container

Let us run a Python container interactively:

```bash
# Run a Python container and open a shell
docker run -it python:3.12-slim python

# You are now inside the container!
>>> print("Hello from Docker!")
Hello from Docker!
>>> import sys
>>> print(sys.version)
3.12.4 (main, Jun 7 2024, 00:00:00)
>>> exit()
```

**What happened:**
1. Docker checked if `python:3.12-slim` exists locally
2. If not, it downloaded (pulled) the image from Docker Hub
3. Created a new container from that image
4. Started the Python interpreter inside the container
5. When you typed `exit()`, the container stopped

---

## Key Docker Concepts — Summary

| Concept | What It Is | Real-World Analogy |
|---------|-----------|-------------------|
| **Image** | Read-only template with OS + code + deps | Recipe card |
| **Container** | Running instance of an image | The cooked dish |
| **Dockerfile** | Instructions to build an image | Recipe steps |
| **Layer** | One step/instruction in an image | One page of the recipe |
| **Registry** | Storage for images (Docker Hub, GHCR) | Recipe book library |
| **Volume** | Persistent storage for container data | External hard drive |
| **Network** | Communication channel between containers | Phone line between offices |

---

## Practice Exercise

1. Install Docker on your machine
2. Run `docker run hello-world` and read the output carefully
3. Pull `python:3.12-slim` and start a Python shell inside it
4. Run `docker images` to see what images are on your machine
5. Run `docker ps -a` to see stopped containers

---

*Next Topic: Writing Dockerfiles — building your own images for FastAPI and Django apps.*
