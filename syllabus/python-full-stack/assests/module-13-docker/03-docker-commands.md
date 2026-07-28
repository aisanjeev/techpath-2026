# Docker Commands — The Complete Reference

**Module 13 — Docker & Containerization | Topic 3**

---

## Docker Command Structure

All Docker commands follow this pattern:

```
docker <command> [options] [arguments]
```

> **Tip:** You can always add `--help` to any command to see all options:
> ```bash
> docker run --help
> docker build --help
> ```

---

## Image Commands

### Pulling Images

```bash
# Pull an image from Docker Hub
docker pull python:3.12-slim

# Pull a specific version
docker pull postgres:16

# Pull from GitHub Container Registry
docker pull ghcr.io/username/app:latest
```

### Listing Images

```bash
# List all images on your machine
docker images

# Example output:
# REPOSITORY          TAG           IMAGE ID       SIZE
# python              3.12-slim     a1b2c3d4e5f6   150MB
# my-fastapi-app      v1.0          b2c3d4e5f6a7   200MB
# postgres            16            c3d4e5f6a7b8   400MB
```

### Removing Images

```bash
# Remove a specific image
docker rmi python:3.12-slim

# Remove by image ID
docker rmi a1b2c3d4e5f6

# Remove all unused images (dangling images)
docker image prune

# Remove ALL unused images (not just dangling)
docker image prune -a
```

### Building Images

```bash
# Build from current directory
docker build -t my-app .

# Build with a tag
docker build -t my-app:v2.0 .

# Build from a specific Dockerfile
docker build -f Dockerfile.prod -t my-app:prod .

# Build without cache (fresh build)
docker build --no-cache -t my-app .
```

---

## Container Commands

### Running Containers

```bash
# Run a container (foreground)
docker run my-app

# Run in the background (detached)
docker run -d my-app

# Run with a name
docker run -d --name api-server my-app

# Run with port mapping
docker run -d -p 8000:8000 my-app

# Run with environment variables
docker run -d -e DATABASE_URL=sqlite:///app.db -e DEBUG=true my-app

# Run with an env file
docker run -d --env-file .env my-app

# Run interactively (with terminal access)
docker run -it python:3.12-slim bash

# Run and remove container when it stops
docker run --rm my-app
```

**Common flags explained:**

| Flag | Full Form | Meaning |
|------|-----------|---------|
| `-d` | `--detach` | Run in background |
| `-p` | `--publish` | Map port (host:container) |
| `-e` | `--env` | Set environment variable |
| `-it` | `--interactive --tty` | Interactive terminal |
| `--rm` | | Auto-remove when stopped |
| `--name` | | Give the container a name |
| `-v` | `--volume` | Mount a volume |
| `--network` | | Connect to a network |

### Listing Containers

```bash
# List running containers
docker ps

# Example output:
# CONTAINER ID   IMAGE          STATUS          PORTS                    NAMES
# a1b2c3d4e5f6   my-app:v1.0    Up 5 minutes    0.0.0.0:8000->8000/tcp   api-server

# List ALL containers (including stopped)
docker ps -a

# List only container IDs
docker ps -q
```

### Stopping and Starting

```bash
# Stop a running container (graceful shutdown)
docker stop api-server

# Stop by container ID
docker stop a1b2c3d4e5f6

# Start a stopped container
docker start api-server

# Restart a container
docker restart api-server

# Force kill (when stop doesn't work)
docker kill api-server
```

### Removing Containers

```bash
# Remove a stopped container
docker rm api-server

# Force remove a running container
docker rm -f api-server

# Remove all stopped containers
docker container prune

# Remove all stopped containers (alternative)
docker rm $(docker ps -aq)
```

---

## Inspecting Containers

### Viewing Logs

```bash
# See all logs
docker logs api-server

# Follow logs in real-time (like tail -f)
docker logs -f api-server

# Show last 50 lines
docker logs --tail 50 api-server

# Show logs with timestamps
docker logs -t api-server

# Combine: last 20 lines + follow
docker logs --tail 20 -f api-server
```

### Executing Commands Inside a Running Container

```bash
# Open a bash shell inside a running container
docker exec -it api-server bash

# Run a single command
docker exec api-server python -c "print('Hello!')"

# Check what's inside the container
docker exec api-server ls /app

# Check environment variables
docker exec api-server env

# Run a Python script
docker exec api-server python manage.py migrate
```

> **Analogy:** `docker exec` is like SSH-ing into a server. You are running commands inside the container while it keeps running.

### Inspecting Container Details

```bash
# See full container details (JSON)
docker inspect api-server

# See only the IP address
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' api-server

# See port mappings
docker port api-server

# See resource usage (CPU, memory)
docker stats

# See resource usage for one container
docker stats api-server
```

---

## Volume Commands — Persistent Storage

Containers are **ephemeral** — when you remove a container, all data inside it is lost. Volumes let you persist data.

> **Analogy:** A container is like a rental car. When you return it, everything inside is gone. A volume is like your own trunk — you carry it between cars.

### Creating and Using Volumes

```bash
# Create a named volume
docker volume create app-data

# List all volumes
docker volume ls

# Run a container with a volume
docker run -d \
  -v app-data:/app/data \
  --name api-server \
  my-app

# Mount a host directory (bind mount)
docker run -d \
  -v $(pwd)/data:/app/data \
  --name api-server \
  my-app

# Read-only mount
docker run -d \
  -v $(pwd)/config.yaml:/app/config.yaml:ro \
  my-app
```

**Volume types:**

| Type | Syntax | Use Case |
|------|--------|----------|
| Named volume | `-v mydata:/app/data` | Database storage, persistent data |
| Bind mount | `-v /host/path:/container/path` | Development (live code reload) |
| Read-only | `-v /path:/path:ro` | Config files that shouldn't change |

### Managing Volumes

```bash
# Inspect a volume
docker volume inspect app-data

# Remove a volume
docker volume rm app-data

# Remove all unused volumes
docker volume prune
```

---

## Network Commands

Docker networks let containers communicate with each other.

### Creating and Using Networks

```bash
# Create a network
docker network create app-network

# List networks
docker network ls

# Run containers on the same network
docker run -d --name db --network app-network postgres:16
docker run -d --name api --network app-network -p 8000:8000 my-app

# Now the API container can reach the DB using hostname "db"
# DATABASE_URL=postgresql://user:pass@db:5432/mydb
```

> **Key insight:** On the same Docker network, containers can reach each other using their container **name** as the hostname. So the API connects to `db:5432`, not `localhost:5432`.

### Managing Networks

```bash
# Inspect a network
docker network inspect app-network

# Connect a running container to a network
docker network connect app-network api-server

# Disconnect from a network
docker network disconnect app-network api-server

# Remove a network
docker network rm app-network

# Remove all unused networks
docker network prune
```

---

## Cleanup Commands

Over time, Docker can use a lot of disk space. These commands help clean up.

```bash
# Remove all stopped containers
docker container prune

# Remove all unused images
docker image prune -a

# Remove all unused volumes
docker volume prune

# Remove all unused networks
docker network prune

# Nuclear option — remove EVERYTHING unused
docker system prune -a --volumes

# Check disk usage
docker system df
```

**Example `docker system df` output:**

```
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          15        3         4.2GB     3.1GB (73%)
Containers      5         2         120MB     80MB (66%)
Volumes         8         3         2.1GB     1.5GB (71%)
Build Cache     30        0         500MB     500MB
```

---

## Quick Reference Table

| Task | Command |
|------|---------|
| Build an image | `docker build -t name .` |
| Run a container | `docker run -d -p 8000:8000 --name api image` |
| List running containers | `docker ps` |
| Stop a container | `docker stop api` |
| View logs | `docker logs -f api` |
| Shell into container | `docker exec -it api bash` |
| Remove container | `docker rm api` |
| Remove image | `docker rmi image` |
| List images | `docker images` |
| Create volume | `docker volume create data` |
| Create network | `docker network create net` |
| Clean up everything | `docker system prune -a` |

---

## Practice Exercise

1. Build your FastAPI app image: `docker build -t my-api .`
2. Run it with a name and port: `docker run -d -p 8000:8000 --name api my-api`
3. Check logs: `docker logs api`
4. Shell into the container: `docker exec -it api bash`
5. Stop and remove: `docker stop api && docker rm api`
6. Create a volume and run with persistent data
7. Check disk usage: `docker system df`

---

*Next Topic: Docker Compose — running multi-service applications.*
