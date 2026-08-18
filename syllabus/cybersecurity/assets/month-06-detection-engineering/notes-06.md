# Month 6 — Quick Revision Notes: Detection Engineering & Job-Ready Skills

## Detection Engineering Overview

Detection engineering is the discipline of creating, testing, tuning, and maintaining detection logic that finds real threats in production environments. It bridges threat intelligence, attacker behaviour, and SIEM capabilities.

**The Detection Lifecycle:**
```
Write → Test → Tune → Deploy → Review → (back to Write)
```

---

## Sigma — Vendor-Neutral Detection Rules

Sigma is a generic, vendor-neutral rule format. Write once, convert to any SIEM.

### Sigma Rule Structure

```yaml
title: Mimikatz via PowerShell
id: abc12345-1234-1234-1234-123456789abc
status: stable
description: Detects Mimikatz credential dumping via PowerShell
references:
  - https://attack.mitre.org/techniques/T1003/001/
author: Your Name
date: 2026/08/01
tags:
  - attack.credential_access
  - attack.t1003.001
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    CommandLine|contains:
      - 'sekurlsa'
      - 'logonPasswords'
      - 'lsadump::sam'
  condition: selection
falsepositives:
  - Security testing / red team exercises
level: high
```

### Converting Sigma Rules

```bash
# Install sigma-cli
pip install sigma-cli

# Convert to Splunk SPL
sigma convert -t splunk -p splunk_windows rule.yml

# Convert to Microsoft Sentinel KQL
sigma convert -t microsoft365defender rule.yml

# Convert to Elastic
sigma convert -t elasticsearch-dsl rule.yml
```

### Sigma Field Reference

| Field | Purpose |
|-------|---------|
| `title` | Human-readable name |
| `id` | UUID for unique identification |
| `status` | `stable`, `test`, `experimental`, `deprecated` |
| `level` | `low`, `medium`, `high`, `critical` |
| `logsource` | `category` + `product` defining what logs it applies to |
| `detection.selection` | Key-value match conditions |
| `detection.filter` | Exclude conditions (AND NOT logic) |
| `detection.condition` | Boolean logic combining selection/filter: `selection and not filter` |
| `falsepositives` | Known FP sources for tuning reference |

---

## YARA — Pattern-Based Malware Detection

YARA matches patterns in files, processes, and memory streams.

### YARA Rule Structure

```yara
rule CobaltStrike_Beacon {
    meta:
        description = "Detects CobaltStrike beacon binary strings"
        author      = "Your Name"
        date        = "2026-08-01"
        reference   = "https://attack.mitre.org/techniques/T1071"

    strings:
        $str1 = "ReflectiveLoader"       ascii
        $str2 = "beacon.x64.dll"         ascii nocase
        $hex1 = { 4D 5A 90 00 03 00 00 00 }  // MZ header
        $re1  = /sleeptime=[0-9]+/        ascii

    condition:
        $hex1 at 0 and any of ($str*, $re1)
}
```

### YARA String Types

| Type | Syntax | Matches |
|------|--------|---------|
| Plain string | `"string"` | Exact ASCII bytes |
| Case-insensitive | `"string" nocase` | Any casing variant |
| Wide string | `"string" wide` | UTF-16LE (Windows) |
| Hex pattern | `{ 4D 5A ?? 00 }` | Hex with `??` wildcard |
| Regex | `/pattern/` | Full regex syntax |

### YARA Condition Logic

```yara
condition:
  all of them           // ALL defined strings must match
  any of them           // ANY one string matches
  2 of ($str*)          // At least 2 of $str1, $str2, $str3...
  $hex1 at 0            // $hex1 found at file offset 0
  filesize < 1MB        // File must be < 1 MB
  uint32(0) == 0x5A4D   // First 4 bytes = MZ header (little-endian)
```

### Running YARA

```bash
# Install
pip install yara-python

# Scan a single file
yara rule.yar suspicious.exe

# Scan a directory recursively
yara -r rule.yar /path/to/scan/

# Scan running processes (requires root/admin)
yara -p rule.yar /proc/*/exe   # Linux
# Use yaraProcScan.py for Windows process scanning
```

---

## Alert Fatigue & Tuning

| Problem | Cause | Solution |
|---------|-------|---------|
| Too many FP alerts | Rule too broad | Add filter conditions, raise threshold |
| Missing real threats | Rule too narrow | Expand selection conditions |
| Alert queue overload | Too many low-value rules | Disable/archive low-efficacy rules |
| Alert blindness | High volume becomes ignored | Reduce total alert count through tuning |

**Tuning Process:**
1. Identify the FP source (which field/value is causing noise)
2. Add a filter block to the Sigma rule: `filter: | field: legitimate_value`
3. Test against historical data before deploying
4. Document the change in the rule's `changelog` field
5. Review impact metrics in the SIEM after 1 week

---

## SOAR Concepts

| Component | Function |
|-----------|---------|
| Trigger | Alert from SIEM/EDR that starts the playbook |
| Enrichment | Automated IOC lookup (VT, AbuseIPDB, MISP) |
| Decision | If/else logic: is this a confirmed threat? |
| Action | Contain (block IP, isolate host, disable account) |
| Notification | Ticket creation, Slack/Teams alert to analyst |
| Case management | Track the incident through resolution |

**Free SOAR platforms:**
- **Tines** (https://www.tines.com) — free community tier, visual workflow builder
- **Shuffle** (https://shuffler.io) — open-source, Docker-deployable

---

## Reporting for Executives

| Audience | Avoid | Use Instead |
|----------|-------|-------------|
| C-Suite | CVE IDs, log excerpts, hex bytes | Business impact in £/$ |
| Board | ATT&CK technique IDs | "Attacker had access to payroll for 4 hours" |
| Technical leads | Vague risk statements | Specific findings with remediation steps |

**Executive Report Structure:**
1. **Headline** — What happened (1 sentence)
2. **Business Impact** — Revenue, data, regulatory exposure
3. **What We Did** — Actions taken (plain English)
4. **Current Status** — Resolved / Contained / Investigating
5. **Top 3 Recommendations** — With estimated effort/cost

---

## CySA+ Exam Quick Facts

| Item | Detail |
|------|--------|
| Full name | CompTIA Cybersecurity Analyst+ |
| Exam code | CS0-003 |
| Questions | 85 (mix of MCQ and performance-based) |
| Duration | 165 minutes |
| Pass mark | 750/900 |
| Validity | 3 years (CE required) |
| Key domains | Threat intelligence, vulnerability management, incident response, reporting |
