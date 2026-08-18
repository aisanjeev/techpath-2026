# Month 12 — Assignment: DevSecOps, GRC & Capstone

**Deadline:** End of Month 12 (Week 52)
**Submission:** GitHub portfolio + LinkedIn post + PDF summary
**Total:** 100 marks

---

## Task 1: Build a DevSecOps CI/CD Security Pipeline (35 marks)

Create a GitHub repository with a simple web application (any language — even a basic Python Flask "Hello World" app) and add a **GitHub Actions security pipeline** that automatically runs on every push.

### The pipeline MUST include:
1. **SAST scan** using Semgrep (`semgrep --config=auto .`)
2. **Dependency vulnerability scan** using Trivy (`trivy fs . --severity HIGH,CRITICAL`)
3. **Secret scanning** using TruffleHog (`trufflehog git . --since-commit HEAD~1`)
4. **Dockerfile scan** (if you have a Dockerfile) using Trivy image scan
5. A **security gate** — the pipeline must FAIL (non-zero exit) if any CRITICAL finding is found

### Demo: Introduce a deliberate vulnerability
- Add a `requirements.txt` with a known vulnerable package (e.g., `Flask==0.12.2` — has CVEs)
- Run the pipeline — screenshot showing Trivy detected the vulnerable dependency
- Fix the version — run again — screenshot showing pipeline passes

**Submit:** GitHub repo link showing Actions tab with both a FAIL run and a PASS run.

**Marking:**
- All 3 scan types in pipeline: 15 marks
- Security gate configured correctly: 8 marks
- Deliberate vuln → detection → fix demo: 12 marks

---

## Task 2: GRC Risk Assessment (25 marks)

Perform a mini risk assessment for a fictional SaaS startup that stores customer data, processes payments, and has 15 employees.

**Identify and document 8 information security risks** in a Risk Register table with these columns:

| Risk ID | Risk Description | Likelihood (1-5) | Impact (1-5) | Risk Score | Owner | Current Controls | Residual Risk | Treatment |
|---------|----------------|-----------------|-------------|-----------|-------|----------------|--------------|-----------|

**Requirements:**
- At least 2 risks must score HIGH (≥12)
- At least 1 risk must relate to the DPDP Act (personal data protection)
- At least 1 risk must relate to a supply chain/third-party vendor
- Each risk must have a proposed treatment (mitigate, transfer, accept, or avoid)

**Then answer:** Which ISO 27001 Annex A controls would address the two highest-scoring risks?

**Submit:** Risk register table in a PDF or Excel file.

**Marking:**
- 8 risks with all columns complete: 12 marks
- DPDP and supply chain risks included: 6 marks
- ISO 27001 control mapping for top 2 risks: 7 marks

---

## Task 3: DevSecOps Tools Hands-On (15 marks)

Complete ALL three of these quick hands-on exercises:

**Exercise A — SonarQube Local Scan (5 marks):**
```bash
# Run SonarQube via Docker
docker run -d -p 9000:9000 sonarqube:community
# Browse to http://localhost:9000 (admin/admin)
# Create project → run sonar-scanner on your repo
# Screenshot showing issues found in Quality Gate report
```

**Exercise B — OWASP ZAP Quick Scan (5 marks):**
```bash
# Scan DVWA (your homelab) or OWASP Juice Shop
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t http://your-target-url -r report.html
# Open report.html and screenshot the findings summary
```

**Exercise C — Secrets in Git History (5 marks):**
```bash
# Create a test repo with a "leaked" secret in history
git init test-repo && cd test-repo
echo "API_KEY=sk-1234567890abcdef" > .env
git add .env && git commit -m "add config"
git rm .env && git commit -m "remove secret (too late!)"

# Run TruffleHog to find it
trufflehog git . --since-commit HEAD~2 --no-verification
# Screenshot showing TruffleHog found the secret in Git history
```

**Submit:** Screenshots of all 3 exercises.

---

## Task 4: Capstone Portfolio (25 marks)

Your final portfolio must tell the story of your 12-month journey. Publish everything to GitHub and submit a **2-page PDF summary**.

**GitHub Portfolio structure:**
```
README.md (12-month summary, skills, certifications, current goals)
├── /month-01-networks/       Wireshark capture + anatomy writeup
├── /month-02-os-linux/       Homelab build documentation
├── /month-03-security-plus/  Python log analyser script
├── /month-04-soc-siem/       SIEM dashboard screenshot + detection
├── /month-05-ir/             Incident investigation report
├── /month-06-detection/      Sigma rule + YARA rule
├── /month-07-pentest/        Pen test report (from HackTheBox/DVWA)
├── /month-08-web-security/   3 OWASP Top 10 exploitation writeups
├── /month-09-cloud/          Prowler scan before/after remediation
├── /month-10-llm/            RAG app + 3 prompt injection demos
├── /month-11-ai-red-team/    AI red team report
└── /month-12-devsecops/      GitHub Actions security pipeline
```

**2-Page PDF Summary includes:**
1. Your name, LinkedIn, GitHub link
2. Skills matrix: list 15+ specific tools/technologies with proficiency (Beginner/Intermediate/Advanced)
3. Top 3 portfolio highlights (what you're most proud of, what it demonstrates)
4. Certifications earned or in progress
5. Target roles and why you're a fit
6. One paragraph on your AI security specialisation

**LinkedIn Post:** Share your capstone completion, link to GitHub, tag relevant hashtags.

**Marking:**
- GitHub portfolio with all 12 folders and content: 15 marks
- 2-page PDF summary complete: 7 marks
- LinkedIn post published: 3 marks

---

## Rubric

| Task | Full Marks | Good (75%) | Needs Work (50%) |
|------|-----------|------------|-----------------|
| DevSecOps Pipeline | All 3 scans + gate + demo | 2 scans + gate | Basic pipeline only |
| Risk Register | 8 risks + DPDP + supply chain + ISO mapping | 6-7 risks, partial mapping | Incomplete table |
| Hands-on tools | All 3 exercises with screenshots | 2 exercises | 1 exercise |
| Capstone portfolio | All 12 folders + PDF + LinkedIn | GitHub only, partial | README only |
