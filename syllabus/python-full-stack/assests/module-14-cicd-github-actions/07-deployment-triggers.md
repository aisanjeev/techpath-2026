# Deployment Triggers & Rollback Strategies

**Module 14 — CI/CD with GitHub Actions | Topic 7**

---

## Deployment Strategies

Once your CI pipeline passes and the Docker image is built, how do you get it to your server? There are several deployment strategies, each with different tradeoffs.

### Strategy 1: SSH Deploy (Simple — VPS)

The most straightforward approach. Your CI pipeline connects to the server via SSH and runs commands.

```yaml
deploy:
  name: Deploy to VPS
  runs-on: ubuntu-latest
  needs: [test, build]
  if: github.ref == 'refs/heads/main'

  steps:
    - name: Deploy via SSH
      run: |
        mkdir -p ~/.ssh
        echo "${{ secrets.DEPLOY_SSH_KEY }}" > ~/.ssh/id_ed25519
        chmod 600 ~/.ssh/id_ed25519
        ssh -o StrictHostKeyChecking=no ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }} << 'EOF'
          cd /opt/my-app
          docker compose pull
          docker compose up -d --remove-orphans
          docker image prune -f
        EOF
```

**How it works:**
1. CI connects to the server via SSH
2. Runs `docker compose pull` to download the new image
3. Runs `docker compose up -d` to restart with the new image
4. Cleans up old images

**Best for:** Small projects, single-server deployments, student projects.

### Strategy 2: Webhook Deploy

The server listens for a webhook call from GitHub and deploys itself.

```yaml
deploy:
  runs-on: ubuntu-latest
  needs: build
  steps:
    - name: Trigger deployment webhook
      run: |
        curl -X POST \
          -H "Authorization: Bearer ${{ secrets.DEPLOY_TOKEN }}" \
          -H "Content-Type: application/json" \
          -d '{"image": "ghcr.io/${{ github.repository }}:${{ github.sha }}"}' \
          https://api.techpath.biz/deploy/webhook
```

**Best for:** When you don't want to expose SSH access.

### Strategy 3: Platform-Specific Deploy

Cloud platforms have their own deployment mechanisms:

```yaml
# Deploy to Render
deploy:
  runs-on: ubuntu-latest
  needs: test
  steps:
    - name: Trigger Render deploy
      run: |
        curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK_URL }}

# Deploy to Railway
deploy:
  runs-on: ubuntu-latest
  needs: test
  steps:
    - name: Deploy to Railway
      uses: bervProject/railway-deploy@main
      with:
        railway_token: ${{ secrets.RAILWAY_TOKEN }}
        service: my-api
```

---

## Deployment Triggers

### Trigger: Push to Main

The most common pattern — deploy whenever code is merged to main.

```yaml
on:
  push:
    branches: [main]

jobs:
  test:
    # ... run tests

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    # ... deploy
```

### Trigger: Release Published

Deploy only when a GitHub release is created (more controlled).

```yaml
on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying version ${{ github.event.release.tag_name }}"
```

### Trigger: Manual with Inputs

Let the team decide when to deploy.

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        type: choice
        options:
          - staging
          - production
      version:
        description: 'Version to deploy'
        required: false
        default: 'latest'

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - run: echo "Deploying ${{ inputs.version }} to ${{ inputs.environment }}"
```

### Trigger: Branch-Based Environments

```yaml
on:
  push:
    branches: [main, develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        if: github.ref == 'refs/heads/develop'
        run: echo "Deploying to staging server"

      - name: Deploy to production
        if: github.ref == 'refs/heads/main'
        run: echo "Deploying to production server"
```

| Branch | Deploys To |
|--------|-----------|
| `develop` | Staging (https://staging.api.techpath.biz) |
| `main` | Production (https://api.techpath.biz) |

---

## Rollback Strategies

Things go wrong. Your deployment might break the app. You need a way to undo it quickly.

### Rollback 1: Redeploy Previous Image

Since every Docker image is tagged with the git SHA, you can redeploy the previous version:

```bash
# On the server — rollback to previous version
docker compose pull  # This pulls the broken latest
# Instead, specify the previous version:
docker pull ghcr.io/user/app:abc1234   # Previous working SHA
docker tag ghcr.io/user/app:abc1234 ghcr.io/user/app:latest
docker compose up -d
```

### Rollback 2: Git Revert

Create a revert commit and let CI/CD redeploy:

```bash
# Revert the last commit
git revert HEAD
git push origin main
# CI/CD runs → builds new image → deploys automatically
```

**Advantage:** Creates an audit trail. Everyone can see the revert in git history.

### Rollback 3: GitHub Actions Manual Rollback

```yaml
# .github/workflows/rollback.yml
name: Rollback Deployment

on:
  workflow_dispatch:
    inputs:
      commit-sha:
        description: 'Git commit SHA to rollback to'
        required: true

jobs:
  rollback:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy specific version
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.DEPLOY_SSH_KEY }}" > ~/.ssh/id_ed25519
          chmod 600 ~/.ssh/id_ed25519
          ssh -o StrictHostKeyChecking=no ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }} << EOF
            cd /opt/my-app
            docker pull ghcr.io/${{ github.repository }}:${{ inputs.commit-sha }}
            docker tag ghcr.io/${{ github.repository }}:${{ inputs.commit-sha }} \
                       ghcr.io/${{ github.repository }}:latest
            docker compose up -d
          EOF
```

This adds a "Run workflow" button where you enter the commit SHA to rollback to.

---

## Health Checks After Deployment

Always verify the deployment succeeded:

```yaml
  - name: Deploy
    run: |
      ssh ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }} \
        "cd /opt/app && docker compose pull && docker compose up -d"

  - name: Wait for app to start
    run: sleep 15

  - name: Health check
    run: |
      STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://api.techpath.biz/health)
      if [ "$STATUS" != "200" ]; then
        echo "Health check failed! Status: $STATUS"
        exit 1
      fi
      echo "Health check passed! Status: $STATUS"
```

If the health check fails, you can automatically rollback:

```yaml
  - name: Rollback on failure
    if: failure()
    run: |
      ssh ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }} << 'EOF'
        cd /opt/app
        docker compose down
        docker tag ghcr.io/user/app:previous ghcr.io/user/app:latest
        docker compose up -d
      EOF
```

---

## Deployment Notifications

Let your team know when deployments happen:

```yaml
  - name: Notify on Slack
    if: always()
    run: |
      STATUS=${{ job.status }}
      curl -X POST ${{ secrets.SLACK_WEBHOOK_URL }} \
        -H 'Content-Type: application/json' \
        -d "{
          \"text\": \"Deployment $STATUS: ${{ github.repository }} by ${{ github.actor }}\"
        }"
```

---

## Complete Deployment Workflow

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12', cache: 'pip' }
      - run: pip install -r requirements.txt
      - run: pytest --cov=app --cov-fail-under=70

  build:
    name: Build Docker
    runs-on: ubuntu-latest
    needs: test
    permissions: { contents: read, packages: write }
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ github.sha }}
            ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    environment: production
    steps:
      - name: Deploy via SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.DEPLOY_SSH_KEY }}" > ~/.ssh/id_ed25519
          chmod 600 ~/.ssh/id_ed25519
          ssh -o StrictHostKeyChecking=no ${{ secrets.DEPLOY_USER }}@${{ secrets.DEPLOY_HOST }} \
            "cd /opt/app && docker compose pull && docker compose up -d && docker image prune -f"

      - name: Health check
        run: |
          sleep 15
          curl -f https://api.techpath.biz/health || exit 1
```

---

## Practice Exercise

1. Create a deployment workflow triggered by push to main
2. Add a manual rollback workflow with `workflow_dispatch`
3. Add a health check step after deployment
4. Set up a `production` environment with required reviewers
5. Test the full flow: push → test → build → deploy → health check

---

*Next Topic: Branch Protection Rules — enforcing code quality before merging.*
