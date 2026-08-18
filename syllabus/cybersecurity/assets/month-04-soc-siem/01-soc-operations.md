# SOC Operations: Structure, Triage, and Analyst Workflow

## What Is a SOC?

A Security Operations Centre (SOC) is the team and facility responsible for continuously monitoring an organisation's IT environment, detecting threats, and coordinating response. The SOC is the operational heart of a defensive security programme — it converts raw telemetry (logs, alerts, threat intel) into actions that protect the business.

SOCs range from a single analyst with a Splunk licence to 24/7 multi-tier teams with hundreds of staff. Understanding their structure is essential whether you plan to work in one or design one.

---

## SOC Tier Model

### L1 — Alert Analyst
The first eyes on every alert. L1 analysts work in high-volume, shift-based environments.

**Responsibilities:**
- Monitor SIEM dashboards and EDR consoles
- Perform initial triage: is this alert real?
- Enrich alerts with context (IP reputation, user account details, asset criticality)
- Document findings in the ticketing system (ServiceNow, Jira, etc.)
- Escalate confirmed or uncertain alerts to L2
- Close false positives with documented reasoning

**Typical Ratio:** 1 L2 for every 3-5 L1 analysts

### L2 — Incident Responder
Receives escalations from L1 and conducts deeper investigation.

**Responsibilities:**
- In-depth forensic analysis: log correlation, memory analysis, artifact review
- Determine scope: what systems are affected, what data was accessed
- Execute containment actions: isolate endpoint, block IP, disable account
- Work with asset owners to coordinate remediation
- Write detailed investigation tickets with timeline and evidence
- Feed findings back to L3 for detection rule improvements

### L3 — Senior Analyst / Threat Hunter
The most experienced tier — proactive rather than reactive.

**Responsibilities:**
- Proactive threat hunting using hypothesis-driven methodology
- Writing and tuning SIEM detection rules
- Designing playbooks for common incident types
- MITRE ATT&CK coverage analysis — what are we not detecting?
- Mentoring L1/L2 analysts
- Purple team exercises with red team

### SOC Manager
Operational leadership rather than hands-on technical work.

**Responsibilities:**
- SLA management (MTTD, MTTR, alert closure targets)
- Shift scheduling and staffing
- Metrics reporting to CISO and business stakeholders
- Tool procurement and budget management
- Vendor relationships (MSSP, threat intel providers)

---

## The Alert Lifecycle

```
Alert Generated (SIEM/EDR)
        │
        ▼
L1: Receive & Enrich
  - Pull IP reputation
  - Check user's recent activity
  - Review asset criticality
        │
        ▼
L1: Classify Severity
  Critical / High / Medium / Low
        │
        ├─── False Positive ────► Tune rule → Close ticket
        │
        └─── True Positive ─────► Escalate to L2
                                        │
                                        ▼
                              L2: Deep Investigation
                                - Forensic log review
                                - Memory/disk analysis
                                - Scope determination
                                        │
                                        ▼
                              Contain → Eradicate → Recover
                                        │
                                        ▼
                              Post-Incident Review (L3)
                              Rule tuning, lessons learned
```

---

## Severity Classification and SLA Targets

| Severity | Response SLA | Characteristics |
|----------|-------------|-----------------|
| **Critical** | Immediate (< 15 min) | Active attack in progress; business-impacting; ransom/exfil underway |
| **High** | < 1 hour | Confirmed compromise but contained; privileged account abuse |
| **Medium** | < 4 hours | Suspicious activity requiring investigation; policy violation |
| **Low** | < 24 hours | Informational; single anomalous event; no clear malicious intent |

---

## Alert Enrichment Process

Before classifying an alert, an L1 analyst should gather context from multiple sources:

1. **IP Reputation** — Check VirusTotal, AbuseIPDB, Shodan. Is this IP known malicious?
2. **User Context** — Is this account active? Normal working hours? Any recent password resets?
3. **Asset Criticality** — Is this a domain controller, a developer workstation, or a kiosk?
4. **Historical Activity** — Has this alert fired before for this account/IP? Was it FP?
5. **Threat Intel** — Does this IP/domain appear in current threat feeds?
6. **MITRE ATT&CK** — What technique does this behaviour map to? Is it part of a known campaign?

---

## SOC Metrics and KPIs

| Metric | Formula | Target |
|--------|---------|--------|
| MTTD | Attack start → First detection | < 24 hours (industry avg: 200+ days) |
| MTTR | Detection → Full remediation | < 4 hours for Critical |
| False Positive Rate | FP alerts ÷ total alerts | < 20% |
| Dwell Time | First access → Detection | Minimize — reduce with proactive hunting |
| Ticket Closure Rate | Tickets closed ÷ tickets opened | > 95% within SLA |
| Escalation Rate | L2 escalations ÷ L1 tickets | Monitor — high rate = L1 needs training |

---

## Shift Handover: Best Practices

Shift handovers are a common failure point — critical context gets lost between teams.

**Good handover includes:**
- Open tickets with current status and last action taken
- Any active incidents (even low-severity) and their timelines
- Systems or accounts currently under watch
- False positive patterns tuned during the shift
- Anything "in the back pocket" — not yet alerted but suspicious

**Template:**
```
Shift: 2026-08-03 06:00 – 14:00 | Analyst: J. Smith
OPEN TICKETS: INC-4421 (escalated to L2 at 09:15 – RDP brute force)
FP TUNED: Rule "Sched Task – Office Macros" whitelisted SCCM service
WATCH LIST: 192.168.1.47 – unusual outbound DNS volume since 11:00
NOTES: Pending Sentinel maintenance window 15:00-16:00, expect alert suppression
```

---

## Common SOC Tools

| Category | Common Tools |
|----------|-------------|
| SIEM | Splunk, Microsoft Sentinel, IBM QRadar, Elastic Security |
| EDR/XDR | CrowdStrike Falcon, Microsoft Defender XDR, SentinelOne, Carbon Black |
| Ticketing | ServiceNow, Jira, PagerDuty |
| Threat Intel | VirusTotal, MISP, Recorded Future, AlienVault OTX |
| Communication | Slack, Microsoft Teams (alert integrations) |
| Orchestration (SOAR) | Splunk SOAR, Palo Alto XSOAR, Tines, Shuffle |

---

## Real-World Analyst Day-in-Life (L1)

```
07:30 — Read shift handover notes; check open tickets
07:45 — Open SIEM dashboard; review overnight alert queue
08:00 — Begin triaging top 5 highest-priority alerts
09:00 — Two alerts confirmed TP; escalate to L2 with full notes
10:00 — Attend daily SOC standup (15 min: what's open, what's trending)
10:15 — Continue triaging medium/low queue
12:00 — Lunch; alerts continue — team rotation ensures coverage
13:00 — Assist L2 with log pull for active investigation
14:00 — Write shift handover notes; hand over to incoming analyst
```
