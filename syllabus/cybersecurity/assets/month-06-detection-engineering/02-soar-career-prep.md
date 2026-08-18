# SOAR, Automation & Career Preparation

## Security Orchestration, Automation and Response (SOAR)

A modern SOC drowns in alerts. The average L1 analyst handles 400+ alerts per day and closes them in minutes — leaving no time for real investigation. SOAR solves this by automating the repetitive, rules-based parts of triage so analysts can focus on what matters.

**What SOAR does:**
- **Orchestration** — Connects disparate security tools (SIEM, EDR, ticketing, threat intel, firewalls)
- **Automation** — Runs playbooks automatically when an alert fires
- **Response** — Takes automated actions (block IP, quarantine host, reset password)

---

## SOAR Architecture

```
Alert Source (SIEM)
        ↓
SOAR Platform receives alert
        ↓
Playbook triggered automatically
        ↓
Enrichment (check IPs, hashes, domains against threat intel)
        ↓
Decision (Is this malicious? High confidence? Low confidence?)
        ↓
Automated Action OR Human handoff with context
        ↓
Case management (ticket created, evidence attached)
        ↓
Notification (analyst, manager, or affected user)
```

---

## Common SOAR Playbooks

### Phishing Triage Playbook (most common L1 task)

```
TRIGGER: Email reported as phishing by user
  ↓
EXTRACT: Sender IP, sender email domain, URLs, attachments
  ↓
ENRICH:
  - Check sender IP on AbuseIPDB
  - Check URLs on VirusTotal
  - Check domain age (new domains = suspicious)
  - Check email headers for spoofing
  ↓
SCORE: Calculate risk score (0-100)
  ↓
IF score > 70:
  - Quarantine email from ALL mailboxes
  - Block sender domain on email gateway
  - Create HIGH priority ticket
  - Notify affected user: "This was malicious, don't click"
  - Notify SOC manager
ELSE IF score 30-70:
  - Create MEDIUM ticket for analyst review
  - Tag email for investigation
ELSE:
  - Close as low risk
  - Update user: "This appears safe"
```

### Brute Force Response Playbook

```
TRIGGER: > 10 failed logins from same IP in 5 minutes
  ↓
IDENTIFY: Is IP internal (RFC1918) or external?
  ↓
IF external:
  - Check IP reputation (AbuseIPDB, VirusTotal)
  - IF malicious → automatically block at firewall
  - Create ticket with evidence
  - Notify SOC analyst
  ↓
IF internal:
  - Escalate immediately (could be insider threat / infected host)
  - Do NOT auto-block (could lock out legitimate user)
  - Notify both SOC and IT
  - Check if IP is a service account (even higher risk)
  ↓
MONITOR: If same IP successfully logs in later → escalate to P1 incident
```

---

## SOAR Platforms Comparison

| Platform | Type | Notes |
|----------|------|-------|
| **Shuffle** | Open source / free cloud tier | Best for learning — visual workflow builder |
| **Tines** | Free community tier | No-code, professional quality |
| **Splunk SOAR** (Phantom) | Enterprise paid | Industry standard, powerful |
| **Palo Alto XSOAR** | Enterprise paid | Feature-rich, complex |
| **Microsoft Sentinel + Logic Apps** | Azure native | Good if already on Azure |
| **TheHive + Cortex** | Open source | Strong IR case management |

**For learning:** Shuffle or Tines community tier — both have drag-and-drop workflow builders and free API integrations.

---

## Reporting — Writing for Non-Technical Audiences

One of the most underrated SOC skills: translating technical findings into business language.

### What executives need to know:
- **What happened** — in plain English, not CVE numbers
- **Who/what was affected** — business systems, customer data, operations
- **How severe** — business risk, not CVSS scores
- **What we did** — actions taken and timeline
- **What you should approve** — recommended investments, policy changes

### Executive Summary Template

```
INCIDENT SUMMARY — [Date] — [Severity: HIGH/MEDIUM/LOW]

WHAT HAPPENED
On [date], our security monitoring detected [plain-English description].
The attacker [what they did, in simple terms].

IMPACT
- [X] customer records potentially exposed
- [Y] systems affected
- [Z] hours of downtime

ACTIONS TAKEN
- Detected at [time], contained at [time]
- [Specific actions: systems isolated, passwords reset, etc.]

CURRENT STATUS
[Contained/Under investigation/Resolved]

RECOMMENDED NEXT STEPS (requires your approval)
1. [Action] — Cost: [£X] — Risk if not done: [description]
2. [Action] — Cost: [£X] — Risk if not done: [description]
```

---

## SOC Interview Preparation

### Common Technical Questions

**Q: Walk me through how you'd investigate a phishing alert.**
A structure: Triage (is it real?) → Enrich (what data is attached?) → Scope (who else got it?) → Contain (quarantine) → Remediate → Document.

**Q: What is the MITRE ATT&CK framework and how do you use it?**
A: Structured knowledge base of adversary tactics and techniques. In SOC work, I use it to map alert activity to specific TTPs, identify gaps in our detection coverage, and communicate threat context to the team.

**Q: Explain the difference between a virus and a worm.**
A: A virus requires a user to execute an infected file to spread. A worm self-propagates across networks without user action.

**Q: What would you do if you found a backdoor on a production server?**
A: 1. Don't tip off the attacker — observe first if safe to do so. 2. Isolate the host from network. 3. Preserve evidence (memory dump, disk image). 4. Notify incident lead. 5. Investigate scope — is this one host or many? 6. Eradicate and recover from clean backup.

### Behavioural Questions

- **Tell me about a time you handled pressure** — Use STAR method, reference a homelab incident or CTF under time pressure
- **How do you stay current in cybersecurity?** — Mention specific resources: Dark Reading, Krebs, specific Twitter/LinkedIn follows, CTFs, certifications in progress
- **Why cybersecurity?** — Be genuine — what specific moment or interest pulled you toward security?

### Portfolio Walk-Through Tips

Be ready to explain every artefact in your portfolio:
- Why you chose the tool/approach
- What you learned from it
- What you'd do differently
- How it applies to the job you're applying for

---

## Career Milestones After Month 6

| Month 6 Status | You're ready for: |
|----------------|------------------|
| Security+ ✓ | Apply for L1 SOC Analyst, Security Associate |
| Homelab documented | Show employers you self-study |
| SIEM dashboard screenshot | Demonstrate hands-on tool experience |
| Incident report written | Prove you can communicate findings |
| Detection rules on GitHub | Show detection engineering initiative |

**Salary range after Month 6 (India 2026):** ₹3.5–6 LPA for L1 SOC roles. With internship or 1 year experience → ₹5–8 LPA.
