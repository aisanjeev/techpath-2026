# Month 4 — Quick Revision Notes: SOC Operations & SIEM

## SOC Tier Structure

| Tier | Title | Core Responsibilities |
|------|-------|-----------------------|
| L1 | Alert Analyst | Monitor dashboards, initial triage, open/close tickets |
| L2 | IR Analyst | Deep investigation, containment decisions, evidence handling |
| L3 | Senior Analyst | Threat hunting, detection rule authorship, architecture review |
| Manager | SOC Manager | SLA enforcement, metrics reporting, stakeholder communication |

## Alert Triage Workflow (6 Steps)

1. **Receive** — Alert fires in SIEM or EDR console
2. **Enrich** — Gather context: IP reputation, user details, asset classification, prior tickets
3. **Classify** — Assign severity (Critical / High / Medium / Low)
4. **Validate** — True positive (TP) or false positive (FP)?
5. **Act** — TP: escalate/contain; FP: tune rule and close with notes
6. **Document** — Record findings, evidence hash, timeline, and actions taken

## Severity Classification

| Severity | SLA Target | Typical Examples |
|----------|------------|------------------|
| Critical | Immediate | Active ransomware, confirmed data exfiltration in progress |
| High | < 1 hour | Credential dumping, lateral movement, privileged account abuse |
| Medium | < 4 hours | Repeated brute force, suspicious scheduled task creation |
| Low | < 24 hours | Single failed login, policy violation, reconnaissance ping |

## Splunk SPL — Essential Commands

```spl
# Basic search with index and field filter
index=windows EventCode=4625 Account_Name!="-"

# Stats aggregation and sorting
| stats count by Account_Name | sort -count | head 10

# Brute force detection
index=windows EventCode=4625
| stats count by Account_Name, src_ip
| where count > 10

# Time modifier
earliest=-1h latest=now

# Regex field extraction
| rex field=_raw "Process Name:\s+(?P<process>[^\n]+)"

# Lookup table enrichment
| lookup threat_intel_lookup src_ip OUTPUT category, risk_score
```

## Microsoft Sentinel KQL — Essential Syntax

```kql
// Brute force: failed logins > 5 in last hour
SecurityEvent
| where EventID == 4625
| where TimeGenerated > ago(1h)
| summarize FailCount = count() by Account, Computer
| where FailCount > 5
| order by FailCount desc

// New service installation
SecurityEvent
| where EventID == 7045
| project TimeGenerated, Computer, ServiceName, ServiceFileName

// Top denied firewall connections
AzureFirewallApplicationRuleLog
| where Action == "Deny"
| summarize DenyCount = count() by SourceIP
| top 15 by DenyCount
```

## Critical Windows Event IDs

| Event ID | Meaning |
|----------|---------|
| 4624 | Successful logon |
| 4625 | Failed logon |
| 4648 | Explicit credential logon (pass-the-hash indicator) |
| 4688 | New process created |
| 4698 / 4702 | Scheduled task created / modified |
| 4720 / 4726 | User account created / deleted |
| 4732 | Member added to privileged group |
| 7045 | New Windows service installed |
| 1102 | Security audit log cleared |

## MITRE ATT&CK — 14 Tactics

| ID | Tactic | Analyst Question |
|----|--------|-----------------|
| TA0043 | Reconnaissance | How did they gather info before attacking? |
| TA0042 | Resource Development | What infrastructure did they build/buy? |
| TA0001 | Initial Access | How did they first get in? |
| TA0002 | Execution | What code ran on the victim system? |
| TA0003 | Persistence | How do they survive reboots/detection? |
| TA0004 | Privilege Escalation | How did they gain admin/SYSTEM? |
| TA0005 | Defense Evasion | How did they avoid detection? |
| TA0006 | Credential Access | How did they steal passwords/hashes? |
| TA0007 | Discovery | What did they learn about the network? |
| TA0008 | Lateral Movement | How did they spread to other systems? |
| TA0009 | Collection | What data did they gather? |
| TA0011 | Command & Control | How did they communicate back? |
| TA0010 | Exfiltration | How did they send data out? |
| TA0040 | Impact | What damage did they do? |

## ELK Stack Components

| Component | Role |
|-----------|------|
| Elasticsearch | Search and storage engine (JSON documents) |
| Logstash | Log ingestion, parsing, transformation pipeline |
| Kibana | Dashboards, visualisation, alert rules |
| Filebeat | Lightweight file log shipper |
| Winlogbeat | Windows Event Log shipper |

## SOC Key Metrics

- **MTTD** — Mean Time to Detect: hours from attack start to alert fire
- **MTTR** — Mean Time to Respond: hours from detection to remediation
- **False Positive Rate** — FP alerts ÷ total alerts × 100%
- **Dwell Time** — Days attacker was in environment before detection
- **Escalation Rate** — % of L1 tickets escalated to L2/L3

## EDR vs XDR

| Feature | EDR | XDR |
|---------|-----|-----|
| Scope | Endpoints only | Endpoints + network + cloud + identity |
| Data | Process, file, registry | Cross-domain telemetry unified |
| Key Vendors | CrowdStrike Falcon, SentinelOne | Microsoft Defender XDR, Cortex XDR |
| Use Case | Endpoint response | Unified platform detection & response |
