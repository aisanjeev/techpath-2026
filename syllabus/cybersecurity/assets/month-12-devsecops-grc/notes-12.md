# Month 12 — DevSecOps, GRC & Capstone — Quick Revision Notes

---

## DevSecOps — Shift Security Left

**Core idea:** Find and fix vulnerabilities as early as possible in the SDLC — code review is cheaper than a breach.

```
Code → Commit → Build → Test → Deploy → Monitor
 ↑        ↑       ↑       ↑       ↑        ↑
Secret  SAST/  Dep scan  DAST  Security  Runtime
scan    lint            check   gates   monitoring
```

### SAST — Static Application Security Testing
- Analyses source code WITHOUT running it
- Finds: SQL injection, hardcoded credentials, XSS, buffer overflows, insecure crypto
- Tools: **Semgrep** (free, fast), **SonarQube** (OSS + paid), **CodeQL** (GitHub, free for OSS)
- When: Run on every pull request, block merges on HIGH/CRITICAL findings

### DAST — Dynamic Application Security Testing
- Tests the RUNNING application from outside, like an attacker would
- Finds: runtime injection flaws, auth issues, business logic bugs SAST misses
- Tools: **OWASP ZAP** (free), **Burp Suite Enterprise** (paid CI/CD integration)
- When: Run in staging environment after deployment

### SCA — Software Composition Analysis
- Scans open-source dependencies for known CVEs
- Finds: vulnerable npm/pip/Maven packages (e.g., Log4Shell came from Log4j dependency)
- Tools: **Trivy** (free, fast), **Snyk** (free tier), **Dependabot** (GitHub built-in)
- When: On every build AND continuously as new CVEs are published

### Secrets Management
- **Never** commit secrets (API keys, passwords, tokens) to Git
- Use: **HashiCorp Vault**, **AWS Secrets Manager**, **Azure Key Vault**, **GitHub Secrets**
- Detect leaks: **git-secrets**, **TruffleHog**, **GitGuardian**
- If a secret is committed: rotate it IMMEDIATELY — assume it's compromised

### Supply Chain Security
- **SLSA (Supply chain Levels for Software Artifacts)** — framework for build provenance
- **SBOM (Software Bill of Materials)** — list of all components in your software
- **Signed commits** — `git commit -S` with GPG key — proves who wrote the code
- **Dependency confusion attacks** — attacker publishes malicious package with same name as internal package

---

## GRC — Governance, Risk & Compliance

### ISO 27001
- International standard for an **Information Security Management System (ISMS)**
- What it covers: risk assessment, policies, controls, access management, incident response, supplier security, business continuity
- Audit process: Gap assessment → Implement controls → Internal audit → Stage 1 (documentation review) → Stage 2 (controls testing) → Certification
- Key document: **Statement of Applicability (SoA)** — lists all Annex A controls and whether they're applied

### SOC 2 (Service Organization Control)
- US standard for SaaS companies — customers ask "are you secure enough to process my data?"
- **5 Trust Service Criteria:** Security, Availability, Processing Integrity, Confidentiality, Privacy
- **Type I** — Point-in-time: "Controls are designed appropriately"
- **Type II** — Period review (6-12 months): "Controls operated effectively over time"
- Almost every enterprise customer will require SOC 2 Type II before signing a contract

### India DPDP Act (Digital Personal Data Protection Act 2023)
| Concept | Meaning |
|---------|---------|
| **Data Fiduciary** | Entity that determines purpose/means of processing (like GDPR controller) |
| **Data Principal** | Individual whose data is processed |
| **Data Processor** | Processes data on behalf of fiduciary |
| **Consent** | Specific, informed, clear consent required before processing |
| **Purpose limitation** | Data used only for stated purpose |
| **Data localisation** | Certain sensitive data must stay in India |
| **Penalties** | Up to ₹250 crore per breach |

### NIST Cybersecurity Framework 2.0 (CSF)
Six functions (GOVERN added in v2.0):
1. **GOVERN** — Establish cybersecurity strategy, policies, roles (new in 2.0)
2. **IDENTIFY** — Asset management, risk assessment
3. **PROTECT** — Access control, training, data security
4. **DETECT** — Monitoring, anomaly detection
5. **RESPOND** — Incident response, communications
6. **RECOVER** — Recovery planning, improvements

### Risk Register
| Column | What it contains |
|--------|----------------|
| Risk ID | Unique identifier |
| Description | What could go wrong |
| Likelihood | 1-5 scale |
| Impact | 1-5 scale |
| Risk Score | L × I |
| Owner | Accountable person |
| Controls | What reduces the risk |
| Residual Risk | Risk score after controls |
| Status | Open/Accepted/Mitigated |

---

## Career Strategy Reminders

- **ATS-friendly resume:** No tables, no headers/footers, use keywords from job description
- **Quantify impact:** "Reduced alert false-positive rate by 40%" not "improved SIEM"
- **LinkedIn headline:** "Cybersecurity Analyst | SOC | SIEM | Cloud Security | Security+"
- **GitHub portfolio:** Always link from LinkedIn featured section
- **Interview prep:** STAR method for behaviourals, draw diagrams for technical questions
