# Module 15 — Assignment: Cloud Deployment

**Submission Deadline:** End of Week 15 (as announced by your trainer)
**How to Submit:** Push all code to your GitHub repository. Share the live deployed URL and your GitHub repo link via the TechPath student portal.

---

## Task 1: Deploy a FastAPI App to Render (Free Tier)

**Difficulty:** Beginner

Take any FastAPI project you built in earlier modules (Module 6 or later) and deploy it to Render.

**What to Do:**
1. Make sure your project has a proper `requirements.txt` with all dependencies
2. Add a `/health` endpoint that returns `{"status": "healthy", "app": "your-app-name"}`
3. Create a `render.yaml` file in your project root (refer to the code snap in this module)
4. Push your code to a public GitHub repository
5. Connect the repo to Render and deploy
6. Verify your app is live by visiting the Render URL

**Deliverables:**
- Live URL of your deployed app (e.g., `https://your-app.onrender.com`)
- Screenshot of the Render dashboard showing a successful deployment
- Screenshot of your `/health` endpoint working in the browser
- GitHub repo link with the `render.yaml` file

---

## Task 2: Set Up a Cloud Database and Connect It

**Difficulty:** Intermediate

Set up a free PostgreSQL database on Supabase or Neon, and connect your deployed app to it.

**What to Do:**
1. Create a free account on [Supabase](https://supabase.com) or [Neon](https://neon.tech)
2. Create a new PostgreSQL database
3. Get the connection string (DATABASE_URL)
4. Update your deployed app's environment variables on Render to use this database
5. Run your database migrations (Alembic) against the cloud database
6. Add at least 3 sample records using your API (e.g., 3 students: Rahul from Bhopal, Priya from Delhi, Vikram from Pune)
7. Verify the data persists by restarting your Render service

**Deliverables:**
- Screenshot of your Supabase/Neon dashboard showing the database and tables
- Screenshot of your API returning data from the cloud database
- Brief write-up (5-10 lines) explaining:
  - Which database service you chose and why
  - The connection string format (with password hidden as `***`)
  - Any issues you faced and how you solved them

---

## Task 3: Create a CI/CD Pipeline with GitHub Actions

**Difficulty:** Intermediate-Advanced

Set up a GitHub Actions workflow that automatically runs tests and deploys your app when you push to the `main` branch.

**What to Do:**
1. Create a `.github/workflows/deploy.yml` file in your project
2. The workflow should:
   - Trigger on push to `main`
   - Install Python dependencies
   - Run at least 3 tests using pytest (write the tests if you do not have them)
   - Deploy to Render using a [Deploy Hook](https://render.com/docs/deploy-hooks) (Render gives you a URL to trigger deployments)
3. Push your workflow file and verify it runs in the "Actions" tab on GitHub
4. Make a small code change, push to main, and show the pipeline running

**Deliverables:**
- GitHub repo link with the workflow file at `.github/workflows/deploy.yml`
- Screenshot of the GitHub Actions tab showing a successful run (green checkmark)
- Screenshot showing all 3 steps (install, test, deploy) passing
- Brief write-up (5-10 lines) explaining what each step in your workflow does

---

## Task 4: Azure Deployment with Monitoring (Bonus Challenge)

**Difficulty:** Advanced

Deploy your app to Azure Container Apps and set up basic monitoring. This task uses Azure's free tier (you get ₹13,500 free credit when you sign up).

**What to Do:**
1. Sign up for an Azure free account at [azure.microsoft.com/free](https://azure.microsoft.com/en-in/free/)
2. Install Azure CLI on your computer
3. Create a Dockerfile for your FastAPI app
4. Build and push the Docker image to Azure Container Registry
5. Deploy to Azure Container Apps (use the commands from the notes)
6. Set up monitoring:
   - Sign up for [UptimeRobot](https://uptimerobot.com) (free)
   - Add your Azure app URL as a monitor
   - Set up email alerts for downtime
7. Add logging to at least 2 endpoints in your FastAPI app

**Deliverables:**
- Live URL of your app on Azure (e.g., `https://techpath-api.xxx.azurecontainerapps.io`)
- Dockerfile in your GitHub repo
- Screenshot of Azure Portal showing your Container App running
- Screenshot of UptimeRobot dashboard with your monitor
- Screenshot of app logs in Azure Portal (Container Apps > Log stream)
- Brief write-up (10-15 lines) comparing Azure deployment vs Render deployment:
  - Which was easier?
  - Which gives more control?
  - When would you use each?

---

## Grading Rubric

| Criteria | Marks | Details |
|----------|-------|---------|
| **Task 1: Render Deployment** | 25 | App is live, health check works, render.yaml is correct |
| **Task 2: Cloud Database** | 25 | Database connected, data persists, write-up is clear |
| **Task 3: CI/CD Pipeline** | 25 | Workflow runs, tests pass, deployment triggers |
| **Task 4: Azure + Monitoring** | 25 (Bonus) | Azure deployment works, monitoring set up, comparison written |
| **Code Quality** | — | Clean code, proper .gitignore, no secrets in code (deduction if violated) |
| **Total** | 75 + 25 Bonus | Minimum 50 marks to pass |

> **Important:** Never commit passwords, API keys, or database URLs to GitHub. Use environment variables and GitHub Secrets. If a reviewer finds secrets in your code, 10 marks will be deducted.

---

## Tips from TechPath Institute

- **Start with Task 1** — it takes only 10-15 minutes if your code is ready
- **Task 2 builds on Task 1** — use the same Render deployment
- **Ask for help early** — deployment issues can be tricky the first time
- **Read error logs** — 90% of deployment problems are explained in the logs
- **Keep your GitHub repo clean** — add a `.gitignore` file to exclude `__pycache__/`, `.env`, `venv/`, etc.
