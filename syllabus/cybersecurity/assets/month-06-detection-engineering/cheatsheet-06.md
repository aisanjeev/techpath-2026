# Month 6 — Cheatsheet: Detection Engineering, SOAR & Reporting

## Sigma Rule Quick Reference

### Rule Skeleton

```yaml
title: <Short descriptive name>
id: <UUID>
status: experimental | test | stable | deprecated
description: <What does this detect?>
references: [<URL>]
author: <Name>
date: <YYYY/MM/DD>
modified: <YYYY/MM/DD>
tags:
  - attack.<tactic>
  - attack.<technique_id>
logsource:
  category: <category>        # process_creation, network_connection, etc.
  product: <product>          # windows, linux, aws, azure, etc.
detection:
  selection:
    <FieldName>|<modifier>: <value>
  filter:
    <FieldName>: <allowed_value>
  condition: selection and not filter
falsepositives: [<FP sources>]
level: low | medium | high | critical
```

### Sigma Field Modifiers

| Modifier | Effect | Example |
|----------|--------|---------|
| `contains` | Field contains string | `CommandLine\|contains: 'mimikatz'` |
| `startswith` | Field starts with | `Image\|startswith: 'C:\Temp'` |
| `endswith` | Field ends with | `Image\|endswith: '.ps1'` |
| `contains\|all` | All strings present | `CommandLine\|contains\|all: ['enc', 'bypass']` |
| `re` | Regex match | `CommandLine\|re: '.*(enc\|EncodedCommand).*'` |
| `base64offset\|contains` | Base64-encoded variant | `CommandLine\|base64offset\|contains: 'IEX'` |

### Sigma Logic Operators

```yaml
condition: selection                     # simple match
condition: selection and not filter      # exclude FP
condition: 1 of selection*              # any of: selection1, selection2...
condition: all of filter*               # all filter variants
condition: selection1 or selection2     # either matches
```

### Common Sigma Log Sources

| category | product | Log Type |
|----------|---------|----------|
| `process_creation` | `windows` | Sysmon EID 1 / Windows EID 4688 |
| `network_connection` | `windows` | Sysmon EID 3 |
| `dns_query` | `windows` | Sysmon EID 22 |
| `image_load` | `windows` | Sysmon EID 7 |
| `file_event` | `windows` | Sysmon EID 11 |
| `registry_set` | `windows` | Sysmon EID 13 |
| `webserver` | `apache` | Apache access log |

---

## YARA Rule Quick Reference

### Rule Skeleton

```yara
rule <RuleName> {
    meta:
        description = "<what it detects>"
        author      = "<name>"
        date        = "<YYYY-MM-DD>"
        hash        = "<sample SHA256>"

    strings:
        $s1  = "plaintext string"  ascii
        $s2  = "wide string"       wide nocase
        $h1  = { 4D 5A 90 00 }
        $r1  = /regex_pattern/

    condition:
        <boolean expression>
}
```

### YARA Condition Building Blocks

| Expression | Meaning |
|------------|---------|
| `all of them` | Every string must match |
| `any of them` | At least one string matches |
| `2 of ($str*)` | At least 2 strings matching prefix `$str` |
| `$s1 at 0` | `$s1` found at offset 0 (file start) |
| `$s1 in (0..100)` | `$s1` found in first 100 bytes |
| `uint32(0) == 0x5A4D` | First 4 bytes equal MZ magic |
| `filesize < 500KB` | File smaller than 500 KB |
| `pe.entry_point` | PE entry point (requires `import "pe"`) |

### YARA Modules

```yara
import "pe"          // PE header inspection
import "hash"        // MD5/SHA hash computation
import "math"        // Entropy calculation (packed/encrypted)
import "dotnet"      // .NET assembly inspection
```

---

## Detection Lifecycle Reference

| Stage | Action | Tool |
|-------|--------|------|
| Write | Author Sigma or YARA rule | Text editor + Sigma spec |
| Test | Run against known-good and attack data | Uncoder.io, SIEM test index |
| Convert | Output to target platform syntax | sigma-cli / pySigma |
| Deploy | Push rule to production SIEM | Splunk API, Sentinel ARM template |
| Monitor | Watch FP rate and volume for 1 week | SIEM dashboard |
| Tune | Add filters, adjust thresholds | PR to detection-rules repo |
| Review | Quarterly review of all active rules | Rule efficacy report |

---

## SOAR Playbook Building Blocks

| Block Type | Free Tool | Purpose |
|-----------|-----------|---------|
| Trigger | Tines / Shuffle Webhook | Receive SIEM alert JSON |
| HTTP Action | Tines HTTP request | Call VirusTotal, AbuseIPDB APIs |
| Condition | Tines `if/else` trigger | Branch on VT score > threshold |
| Action | Tines HTTP to SIEM API | Block IP, disable account |
| Notification | Tines Teams/Slack | Alert analyst with context |
| Ticket | Tines Jira / ServiceNow | Auto-create IR ticket |

---

## Executive Report Template

```
SECURITY INCIDENT REPORT
Date: [Date] | Reference: INC-XXXX | Classification: CONFIDENTIAL

HEADLINE
[One sentence: what happened]

BUSINESS IMPACT
[Revenue / data / regulatory exposure in business terms]

WHAT WE FOUND
[Plain English: who, how they got in, what they accessed, when]

WHAT WE DID
[Actions taken: containment, eradication, recovery]

STATUS: ☐ Under Investigation  ☐ Contained  ☑ Resolved

RECOMMENDATIONS (Priority Order)
1. [Action] — [Business reason] — [Effort: Low/Med/High]
2. [Action] — [Business reason] — [Effort: Low/Med/High]
3. [Action] — [Business reason] — [Effort: Low/Med/High]
```

---

## CySA+ CS0-003 Domain Breakdown

| Domain | Weight |
|--------|--------|
| Security Operations | 33% |
| Vulnerability Management | 30% |
| Incident Response & Management | 20% |
| Reporting and Communication | 17% |

## Interview Cheat Sheet — Common SOC Questions

| Question | Key Answer Points |
|----------|-----------------|
| "Walk me through a phishing investigation" | Identify sender, analyse headers, sandbox attachment, IOC extraction, block + report |
| "What is ATT&CK and how do you use it?" | Framework for describing adversary TTPs; use for detection coverage mapping and threat hunting |
| "Difference between SIEM and SOAR?" | SIEM detects; SOAR automates response actions based on SIEM alerts |
| "What is a false positive and how do you reduce them?" | Alert on legitimate activity; tune rule with more specific conditions or filters |
| "What would you do first at a ransomware incident?" | Contain (isolate) — but preserve volatile memory first before pulling network |
