# DevSecOps: Securing the Software Delivery Pipeline

## What Is DevSecOps?

DevSecOps integrates security into every stage of the software development lifecycle (SDLC) rather than treating it as an afterthought at release time. The core principle is **shift left** — find and fix vulnerabilities as early as possible, where changes are cheap, rather than discovering them in production where they are expensive and dangerous.

Traditional model:
```
Plan → Develop → Build → Test → Release → [Security review] → Deploy
                                                ↑ too late
```

DevSecOps model:
```
Plan → Develop → Build → Test → Release → Deploy → Monitor
 ↑        ↑        ↑       ↑       ↑         ↑        ↑
Risk    SAST    SCA/   DAST  Security  Image   Runtime
review  lint   secrets       gate    sign    alerts
```

---

## The Security Testing Toolkit

### SAST — Static Application Security Testing

SAST analyses source code, bytecode, or binaries **without executing them**. It's the fastest way to catch a broad class of bugs.

**What it finds:**
- SQL injection patterns (`"SELECT * FROM users WHERE id = " + user_input`)
- Hardcoded credentials (`password = "abc123"`)
- Dangerous function calls (`eval()`, `exec()`, `os.system()`)
- Insecure cryptography (MD5 for passwords, ECB mode for AES)
- Path traversal vulnerabilities
- XSS patterns in web code

**Tools:**

| Tool | Best for | Cost |
|------|---------|------|
| **Semgrep** | Multi-language, fast, custom rules | Free |
| **SonarQube** | Enterprise, technical debt tracking | OSS + paid |
| **CodeQL** | Deep analysis, GitHub-native | Free for OSS |
| **Bandit** | Python-specific | Free |
| **ESLint security plugins** | JavaScript/TypeScript | Free |

**Semgrep example — detect SQL injection pattern:**
```yaml
# .semgrep/rules/sql-injection.yaml
rules:
  - id: raw-sql-string-concat
    patterns:
      - pattern: |
          $DB.execute("..." + $USER_INPUT)
    message: "Possible SQL injection: never concatenate user input into SQL strings"
    languages: [python]
    severity: ERROR
```

**Integration in GitHub Actions:**
```yaml
- name: Semgrep SAST
  run: |
    pip install semgrep
    semgrep --config=auto . \
      --error \
      --json \
      --output=semgrep-report.json
```

**Limitations:** SAST has false positives. A reported pattern may not actually be exploitable in context. Tune rules and suppress known-safe patterns with inline comments (`# nosemgrep: rule-id`).

---

### DAST — Dynamic Application Security Testing

DAST tests the **running application** from the outside, simulating how an attacker would probe it. It cannot see source code — it sends HTTP requests and analyses responses.

**What it finds that SAST cannot:**
- Authentication and session management flaws
- Business logic vulnerabilities (e.g., negative quantity in cart gives refund)
- Server-side request forgery (SSRF) that only manifests at runtime
- Open redirects
- Security misconfiguration (exposed admin pages, directory listing)

**Tools:**

| Tool | Type | Cost |
|------|------|------|
| **OWASP ZAP** | Full-featured scanner | Free |
| **Burp Suite Enterprise** | CI/CD integration, automation | Paid |
| **Nuclei** | Template-based, fast | Free |

**ZAP in CI/CD (baseline scan mode):**
```yaml
- name: DAST Scan with ZAP
  run: |
    docker run --network=host \
      -v $(pwd):/zap/wrk/:rw \
      owasp/zap2docker-stable \
      zap-baseline.py \
      -t http://staging.yourapp.com \
      -r zap-report.html \
      -x zap-report.xml \
      --exit-code 1  # fail on alerts
```

**When to run:** In a staging environment after deployment. DAST needs a running app — never run it against production without authorisation and a proper scope agreement.

---

### SCA — Software Composition Analysis

Modern applications import hundreds of open-source libraries. SCA scans these dependencies against known vulnerability databases (NVD, OSV, GitHub Advisory).

**The Log4Shell lesson:** Log4j was buried inside dozens of enterprise products as a transitive dependency. A single CVE (CVE-2021-44228 — CVSS 10.0) affected millions of systems. SCA would have identified Log4j as a component and flagged it the moment the CVE was published.

**Tools:**

| Tool | Cost | Strengths |
|------|------|-----------|
| **Trivy** | Free | Containers, filesystems, SBOMs, IaC |
| **Snyk** | Free tier | Developer UX, PR comments |
| **Dependabot** | Free (GitHub) | Automated dependency updates |
| **OWASP Dependency-Check** | Free | Java/Python/.NET depth |

**Trivy scan commands:**
```bash
# Scan filesystem (requirements.txt, package.json, etc.)
trivy fs . --severity HIGH,CRITICAL

# Scan a Docker image
trivy image python:3.11-slim

# Generate SBOM (Software Bill of Materials)
trivy fs . --format cyclonedx --output sbom.json

# Scan Terraform IaC for misconfigs
trivy config ./terraform/
```

**Trivy output:**
```
requirements.txt (pip)
======================
Total: 2 (HIGH: 1, CRITICAL: 1)

┌─────────────────┬───────────┬──────────┬──────────────────┐
│ Library         │ CVE       │ Severity │ Fixed Version    │
├─────────────────┼───────────┼──────────┼──────────────────┤
│ Flask           │ CVE-2018- │ HIGH     │ 0.12.3           │
│ 0.12.2          │ 1000656   │          │                  │
├─────────────────┼───────────┼──────────┼──────────────────┤
│ requests        │ CVE-2018- │ CRITICAL │ 2.20.0           │
│ 2.18.0          │ 18074     │          │                  │
└─────────────────┴───────────┴──────────┴──────────────────┘
```

---

## Secrets Management

### Why Secrets in Code Are a Critical Issue

Git is permanent. When a developer commits an API key to a public (or private) repository:
1. Bots crawl GitHub and find it within seconds
2. Even if the commit is reverted, the key exists in git history, in forks, and in GitHub's index
3. The only correct response is **immediate revocation** of the key

**Common secrets accidentally committed:**
- AWS access keys (`AKIA...`)
- Private SSH keys (`-----BEGIN RSA PRIVATE KEY-----`)
- Database connection strings (`postgresql://user:password@host/db`)
- JWT signing secrets
- Firebase service account JSON files
- Stripe/Razorpay API keys

### Pre-commit Prevention

Install `git-secrets` or `detect-secrets` as a pre-commit hook:
```bash
# Install detect-secrets
pip install detect-secrets

# Scan current codebase
detect-secrets scan . > .secrets.baseline

# Set up pre-commit hook
detect-secrets-hook --baseline .secrets.baseline
```

The hook runs before every commit and refuses to commit if a secret pattern is found.

### Secrets Scanning in CI

**TruffleHog** scans the entire git history, not just the current state:
```yaml
- name: TruffleHog Secret Scan
  uses: trufflesecurity/trufflehog@main
  with:
    path: ./
    base: HEAD~1  # compare from 1 commit ago
    head: HEAD
    extra_args: --only-verified  # only flag verified live secrets
```

### Secrets at Runtime — HashiCorp Vault

Never bake secrets into Docker images or environment variables in CI config. Use a secrets manager:

**HashiCorp Vault — dynamic secrets:**
```bash
# App requests a database credential at runtime
vault read database/creds/my-app
# Returns: username=v-app-xyz12345, password=A1b2c3D4e5f6 (expires in 1h)
```

Key benefits:
- Secrets expire automatically — no stale credentials
- Every access is audited in the Vault audit log
- Revocation is instant if compromise is suspected

**AWS-native alternative:** AWS Secrets Manager or Parameter Store:
```python
import boto3
client = boto3.client('secretsmanager', region_name='ap-south-1')
secret = client.get_secret_value(SecretId='prod/myapp/db-password')
db_password = secret['SecretString']
```

---

## Supply Chain Security

### The Attack Surface

Your application's supply chain includes:
- Open-source libraries you import (npm, pip, Maven)
- Build tools and CI/CD systems themselves
- Container base images (what's in that `python:3.11-slim`?)
- Infrastructure-as-Code modules (Terraform registry)
- Third-party GitHub Actions

**SolarWinds attack (2020):** Attackers compromised SolarWinds' own build pipeline and inserted malicious code into signed updates. 18,000 organisations downloaded the malicious update because it was signed by SolarWinds itself. This is the worst-case supply chain scenario.

### Dependency Confusion Attack

In 2021, security researcher Alex Birsan demonstrated that many companies could be compromised by publishing public packages with the same name as their private internal packages. When `npm install` or `pip install` runs, the package manager may prefer the public (malicious) version over the private (legitimate) internal one.

**Mitigation:**
- Use `--prefer-offline` or private registry locks
- Namespace your internal packages with a company prefix
- Configure package managers to only use your private registry for internal packages

### SLSA Framework

**Supply chain Levels for Software Artifacts** defines four levels of build provenance:

| Level | Requirement | Example |
|-------|------------|---------|
| L1 | Scripted build, provenance exists | GitHub Actions build |
| L2 | Hosted build, signed provenance | Build signed with GitHub OIDC token |
| L3 | Hardened build, non-falsifiable provenance | Hermetic build, ephemeral credentials |
| L4 | Two-party review, reproducible builds | Rare, highest assurance |

**SBOM (Software Bill of Materials):** Generate one for every release:
```bash
# Generate CycloneDX SBOM with Syft
syft packages python:3.11-slim -o cyclonedx-json > sbom.json
```

When Log4Shell happened, teams with SBOMs knew within minutes which of their containers contained Log4j. Teams without SBOMs spent days auditing manually.

---

## GitHub Actions Security Best Practices

### Principle of Least Privilege for Workflows

```yaml
permissions:
  contents: read      # only read the repo
  security-events: write  # only what's needed for SARIF upload

jobs:
  scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read   # job-level overrides workflow-level
```

### Pin Action Versions to SHA (not tag)

```yaml
# INSECURE — tag can be changed by the action author
- uses: actions/checkout@v4

# SECURE — SHA cannot be changed
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11
```

If a popular GitHub Action account is compromised, an attacker can push a new commit to the `v4` tag. SHA pinning means your workflow runs exactly what you audited.

### OIDC for Cloud Authentication

Instead of storing AWS credentials as GitHub Secrets, use OpenID Connect:
```yaml
jobs:
  deploy:
    permissions:
      id-token: write  # required for OIDC
      contents: read
    steps:
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/github-actions-role
          aws-region: ap-south-1
      # No secret stored anywhere — GitHub gets a short-lived token from AWS STS
```

### Branch Protection and Required Status Checks

A pipeline is only as good as its enforcement. Configure branch protection on `main`:
1. Require pull request reviews
2. Require all these status checks to pass before merging
3. Require branches to be up to date
4. Restrict who can push directly to main

Without branch protection, a developer can push directly to main, bypassing all your beautiful SAST/DAST/SCA gates.

---

## Container Security

### Image Scanning

Every container image you ship is a package of software. Scan it before pushing:
```bash
# Scan image before push
trivy image myapp:latest --exit-code 1 --severity CRITICAL

# Scan official base image to choose the most secure one
trivy image python:3.11         # Full: 100+ vulnerabilities
trivy image python:3.11-slim    # Reduced: 40+ vulnerabilities
trivy image python:3.11-alpine  # Minimal: 5 vulnerabilities
```

### Dockerfile Security

```dockerfile
# BAD — running as root
FROM python:3.11-slim
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]

# GOOD — non-root user, minimal attack surface
FROM python:3.11-alpine
RUN adduser -D -s /bin/sh appuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=appuser:appuser . .
USER appuser
EXPOSE 8000
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]
```

Key principles:
- Never run containers as root
- Use minimal base images (alpine vs slim vs full)
- Don't copy secrets into the image; use runtime secrets injection
- Use multi-stage builds to keep build tools out of the final image

### Image Signing with Cosign

```bash
# Sign image after pushing to registry
cosign sign --key cosign.key gcr.io/myproject/myapp:latest

# Verify image signature before deploying
cosign verify --key cosign.pub gcr.io/myproject/myapp:latest
```

Kubernetes admission controllers (like Sigstore's Policy Controller) can enforce that only signed images are deployed, rejecting unsigned or tampered images at deploy time.

---

## Full DevSecOps Pipeline Reference

```
Developer commits code
         ↓
Pre-commit hooks
  ├── detect-secrets (secret patterns)
  ├── semgrep (quick SAST)
  └── lint (code quality)
         ↓
CI Pipeline (GitHub Actions)
  ├── SAST: Semgrep / CodeQL
  ├── SCA: Trivy / Dependabot
  ├── Secrets: TruffleHog
  ├── IaC: Checkov / Trivy config
  └── SBOM generation
         ↓
   [Security Gate — block merge on CRITICAL]
         ↓
Container Build
  ├── Multi-stage Dockerfile
  ├── Non-root user
  └── Trivy image scan
         ↓
Registry Push
  └── Cosign image signing
         ↓
Deploy to Staging
  ├── DAST: OWASP ZAP baseline scan
  └── OWASP Dependency-Check
         ↓
   [Security Gate — block prod deploy on failures]
         ↓
Deploy to Production
  └── Runtime security monitoring
         (Falco, AWS GuardDuty, Datadog)
```
