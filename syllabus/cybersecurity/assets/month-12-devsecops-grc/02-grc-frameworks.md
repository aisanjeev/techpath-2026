# Governance, Risk & Compliance (GRC) Frameworks

## What Is GRC?

GRC stands for **Governance, Risk, and Compliance** — the three pillars that let organisations make security decisions systematically rather than reactively.

- **Governance:** Who makes security decisions? What policies exist? What is acceptable risk?
- **Risk:** What could go wrong? How likely? How severe? What controls reduce it?
- **Compliance:** What laws, standards, and contracts must we meet? How do we prove it?

A security team without GRC builds the right walls in the wrong places. GRC answers: *why these walls, how tall, and how do we prove they're standing?*

---

## ISO 27001 — International ISMS Standard

### What It Is

ISO/IEC 27001 is the internationally recognised standard for an **Information Security Management System (ISMS)**. An ISMS is not a product — it's a systematic approach to managing sensitive information so that it remains secure.

Achieving ISO 27001 certification means an accredited third-party auditor has verified that your security controls are designed, implemented, and operating effectively.

### Why It Matters

- Enterprises, banks, and government agencies commonly require ISO 27001 before signing vendor contracts
- It demonstrates a systematic approach (not ad hoc) to security
- Certification is valid for 3 years with annual surveillance audits

### The ISMS Structure (PDCA Cycle)

```
     Plan          →     Do         →     Check        →     Act
 
Establish ISMS:     Implement &       Monitor &           Improve:
Risk assessment,    operate:          review:             Address
security policy,    Controls,         Internal audits,    nonconformities,
risk treatment,     training,         KPIs, management    preventive &
SoA                 procedures        review              corrective action
```

### Annex A Controls — Structure

ISO 27001:2022 Annex A contains **93 controls** in 4 categories:

| Category | Controls | Examples |
|----------|---------|---------|
| **Organisational** (Chap 5) | 37 | Information security policies, threat intelligence, supplier security |
| **People** (Chap 6) | 8 | Background checks, security training, disciplinary process |
| **Physical** (Chap 7) | 14 | Physical entry controls, clear desk, secure disposal |
| **Technological** (Chap 8) | 34 | Vulnerability management, DLP, SIEM, application security |

### Key Documents You Must Produce

| Document | Purpose |
|----------|---------|
| **Risk Register** | Identifies, scores, and tracks all information security risks |
| **Statement of Applicability (SoA)** | Lists all 93 Annex A controls — which apply, which don't, and why |
| **Risk Treatment Plan** | Documents how each accepted risk will be mitigated |
| **Information Security Policy** | Top-level policy signed by executive management |
| **Internal Audit Reports** | Evidence that controls are being checked periodically |
| **Management Review Records** | Documented executive review of ISMS performance |

### Certification Journey

```
1. Gap Assessment (weeks 1-4)
   Compare current state vs ISO 27001 requirements
   Identify all gaps
   
2. Implement Controls (months 2-6)
   Risk assessment & treatment
   Write policies and procedures
   Technical controls implementation
   Staff training
   
3. Internal Audit (month 7)
   Independent audit before external auditor arrives
   Find and fix any remaining gaps
   
4. Stage 1 Audit (month 8)
   Auditor reviews documentation only
   Confirms ISMS is designed correctly
   Issues any non-conformities for Stage 2

5. Stage 2 Audit (month 9)
   Auditor tests if controls actually work
   Interviews staff, samples evidence
   Issues certificate if passed
   
6. Surveillance Audits (years 2-3)
   Annual check that ISMS is maintained
   Recertification every 3 years
```

---

## SOC 2 — Trust Services for SaaS Companies

### What It Is

SOC 2 (Service Organization Control 2) is a US audit framework developed by the American Institute of Certified Public Accountants (AICPA). It's specifically designed for technology and cloud companies.

When a customer asks "is your platform secure enough to store our data?", a SOC 2 Type II report is the answer.

### Five Trust Service Criteria

| Criterion | Questions it answers |
|-----------|---------------------|
| **Security** (mandatory) | Is the system protected against unauthorised access? |
| **Availability** | Is the system available for operation and use as agreed? |
| **Processing Integrity** | Does the system process data completely and accurately? |
| **Confidentiality** | Is sensitive information protected as committed? |
| **Privacy** | Is personal information collected, used, and disclosed correctly? |

Most companies start with Security only. Enterprise contracts in fintech and healthcare often require all 5.

### Type I vs Type II

| | SOC 2 Type I | SOC 2 Type II |
|-|-------------|-------------|
| **Scope** | Point-in-time snapshot | 6-12 month period |
| **What it proves** | Controls are *designed* appropriately | Controls *operated effectively* over time |
| **Time to obtain** | 3-4 months | 12-18 months |
| **Value to customers** | Low-medium | High |

Almost every enterprise SaaS customer will eventually require Type II. Type I is sometimes used to show progress while working toward Type II.

### Common SOC 2 Controls

- Access reviews: evidence that user access lists are reviewed quarterly
- Vendor assessments: documented third-party security reviews
- Penetration testing: annual third-party pen test results
- Incident response: tested IR procedures with evidence of tabletop exercises
- Change management: documented process for code changes and releases
- Encryption: evidence of encryption at rest and in transit
- Logging and monitoring: SIEM alerts, log retention

---

## India — Digital Personal Data Protection (DPDP) Act 2023

### Context

The DPDP Act came into force in 2023 and is India's primary data privacy law. It's broadly similar in intent to Europe's GDPR but adapted for India's context.

### Key Definitions

| Term | Meaning |
|------|---------|
| **Personal Data** | Any data about an identifiable individual (name, phone, email, UID/Aadhaar, PAN, etc.) |
| **Data Principal** | The individual whose data is being processed (the person) |
| **Data Fiduciary** | The entity that decides *why* and *how* data is processed (equivalent to GDPR Controller) |
| **Data Processor** | Processes data on behalf of the Fiduciary (equivalent to GDPR Processor) |
| **Significant Data Fiduciary (SDF)** | Large-scale processors designated by government; extra obligations apply |
| **Consent Manager** | A registered intermediary that manages consent on behalf of Data Principals |

### Core Obligations for Data Fiduciaries

**1. Lawful Processing (Consent)**
Personal data can only be processed with:
- Free, specific, informed, unconditional, and unambiguous consent — OR —
- A "legitimate use" (employment, medical emergency, state functions, legal obligation)

The consent request must:
- Be in English *or* the individual's chosen language
- List the specific purpose clearly
- Allow withdrawal at any time

**2. Purpose Limitation**
Data collected for "billing" cannot be used for "marketing". Each use requires its own consent.

**3. Data Minimisation**
Collect only what is necessary for the stated purpose.

**4. Storage Limitation**
Delete personal data when the purpose is fulfilled or consent is withdrawn.

**5. Data Principal Rights**

| Right | What it means |
|-------|--------------|
| Right to information | Know what data is held, for what purpose |
| Right to correction | Correct inaccurate or incomplete data |
| Right to erasure | Delete personal data when consent is withdrawn |
| Right to grievance redressal | A named point of contact for complaints |
| Right to nominate | Nominate someone to exercise rights after death |

**6. Data Breach Notification**
Notify the Data Protection Board (DPB) and affected individuals "without delay" (specific timeline to be set by rules).

**7. Data Localisation**
The government may designate certain categories of data that must be stored only within India.

### Penalties

| Violation | Maximum Penalty |
|-----------|----------------|
| Failure to protect personal data | ₹250 crore |
| Failure to notify breach | ₹200 crore |
| Breach of children's data provisions | ₹200 crore |
| Non-compliance with DPB orders | ₹150 crore |

### DPDP vs GDPR — Quick Comparison

| Aspect | DPDP Act (India) | GDPR (EU) |
|--------|----------------|---------|
| Consent | Specific, clear | Freely given, specific, informed |
| Legitimate interests | Listed in Act | Broad "legitimate interests" basis |
| Data localization | Possible (government discretion) | No (free flow within EU) |
| Children's age | Under 18 | Under 16 (varies by member state) |
| DPA | Data Protection Board (to be set up) | National DPA (e.g., ICO, CNIL) |
| Extraterritorial? | Yes — any entity offering goods/services to Indians | Yes — any processing of EU residents |

---

## NIST Cybersecurity Framework 2.0

### What Changed from v1.1

The NIST CSF was originally published in 2014 for critical infrastructure and later adopted widely across industries. Version 2.0 (released February 2024) added a sixth function and significantly expanded governance guidance.

**New in v2.0:** The **GOVERN** function, which sits at the centre of all other functions. Key change: security is now explicitly a board-level and executive governance matter, not just a technical team concern.

### The Six Functions

```
                  ┌─────────┐
                  │  GOVERN │ ← New in 2.0
                  │         │   Strategy, policies, risk appetite
                  └────┬────┘
                       │ informs all functions
         ┌─────────────┼─────────────┐
         ↓             ↓             ↓
    IDENTIFY       PROTECT        DETECT
   What assets   How do we     How do we
   do we have?   limit harm?   spot attacks?
         ↓             ↓             ↓
    RESPOND       RECOVER
   What do we    How do we
   do when hit?  bounce back?
```

### Function Details

**GOVERN** (GV)
- Organisational context (who are we, what do we do, what are our risks?)
- Risk management strategy (what risk appetite has the board agreed?)
- Roles and responsibilities (who is accountable for what?)
- Policies (information security policy, acceptable use, vendor security)
- Oversight (how does the board monitor cybersecurity performance?)

**IDENTIFY** (ID)
- Asset Management: inventory of hardware, software, data, cloud services
- Risk Assessment: identify threats, assess likelihood and impact
- Improvement: learning from incidents and exercises

**PROTECT** (PR)
- Identity Management and Access Control (MFA, least privilege, PAM)
- Awareness and Training (phishing simulations, security culture)
- Data Security (encryption, DLP, data classification)
- Platform Security (patch management, configuration hardening)
- Technology Infrastructure Resilience (backups, redundancy)

**DETECT** (DE)
- Continuous Monitoring (SIEM, IDS/IPS, EDR)
- Adverse Event Analysis (alert triage, threat hunting)

**RESPOND** (RS)
- Incident Management (IR plan, roles, communication plan)
- Incident Analysis (root cause, impact assessment)
- Incident Response Reporting (internal, regulatory, customer notification)
- Mitigation (containment, eradication)

**RECOVER** (RC)
- Incident Recovery Plan (recovery time objectives, RTO/RPO)
- Incident Recovery Communication (stakeholder updates)
- Improvements (post-incident review, lessons learned)

### Using the CSF — Tiers and Profiles

**Tiers** describe how mature your cybersecurity practice is:

| Tier | Description |
|------|-------------|
| 1 — Partial | Ad hoc, reactive, no formal risk management |
| 2 — Risk Informed | Risk awareness exists but not consistently applied |
| 3 — Repeatable | Risk management processes formally defined and followed |
| 4 — Adaptive | Adaptive, continuously improving, data-driven decisions |

**Profiles** are customised versions of the CSF for your sector. NIST publishes Community Profiles for healthcare, financial services, manufacturing, etc.

---

## Risk Management — The Core Process

### The Risk Register

Every GRC program centres on a risk register. It documents the identified risks, scores them, assigns owners, and tracks treatment.

**Risk Scoring:**
```
Risk Score = Likelihood × Impact

Likelihood scale:
  1 = Rare (once in 10+ years)
  2 = Unlikely (once in 3-10 years)
  3 = Possible (once in 1-3 years)
  4 = Likely (once per year)
  5 = Almost Certain (multiple times per year)

Impact scale:
  1 = Insignificant (no real harm)
  2 = Minor (limited financial or reputational damage)
  3 = Moderate (requires management attention, limited regulatory exposure)
  4 = Major (significant financial, legal, or reputational damage)
  5 = Critical (existential threat to the organisation)
```

**Heat map:**

```
      Impact →    1      2      3      4      5
Likelihood ↓
    5          5     10     15     20     25 ← CRITICAL
    4          4      8     12     16     20 ← HIGH
    3          3      6      9     12     15 ← MEDIUM
    2          2      4      6      8     10 ← LOW
    1          1      2      3      4      5 ← VERY LOW
```

### Risk Treatment Options

| Option | When to use |
|--------|------------|
| **Mitigate** | Implement controls to reduce likelihood or impact |
| **Transfer** | Cyber insurance, outsource to a managed service provider |
| **Accept** | Risk score is low, or cost of mitigation exceeds expected loss |
| **Avoid** | Stop the activity that creates the risk |

### Residual Risk

After controls are applied, the remaining risk is **residual risk**. Executive management must formally accept residual risk — it's not the security team's decision alone.

---

## GRC in Practice — Putting It Together

### A Compliance Program for a Startup

**Quarter 1 (Foundation):**
- Asset inventory and data classification
- Risk assessment (identify top 10 risks)
- Write information security policy
- Implement quick wins: MFA, password manager, patching schedule

**Quarter 2 (Controls):**
- Implement risk treatment plans
- Vendor security assessments for top 5 suppliers
- Penetration test
- Incident response plan and tabletop exercise

**Quarter 3 (Evidence):**
- Start collecting evidence for SOC 2 (access reviews, logs, training records)
- Internal audit
- Engage external auditor for Stage 1

**Quarter 4 (Certification):**
- Stage 2 audit (SOC 2 or ISO 27001)
- Publish certification to customers
- Start continuous monitoring program

### GRC Tools

| Tool | Type | Cost |
|------|------|------|
| **Vanta** | SOC 2 / ISO 27001 automation | Paid |
| **Drata** | Compliance automation | Paid |
| **Tugboat Logic** | Risk and policy management | Paid |
| **SimpleRisk** | Risk register (open-source) | Free |
| **Eramba** | GRC platform (community edition) | Free |
| **Spreadsheets** | Risk register, SoA | Free — sufficient for small teams |

---

## Career Paths in GRC

GRC is one of the fastest-growing areas in cybersecurity because every company processing data needs compliance expertise.

**Entry roles:**
- **Junior GRC Analyst** — Risk register maintenance, policy writing, evidence collection for audits
- **Compliance Analyst** — Manage specific frameworks (ISO 27001, SOC 2, PCI-DSS)
- **Privacy Analyst** — GDPR/DPDP Act compliance, data mapping, privacy impact assessments

**Senior roles:**
- **GRC Manager** — Lead the compliance program, manage auditors, report to CISO
- **Chief Information Security Officer (CISO)** — Board-level accountability for security posture
- **Data Protection Officer (DPO)** — Mandatory role under GDPR for certain organisations, increasingly required under DPDP Act for Significant Data Fiduciaries

**Key skills:**
- Risk assessment methodology
- Framework knowledge (ISO 27001, SOC 2, NIST, DPDP)
- Evidence collection and audit management
- Policy writing
- Executive communication (present risk in business terms, not technical ones)

**Certifications:**
- CISM (Certified Information Security Manager) — ISACA
- CRISC (Certified in Risk and Information Systems Control) — ISACA
- ISO 27001 Lead Implementer or Lead Auditor — BSI / PECB
- CGEIT (Certified in the Governance of Enterprise IT) — ISACA
- CDPSE (Certified Data Privacy Solutions Engineer) — ISACA
