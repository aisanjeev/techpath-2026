# Cheat Sheet — DevSecOps, GRC & Capstone

**Month 12 | Quick Reference Card**

---

## DevSecOps Tool Reference

| Tool | Category | Free? | Command |
|------|----------|-------|---------|
| **Semgrep** | SAST | Yes | `semgrep --config=auto .` |
| **SonarQube** | SAST | OSS | `sonar-scanner` (CI plugin) |
| **OWASP ZAP** | DAST | Yes | `zap-full-scan.py -t https://target` |
| **Trivy** | SCA + Secrets | Yes | `trivy fs . --security-checks vuln,secret` |
| **Snyk** | SCA | Free tier | `snyk test` |
| **TruffleHog** | Secret scanning | Yes | `trufflehog git https://github.com/...` |
| **Checkov** | IaC scan | Yes | `checkov -d ./terraform` |
| **Cosign** | Image signing | Yes | `cosign sign image:tag` |

---

## GitHub Actions Security Pipeline

```yaml
name: Security Pipeline
on: [push, pull_request]
jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Semgrep
        run: pip install semgrep && semgrep --config=auto . --error

  sca:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Trivy SCA
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
          severity: HIGH,CRITICAL
          exit-code: 1

  secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: {fetch-depth: 0}
      - name: TruffleHog Scan
        uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified
```

---

## GRC Framework Quick Reference

| Framework | Type | Who it's for | Key output |
|-----------|------|-------------|------------|
| **ISO 27001** | International cert | Any org handling data | ISMS + Certification |
| **SOC 2** | US audit | SaaS / cloud companies | Type I or II Report |
| **NIST CSF 2.0** | US framework | Government, enterprises | Identify/Protect/Detect/Respond/Recover |
| **DPDP Act** | India law | Any org processing Indian personal data | Compliance program |
| **GDPR** | EU law | Any org with EU data subjects | DPA, privacy notices |
| **PCI-DSS** | Industry standard | Orgs handling card payments | Compliance report |
| **HIPAA** | US law | Healthcare orgs | Privacy/security rules |

---

## Risk Score Matrix

```
Impact →  1      2      3      4      5
         Low   Minor  Mod   Major  Crit
   5 Alm  5     10     15    20    25  ← CRITICAL
   4 Like 4      8     12    16    20  ← HIGH
   3 Poss 3      6      9    12    15  ← MEDIUM
   2 Unl  2      4      6     8    10  ← LOW
   1 Rare 1      2      3     4     5  ← VERY LOW
↑
Likelihood
```
Risk Score 15-25 → Immediate action required
Risk Score 8-12 → High priority
Risk Score 4-6 → Medium priority
Risk Score 1-3 → Accept or monitor

---

## NIST CSF 2.0 Functions

| # | Function | Key Questions |
|---|----------|--------------|
| 1 | **GOVERN** | What are our cybersecurity policies and risk appetite? |
| 2 | **IDENTIFY** | What assets do we have? What are the risks? |
| 3 | **PROTECT** | How do we prevent or limit attacks? |
| 4 | **DETECT** | How do we identify when something bad happens? |
| 5 | **RESPOND** | What do we do when an incident occurs? |
| 6 | **RECOVER** | How do we restore operations after an incident? |

---

## Interview Quick Reference

| Question type | Framework to use |
|--------------|-----------------|
| Behavioural | STAR (Situation, Task, Action, Result) |
| Incident scenario | NIST IR lifecycle (Prep→ID→Contain→Eradicate→Recover→Learn) |
| "How would you secure X?" | CIA Triad + Defence in depth |
| Risk question | Likelihood × Impact, Controls, Residual risk |
| "What tools do you use?" | Name 2-3 from your homelab, explain WHY |

---

## Salary Negotiation Anchors (India 2026)

| Role | Experience | Range |
|------|-----------|-------|
| SOC L1 Analyst | 0-1 yr | ₹3.5-6 LPA |
| SOC L2 / Detection Eng | 1-3 yr | ₹6-12 LPA |
| Cloud Security Eng | 2-5 yr | ₹10-22 LPA |
| AI/LLM Security (premium) | 2-4 yr | ₹12-25 LPA |
| Pen Tester | 2-4 yr | ₹8-18 LPA |
| Security Architect | 7+ yr | ₹22-50 LPA |

**Negotiation tip:** Always give a range with your target at the bottom. Research Glassdoor + AmbitionBox + LinkedIn Salary for current market rates.
