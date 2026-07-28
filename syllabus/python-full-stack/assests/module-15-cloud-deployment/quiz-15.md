# Cloud Deployment — Quiz

**Module 15 | 15 Questions**

---

### Q1. Which free-tier platform is the easiest for deploying a Python FastAPI app for the first time?

- A) AWS Lambda
- B) Render — it auto-detects Python and deploys with minimal setup ✅
- C) Azure Virtual Machines
- D) Google Kubernetes Engine

> **Explanation:** Render is the most beginner-friendly platform. You connect your GitHub repo, it detects Python, and you provide a start command. It auto-deploys on every push with a generous free tier of 750 hours/month.

---

### Q2. What happens to a Render free-tier app when it receives no requests for 15 minutes?

- A) It gets deleted
- B) It continues running normally
- C) It goes to sleep and takes 30-60 seconds to wake up on the next request ✅
- D) It automatically upgrades to a paid plan

> **Explanation:** Render free-tier services go to sleep after 15 minutes of inactivity. The first request after sleeping triggers a "cold start" that takes 30-60 seconds. Subsequent requests are fast until the next idle period.

---

### Q3. Why should you use Supabase's pooler port (6543) instead of the direct connection port (5432) for your app?

- A) Port 6543 is faster
- B) Port 5432 doesn't support SSL
- C) The pooler manages connection limits efficiently — direct connections are limited and should only be used for migrations ✅
- D) Port 6543 is the only port that works

> **Explanation:** Supabase's connection pooler (Supavisor) on port 6543 efficiently manages database connections. Direct connections on port 5432 are limited in number and should only be used for admin tasks like running migrations.

---

### Q4. What is Neon's unique feature that sets it apart from other cloud databases?

- A) It supports MongoDB
- B) Database branching — create instant copies of your database for testing, like Git branches for code ✅
- C) It is the cheapest option
- D) It only works with Azure

> **Explanation:** Neon supports database branching — you can create an instant copy of your production database to test migrations safely. The branch shares storage with the parent (no duplication), and you can delete it when done.

---

### Q5. When deploying a frontend to Vercel, what happens when you open a Pull Request?

- A) Nothing — PRs are ignored
- B) Vercel creates a unique preview deployment URL and comments it on the PR ✅
- C) It deploys directly to production
- D) It runs tests but doesn't deploy

> **Explanation:** Vercel creates a unique preview deployment for every PR. The preview URL is automatically commented on the PR, allowing reviewers to test changes live without running anything locally.

---

### Q6. What is the purpose of an SSL certificate for your website?

- A) It makes the website load faster
- B) It encrypts data between the browser and server, shown as HTTPS with a padlock icon ✅
- C) It prevents the website from being hacked
- D) It is required only for e-commerce sites

> **Explanation:** SSL certificates enable HTTPS, encrypting all data transmitted between the user's browser and your server. Without it, browsers show "Not Secure" warnings, and sensitive data like passwords travel as plain text.

---

### Q7. In Azure, what is a Resource Group?

- A) A team of Azure administrators
- B) A logical container that groups related Azure resources for organization, access control, and cost tracking ✅
- C) A virtual machine group
- D) A database cluster

> **Explanation:** A Resource Group is like a folder for Azure resources. It groups related items (app, database, storage) together for organization, shared access control, cost tracking, and easy cleanup — deleting the group removes all resources inside.

---

### Q8. What is the advantage of Azure Container Apps over Azure App Service for microservices?

- A) Container Apps is always cheaper
- B) Container Apps can scale to zero (no cost when idle) and supports multiple containers with advanced auto-scaling ✅
- C) App Service doesn't support Python
- D) Container Apps doesn't require Docker

> **Explanation:** Azure Container Apps is designed for microservices — it can scale to zero (pay nothing when idle), run multiple containers, use KEDA-based auto-scaling, and integrate with Dapr. App Service is simpler but always runs (and charges).

---

### Q9. Why should you use Azure Key Vault instead of environment variables for production secrets?

- A) Key Vault is faster to read
- B) Key Vault provides encryption at rest, access control, audit logging, and secret rotation — environment variables have none of these ✅
- C) Environment variables don't work in Docker
- D) Key Vault is free while environment variables cost money

> **Explanation:** Key Vault encrypts secrets at rest and in transit, provides fine-grained access control (who can read which secrets), logs every access for auditing, supports versioning and rotation — none of which plain environment variables offer.

---

### Q10. What is the purpose of a /health endpoint in a production API?

- A) To show health tips to users
- B) To provide a simple endpoint that monitoring tools can ping to verify the app and database are working ✅
- C) To display server hardware information
- D) To reset the application

> **Explanation:** A /health endpoint returns a simple status (200 OK if healthy, 503 if not) that monitoring tools, load balancers, and container orchestrators use to verify the app is working. It typically checks the database connection and returns quickly.

---

### Q11. What does 99.9% uptime SLA mean in terms of allowed monthly downtime?

- A) No downtime allowed
- B) About 7 hours per month
- C) About 43 minutes per month ✅
- D) About 4 minutes per month

> **Explanation:** 99.9% uptime means 0.1% downtime per month. 0.1% of approximately 43,200 minutes in a month is approximately 43 minutes. This is a common SLA target for production web services.

---

### Q12. In a three-environment strategy, which branch typically maps to the staging environment?

- A) main
- B) develop ✅
- C) feature/*
- D) release/*

> **Explanation:** In the standard branch strategy: feature/* branches map to local development, the develop branch auto-deploys to staging for testing, and the main branch deploys to production after approval.

---

### Q13. What is zero-downtime deployment?

- A) Deploying without any code changes
- B) Deploying in a way that users never experience errors or interruptions during the update ✅
- C) Deploying at midnight when no one is using the app
- D) Deploying without testing

> **Explanation:** Zero-downtime deployment ensures users never see errors during updates. Strategies include rolling updates (replace one container at a time) and blue-green deployment (switch traffic between two identical environments).

---

### Q14. What does 'order: start-first' mean in a Docker Compose deploy configuration?

- A) Start containers in alphabetical order
- B) Start the new container and verify it's healthy before stopping the old one — ensures zero downtime ✅
- C) Start the first service defined in the file
- D) Start containers on the first available server

> **Explanation:** With "order: start-first", Docker starts the new version container and waits for its health check to pass before stopping the old one. This ensures there is always a healthy container serving requests — zero downtime.

---

### Q15. What is the recommended log level for a production FastAPI application?

- A) DEBUG — log everything for maximum detail
- B) INFO or WARNING — log important events without excessive noise ✅
- C) CRITICAL — only log when the app is about to crash
- D) No logging in production

> **Explanation:** Production apps should use INFO or WARNING level. DEBUG is too verbose and can impact performance and generate huge log files. CRITICAL is too quiet — you would miss important error information. INFO/WARNING provides the right balance.
