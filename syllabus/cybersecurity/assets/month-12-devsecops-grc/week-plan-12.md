# Month 12 — Week-by-Week Study Plan
## DevSecOps, GRC, and Capstone Portfolio

**Total study time: ~80 hours over 4 weeks**

---

## Week 1 — DevSecOps: Integrating Security into the Pipeline

**Goal:** Build a complete security-integrated CI/CD pipeline and understand the DevSecOps toolchain.

### Day 1 — DevSecOps Philosophy and Shift-Left Security
- **Read:** `01-devsecops-pipeline.md` — introduction section
- **"Shift left" means:** Move security testing earlier in the software development lifecycle — ideally before code is even written, and definitely before it reaches production.
- **Cost of finding vulnerabilities at each stage:**
  ```
  Design:      1x cost
  Development: 6x cost
  Testing:     15x cost
  Production:  100x cost
  ```
  Security found in production after exploitation: immeasurable cost (breach, legal, reputation)

- **DevSecOps maturity levels:**
  
  **Level 0 (No security):** Security reviewed only before release, if at all
  **Level 1 (Basic):** Dependency scanning in CI, SAST on main branch
  **Level 2 (Integrated):** SAST + DAST + SCA on every PR, secrets scanning, security gates
  **Level 3 (Advanced):** Automated threat modelling, IaC scanning, supply chain verification, runtime protection, security metrics in engineering KPIs

- **Tools overview (each has a free/open-source option):**
  ```
  Secret scanning: TruffleHog, Gitleaks, GitHub Secret Scanning
  SAST (code analysis): Semgrep, CodeQL, Bandit (Python), Brakeman (Ruby)
  SCA (dependency vulns): Trivy, Snyk, OWASP Dependency-Check
  DAST (runtime testing): OWASP ZAP, Nuclei
  Container scanning: Trivy, Grype, Clair
  IaC scanning: Checkov, tfsec, KICS
  Supply chain: SLSA, SBOM (CycloneDX, SPDX)
  ```

### Day 2 — SAST: Static Analysis in Practice
- **Semgrep — the most versatile SAST tool (free, open-source):**
  ```bash
  pip install semgrep
  
  # Scan a directory with default security rules
  semgrep --config=auto ./my-project/
  
  # Use specific rule sets
  semgrep --config=p/python ./app/          # Python security rules
  semgrep --config=p/django ./app/          # Django-specific rules
  semgrep --config=p/javascript ./frontend/ # JavaScript rules
  semgrep --config=p/owasp-top-10 ./       # OWASP Top 10 coverage
  
  # Scan and output to JSON for CI/CD
  semgrep --config=auto --json ./app/ > semgrep-results.json
  
  # Write a custom Semgrep rule
  cat > my-rules.yaml << 'EOF'
  rules:
    - id: hardcoded-password-in-config
      patterns:
        - pattern: PASSWORD = "..."
        - pattern: password = "..."
        - pattern: api_key = "..."
      message: Hardcoded credential found. Use environment variables or secrets manager.
      severity: ERROR
      languages: [python, javascript]
  EOF
  semgrep --config=my-rules.yaml ./app/
  ```

- **Bandit — Python-specific security scanner:**
  ```bash
  pip install bandit
  
  bandit -r ./app/                # Recursive scan
  bandit -r ./app/ -l             # Low severity too
  bandit -r ./app/ -f json        # JSON output
  bandit -t B101,B102 ./app/      # Test specific rules only
  
  # Common Bandit findings:
  # B101: assert used in non-test code (can be optimised away)
  # B301: pickle.loads — arbitrary code execution risk
  # B501-B506: SSL/TLS settings (version, verify, cert issues)
  # B601-B608: Shell injection risks, SQL injection
  ```

### Day 3 — SCA: Dependency Vulnerability Scanning
- **Trivy — comprehensive container and dependency scanner:**
  ```bash
  # Install Trivy
  curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh
  
  # Scan a Docker image
  trivy image python:3.11-slim
  trivy image --severity HIGH,CRITICAL nginx:1.24
  
  # Scan a filesystem (requirements.txt, package.json, etc.)
  trivy fs ./my-project/
  
  # Scan a git repository
  trivy repo https://github.com/your-org/your-app
  
  # SBOM generation (Software Bill of Materials)
  trivy image --format cyclonedx --output sbom.json python:3.11-slim
  
  # Scan for IaC misconfigurations
  trivy config ./terraform/
  ```
- **OWASP Dependency-Check (Java/JavaScript/Python):**
  ```bash
  # For Python
  pip-audit ./requirements.txt    # Simple pip audit
  
  # For Node.js
  npm audit
  npm audit --json > audit-results.json
  
  # Full OWASP DC (Java-based, more thorough)
  dependency-check.sh --scan ./project/ --format JSON --out ./reports/
  ```

### Day 4 — Secrets Scanning
- **Why secrets in git are catastrophic:** Once pushed to GitHub, secrets are visible in the git history even if deleted in a subsequent commit. GitHub automatically notifies affected service providers.
- **TruffleHog:**
  ```bash
  pip install trufflehog3
  
  # Scan a local git repository
  trufflehog git file://./my-repo/
  
  # Scan GitHub organisation (requires token)
  trufflehog github --org=myorganisation --token=$GITHUB_TOKEN
  
  # Scan only recent commits (for CI)
  trufflehog git --since-commit HEAD~5 file://./my-repo/
  ```
- **Gitleaks:**
  ```bash
  # Install
  brew install gitleaks   # Mac
  # Or download binary from github.com/gitleaks/gitleaks/releases
  
  gitleaks detect --source=./my-repo/          # Scan local repo
  gitleaks detect --source=./my-repo/ --report-format json --report-path leaks.json
  
  # Pre-commit hook (prevents committing secrets)
  # Add to .pre-commit-config.yaml:
  # - repo: https://github.com/gitleaks/gitleaks
  #   rev: v8.18.4
  #   hooks:
  #     - id: gitleaks
  ```

### Day 5 — Building a GitHub Actions Pipeline
- **Complete `lab-12-a.json`** — all 5 steps
- **Build a complete GitHub Actions DevSecOps pipeline:**
  ```yaml
  # .github/workflows/security.yml
  name: Security Pipeline
  
  on: [push, pull_request]
  
  jobs:
    secret-scan:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
          with:
            fetch-depth: 0   # Full history for secret scanning
        - name: TruffleHog Secrets Scan
          uses: trufflesecurity/trufflehog@main
          with:
            base: main
            head: HEAD
            extra_args: --only-verified
    
    sast:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Semgrep SAST
          uses: returntocorp/semgrep-action@v1
          with:
            config: >-
              p/python
              p/owasp-top-10
          env:
            SEMGREP_APP_TOKEN: ${{ secrets.SEMGREP_APP_TOKEN }}
    
    dependency-scan:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - name: Trivy SCA + Container Scan
          uses: aquasecurity/trivy-action@master
          with:
            scan-type: 'fs'
            format: 'sarif'
            output: 'trivy-results.sarif'
            severity: 'HIGH,CRITICAL'
        - name: Upload to GitHub Security tab
          uses: github/codeql-action/upload-sarif@v3
          with:
            sarif_file: trivy-results.sarif
  
    security-gate:
      needs: [secret-scan, sast, dependency-scan]
      runs-on: ubuntu-latest
      steps:
        - name: Block PR if any security job failed
          if: ${{ failure() }}
          run: exit 1
  ```

---

## Week 2 — GRC: Governance, Risk, and Compliance

**Goal:** Master the GRC frameworks used in real organisations.

### Day 6 — ISO 27001: Building an ISMS
- **Read:** `02-grc-frameworks.md` — ISO 27001 section
- **ISO 27001 ISMS (Information Security Management System):**
  - A systematic approach to managing sensitive company information
  - Uses the PDCA (Plan-Do-Check-Act) cycle
  - Certification requires a third-party audit

- **The 4 mandatory phases:**
  1. **PLAN:** Define scope, risk assessment methodology, statement of applicability
  2. **DO:** Implement controls from Annex A based on risk
  3. **CHECK:** Measure effectiveness, internal audits, management review
  4. **ACT:** Correct non-conformities, continuously improve

- **ISO 27001:2022 Annex A — 93 controls across 4 themes:**
  - 5.x — Organisational Controls (37 controls): policies, roles, supplier management
  - 6.x — People Controls (8 controls): screening, awareness, remote working
  - 7.x — Physical Controls (14 controls): physical access, equipment security
  - 8.x — Technological Controls (34 controls): access control, encryption, development

- **Statement of Applicability (SoA):** Document declaring which Annex A controls apply, why, and whether implemented. Mandatory for certification.

### Day 7 — SOC 2 and DPDP Act
- **SOC 2 (System and Organisation Controls):**
  - American standard for service organisations (SaaS companies especially)
  - 5 Trust Service Criteria: Security, Availability, Processing Integrity, Confidentiality, Privacy
  - Type I: Controls designed correctly at a point in time
  - Type II: Controls operating effectively over 6-12 months (much stronger)
  - Indian SaaS companies selling to US enterprises often need SOC 2

- **DPDP Act 2023 (Digital Personal Data Protection Act, India):**
  ```
  Key definitions:
  - Data Fiduciary: organisation that collects/processes personal data
  - Data Principal: individual whose data is being processed
  - Consent: must be free, specific, informed, unconditional, revocable
  
  Key obligations for Data Fiduciaries:
  - Purpose limitation: collect only for specified, lawful purpose
  - Data minimisation: collect only what's necessary
  - Accuracy: maintain accurate data
  - Storage limitation: don't retain longer than necessary
  - Security safeguards: implement appropriate technical/organisational measures
  - Data Principal rights: right to access, correct, erase, grievance redressal
  
  Penalties:
  - Failure to notify breach: up to ₹200 crore
  - Breach of data principal rights: up to ₹250 crore
  - Non-compliance: up to ₹250 crore
  - Significant Data Fiduciary non-compliance: up to ₹500 crore
  ```

### Day 8 — NIST Cybersecurity Framework 2.0
- **NIST CSF 2.0 has 6 functions (added GOVERN in 2024):**
  
  **GOVERN (new in 2.0):** Organisational context, risk management strategy, supply chain risk
  **IDENTIFY:** Asset management, business environment, risk assessment
  **PROTECT:** Identity management, awareness training, data security, processes
  **DETECT:** Anomalies and events, continuous monitoring, detection processes
  **RESPOND:** Response planning, communications, analysis, mitigation
  **RECOVER:** Recovery planning, improvements, communications

- **CSF Implementation Tiers:**
  - Tier 1 Partial: Ad hoc, limited awareness
  - Tier 2 Risk Informed: Risk-aware but not org-wide
  - Tier 3 Repeatable: Formal policies, risk management
  - Tier 4 Adaptive: Predictive, adaptive, continuous improvement

- **CSF Profiles:** Current profile (what you're doing now) vs Target profile (where you want to be) → gap = your security roadmap

### Day 9 — Risk Management
- **Complete `lab-12-b.json`** — all 5 steps
- **Risk = Likelihood × Impact. Build a risk register:**
  ```python
  # Risk scoring
  LIKELIHOOD_SCORES = {1: "Rare", 2: "Unlikely", 3: "Possible", 4: "Likely", 5: "Almost Certain"}
  IMPACT_SCORES = {1: "Negligible", 2: "Minor", 3: "Moderate", 4: "Major", 5: "Catastrophic"}
  
  def risk_level(likelihood: int, impact: int) -> str:
      score = likelihood * impact
      if score >= 15: return "Critical"
      elif score >= 10: return "High"
      elif score >= 6:  return "Medium"
      else:             return "Low"
  
  # Example risk register
  risks = [
      {
          "id": "R001",
          "description": "Phishing attack leading to account compromise",
          "likelihood": 4,   # Likely
          "impact": 4,        # Major (customer data breach)
          "score": 16,
          "level": "Critical",
          "control": "MFA on all accounts, phishing simulation training",
          "owner": "CISO",
          "review_date": "2024-06-01"
      },
  ]
  ```

### Day 10 — Building a GRC Programme from Scratch
- **12-month GRC roadmap for a startup:**
  
  **Month 1-3 (Foundation):**
  - Asset inventory: what do we have?
  - Risk assessment: what are the biggest risks?
  - Write basic policies: Information Security Policy, Acceptable Use, Incident Response
  - Enable MFA on all systems
  - Set up audit logging
  
  **Month 4-6 (Controls):**
  - Implement controls for top 10 risks
  - Vendor security assessment for critical suppliers
  - Security awareness training for all staff
  - Penetration test
  
  **Month 7-9 (Monitoring):**
  - SIEM for log monitoring
  - Vulnerability management programme
  - Business Continuity Plan (BCP) and Disaster Recovery Plan (DRP)
  - First tabletop exercise
  
  **Month 10-12 (Certification Prep):**
  - Gap analysis against ISO 27001 or SOC 2
  - Internal audit
  - External audit (for certification)

---

## Week 3 — Capstone: Integration and Career Readiness

### Day 11 — The Security Engineer Career Path
- **Career paths from this curriculum:**
  ```
  Penetration Tester / Ethical Hacker (Months 7-8 skills)
  → Entry: Junior PT → Mid: Penetration Tester → Senior: Red Team Lead → Principal: Red Team Architect
  
  SOC Analyst / Detection Engineer (Months 4, 6 skills)
  → Entry: L1 SOC Analyst → Mid: L2/Detection Engineer → Senior: Threat Hunter → 
    Principal: Security Operations Manager
  
  Cloud Security Engineer (Month 9 skills)
  → Entry: Cloud Security Analyst → Mid: Cloud Security Engineer → 
    Senior: Cloud Security Architect → Principal: CISO
  
  AI Security Researcher (Months 10-11 skills)
  → Entry: AI Security Analyst → Mid: AI Red Team Engineer → 
    Senior: AI Safety Researcher → Principal: Head of AI Security
  
  GRC Analyst / Manager (Month 12 skills)
  → Entry: GRC Analyst → Mid: Information Security Manager → 
    Senior: CISO → Principal: VP Information Security
  ```

### Day 12 — Professional Certifications Roadmap
- **Certifications by career path and level:**
  
  **Entry Level (Year 1-2):**
  - CompTIA Security+ — fundamental, vendor neutral
  - Google Cybersecurity Certificate — good for beginners
  - AWS Cloud Practitioner → AWS Security Specialty
  
  **Mid Level (Year 2-4):**
  - CEH (Certified Ethical Hacker) — offensive security recognition
  - **OSCP (Offensive Security Certified Professional)** — industry gold standard for pen testing; requires hacking 5 machines in 24 hours
  - GCIA, GCIH, GCDA — GIAC/SANS for detection and incident response
  
  **Senior Level (Year 4+):**
  - CISSP — gold standard for security leadership
  - CISM — security management focused
  - CRISC — risk management focused
  - ISO 27001 Lead Implementer/Auditor — for GRC roles
  
  **Specialist:**
  - eCPPT, eWPT — eLearnSecurity affordable alternatives to OSCP
  - BTL1 (Blue Team Level 1) — excellent for SOC/detection engineers
  - CDPSE — data privacy specialist

### Day 13 — Building Your Cybersecurity Portfolio
- **Portfolio structure (GitHub + LinkedIn):**
  ```
  GitHub: github.com/yourname
  ├── detection-content/       (Sigma rules, YARA rules — Month 6)
  ├── pentest-reports/         (Anonymous reports from lab work — Month 7-8)
  ├── ir-playbooks/            (IR and forensics work — Month 5)
  ├── cloud-security-scripts/  (AWS/Azure automation — Month 9)
  ├── llm-security/            (Garak tests, injection demos — Month 10-11)
  ├── devsecops-pipeline/      (GitHub Actions templates — Month 12)
  └── writeups/                (CTF writeups, blog posts)
  
  LinkedIn:
  - Update headline: "Security Analyst | SOC & Detection Engineering | CEH"
  - Add all certifications as you earn them
  - Post: 1 technical article per month (share CTF writeup, share a detection rule)
  - Engage with cybersecurity community (comment on posts, share relevant news)
  ```

### Day 14 — Interview Preparation
- **Technical interview questions by domain:**
  
  **SOC/Detection:**
  - "Walk me through your incident triage process when you receive an AV alert"
  - "Write a Splunk SPL query to detect brute force login attempts"
  - "Explain the difference between SIEM and EDR"
  
  **Pen Testing:**
  - "How would you approach a black-box web application pentest?"
  - "Explain how SQL injection works and how to test for it safely"
  - "You have a low-privilege shell on a Linux machine — how do you escalate?"
  
  **Cloud Security:**
  - "What is the AWS Shared Responsibility Model?"
  - "How would you respond to an alert that an access key was leaked in a public repo?"
  - "Explain the principle of least privilege in the context of IAM"
  
  **GRC:**
  - "What is the difference between ISO 27001 and SOC 2?"
  - "How would you conduct a risk assessment for a cloud-based SaaS company?"
  - "Explain the DPDP Act requirements and penalties"
  
  **Behavioural:**
  - "Describe a time you found a security vulnerability — what did you do?"
  - "How do you stay current with the rapidly evolving threat landscape?"
  - "Describe a situation where you had to communicate a technical security risk to a non-technical stakeholder"

### Day 15 — Review and Final Exercises
- **Complete:** `exercises-12.md` questions 1-15
- **Capstone reflection:** Write a 1-page summary of your 12 months:
  - What are your strongest skills?
  - Which area interested you most?
  - What certifications will you pursue first?
  - What job title are you targeting?
  - What is your 12-month career plan from here?

---

## Week 4 — Capstone, Final Assessment, and Career Launch

### Day 16-17 — Capstone Project Part 1: Technical
- **Complete a full security assessment of a vulnerable practice environment:**
  - Use DVWA, TryHackMe, or HackTheBox
  - Write a professional pentest report (Day 16)
  - Conduct a mock SOC investigation (Day 17)
  - Document everything as if submitting to a real client

### Day 18-19 — Capstone Project Part 2: Career Assets
- **Day 18 — Portfolio completion:**
  - Ensure all 12 months of work is on GitHub
  - LinkedIn profile fully updated with projects, skills, certifications
  - Clean up and polish the best 5 portfolio items

- **Day 19 — Job search launch:**
  - Apply to 3 entry-level/junior cybersecurity roles
  - Search: "Junior SOC Analyst", "Security Analyst L1", "Information Security Analyst"
  - Platforms: LinkedIn, Naukri.com, Instahyre (India), Indeed
  - Also look at: startup cybersecurity roles (often more learning, less formal requirements)

### Day 20 — Final Assessment + Certification
- **Complete:** `exercises-12.md` questions 16-25
- **Quiz:** `quiz-12.json` — all 15 questions
- **Final Competency Checklist — 12 Month Mastery:**
  - [ ] Networks & Protocol: Explain TCP/IP, OSI model, DNS, TLS from memory with security implications
  - [ ] OS Security: Investigate a compromised Linux/Windows host; find malware evidence
  - [ ] Cryptography: Explain AES, RSA, SHA-256, certificates, PKI
  - [ ] SOC Operations: Triage an alert from detection through escalation
  - [ ] SIEM: Write Splunk SPL and Microsoft Sentinel KQL for 3 different detections
  - [ ] Incident Response: Lead a tabletop exercise for ransomware
  - [ ] Digital Forensics: Run Volatility3 and interpret memory forensics results
  - [ ] Detection Engineering: Write Sigma and YARA rules from scratch
  - [ ] SOAR: Build a 5-step phishing triage playbook
  - [ ] Ethical Hacking: Conduct reconnaissance → exploitation on a lab target
  - [ ] Web Security: Manually exploit SQLi and XSS in DVWA
  - [ ] Cloud Security: Audit an AWS account with Prowler and fix findings
  - [ ] LLM Security: Explain OWASP LLM Top 10 and conduct prompt injection testing
  - [ ] AI Red Teaming: Run Garak and write an AI red team finding report
  - [ ] DevSecOps: Build a GitHub Actions pipeline with SAST, SCA, secrets scanning
  - [ ] GRC: Write a risk register and map risks to ISO 27001 controls
  - [ ] Career: Resume updated, GitHub portfolio live, first job applications sent
