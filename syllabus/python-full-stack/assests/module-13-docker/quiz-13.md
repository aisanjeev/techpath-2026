# Docker & Containerization — Quiz

**Module 13 | 15 Questions**

---

### Q1. What problem does Docker primarily solve?

- A) Making websites load faster
- B) The "it works on my machine" problem — environment inconsistency ✅
- C) Writing Python code automatically
- D) Replacing GitHub for version control

> **Explanation:** Docker packages your app with all its dependencies into a container, ensuring it runs the same way on every machine — solving the classic "it works on my machine" problem.

---

### Q2. What is the main difference between a Docker container and a virtual machine (VM)?

- A) Containers are more expensive to run
- B) VMs share the host OS kernel while containers don't
- C) Containers share the host OS kernel, making them lightweight, while VMs run a full OS each ✅
- D) Containers can only run Linux applications

> **Explanation:** Containers share the host OS kernel and are process-level isolated, making them much lighter (MBs vs GBs) and faster to start (seconds vs minutes) compared to VMs that run a full OS.

---

### Q3. What is the relationship between a Docker image and a Docker container?

- A) They are the same thing
- B) An image is a running instance of a container
- C) A container is a running instance of an image ✅
- D) Images can only be downloaded, not created

> **Explanation:** An image is a read-only template (like a recipe), and a container is a running instance created from that image (like the cooked dish). One image can create many containers.

---

### Q4. Which Dockerfile instruction should always be the first line?

- A) WORKDIR
- B) RUN
- C) FROM ✅
- D) CMD

> **Explanation:** Every Dockerfile must start with FROM, which specifies the base image to build upon (e.g., FROM python:3.12-slim).

---

### Q5. Why should you copy requirements.txt and install dependencies BEFORE copying the rest of your code?

- A) Python requires it in that order
- B) For Docker layer caching — dependencies rarely change, so this layer stays cached even when code changes ✅
- C) The Dockerfile won't build otherwise
- D) It makes the image smaller

> **Explanation:** Docker caches each layer. Since requirements.txt changes rarely but code changes often, installing deps first means Docker reuses the cached dependency layer on code-only changes, making builds much faster.

---

### Q6. What does the flag -p 8000:8000 do in 'docker run -p 8000:8000 my-app'?

- A) Sets the app's password to 8000
- B) Maps port 8000 on the host machine to port 8000 inside the container ✅
- C) Opens 8000 connections to the container
- D) Limits the container to use 8000 MB of memory

> **Explanation:** The -p flag maps ports in the format host:container. So -p 8000:8000 means accessing localhost:8000 on your machine routes traffic to port 8000 inside the container.

---

### Q7. What is the purpose of a .dockerignore file?

- A) To list files that Docker should delete after building
- B) To prevent specific files from being sent to the Docker build context ✅
- C) To ignore Docker errors during the build
- D) To list containers that should not be started

> **Explanation:** The .dockerignore file tells Docker which files to exclude from the build context (like .git, .env, node_modules). This makes builds faster and prevents sensitive files from ending up in the image.

---

### Q8. In Docker Compose, how does one service connect to another by hostname?

- A) Using localhost
- B) Using the service name defined in docker-compose.yml ✅
- C) Using the container's IP address only
- D) Services cannot communicate with each other

> **Explanation:** Docker Compose creates a network where services can reach each other using their service name as hostname. For example, if your database service is named "db", the API connects to it at "db:5432".

---

### Q9. What does 'docker compose down -v' do?

- A) Stops services with verbose output
- B) Stops services and shows the version
- C) Stops services, removes containers, networks, AND deletes volumes (data loss!) ✅
- D) Stops only the services with volumes attached

> **Explanation:** The -v flag with "docker compose down" removes named volumes along with containers and networks. This means persistent data (like database contents) will be permanently deleted.

---

### Q10. What is the benefit of a multi-stage Docker build?

- A) It runs the app in multiple stages for better performance
- B) It uses one stage for building/compiling and a clean stage for the final image, reducing size ✅
- C) It allows running multiple apps in one container
- D) It automatically scales the application

> **Explanation:** Multi-stage builds use a "builder" stage to install build tools and compile dependencies, then copy only the compiled output to a fresh, slim final image. Build tools like gcc are left behind, dramatically reducing image size.

---

### Q11. Why should you use '--host 0.0.0.0' when running uvicorn inside a Docker container?

- A) It makes the app run faster
- B) It is required by Docker to start the container
- C) By default uvicorn binds to 127.0.0.1 (localhost only), which is unreachable from outside the container ✅
- D) It enables HTTPS

> **Explanation:** 127.0.0.1 means "only accept connections from inside this machine." Inside a container, that means only the container itself can connect. Using 0.0.0.0 makes the app accept connections from any network interface, including the host machine.

---

### Q12. Which Docker command lets you run a bash shell inside an already running container?

- A) docker run -it container bash
- B) docker exec -it container bash ✅
- C) docker shell container
- D) docker ssh container

> **Explanation:** "docker exec -it container bash" executes a new command (bash) inside an already running container. "docker run" would create a new container instead.

---

### Q13. What is the recommended Python base image for production Dockerfiles?

- A) python:3.12 (full image, ~900 MB)
- B) python:3.12-slim (~150 MB) ✅
- C) ubuntu:22.04
- D) python:3.12-alpine (~50 MB)

> **Explanation:** python:3.12-slim is the recommended choice for production. It is much smaller than the full image but has better package compatibility than alpine. It provides a good balance of size and reliability.

---

### Q14. Where should you NEVER store secrets like API keys and database passwords?

- A) In environment variables passed at runtime
- B) In a .env.local file (added to .gitignore)
- C) Hardcoded in the Dockerfile using ENV instruction ✅
- D) In a secrets manager like Azure Key Vault

> **Explanation:** Secrets in a Dockerfile's ENV instruction get baked into the image layer and are visible via "docker history". Anyone who pulls the image can see them. Use runtime environment variables or a secrets manager instead.

---

### Q15. What is the correct image naming format for pushing to GitHub Container Registry (GHCR)?

- A) github.com/username/image:tag
- B) ghcr.io/username/image:tag ✅
- C) registry.github.com/username/image:tag
- D) username/image:tag

> **Explanation:** GHCR uses the format ghcr.io/username/image:tag. For example: ghcr.io/rahul2024/fastapi-app:v1.0. The ghcr.io prefix tells Docker to push to GitHub's registry instead of Docker Hub.
