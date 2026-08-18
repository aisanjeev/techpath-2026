# Month 06 — Assignment: Detection Engineering & Job-Ready Milestone

**Deadline:** End of Month 6 (Week 26)
**Submission:** GitHub portfolio link + LinkedIn post screenshot
**Total:** 100 marks

---

## Task 1: Write a Sigma Detection Rule (25 marks)

Write a Sigma rule that detects **suspicious PowerShell execution** — specifically, PowerShell downloading content from the internet using `Invoke-WebRequest` or `IEX` (Invoke-Expression), which are commonly used in malware loaders.

Your rule must include:
- `title`, `description`, `status: experimental`
- `logsource` pointing to Windows process creation (Sysmon EventID 1)
- `detection` block with the suspicious command patterns
- `condition` combining the patterns
- `level: high`
- `tags` mapping to a MITRE ATT&CK technique (T1059.001)

```yaml
# Template to start from:
title: Suspicious PowerShell Download Cradle
id: <generate a UUID>
status: experimental
description: |
  Detects PowerShell commands used to download and execute content from the internet,
  commonly seen in malware loaders and Living-off-the-Land attacks.
logsource:
  category: process_creation
  product: windows
detection:
  selection:
    Image|endswith: '\powershell.exe'
    CommandLine|contains:
      - 'Invoke-WebRequest'
      - 'IEX'
      - 'DownloadString'
      - 'WebClient'
  condition: selection
falsepositives:
  - Legitimate admin scripts
  - Windows update components
level: high
tags:
  - attack.execution
  - attack.t1059.001
```

**Extend it:** Add a second detection block that also flags `wget` or `curl` from PowerShell.

**Submit:** Complete `.yml` Sigma rule file on GitHub.

**Marking:**
- Valid YAML structure: 8 marks
- Detection logic is correct: 10 marks
- MITRE tags present: 4 marks
- False positives documented: 3 marks

---

## Task 2: Write a YARA Rule (25 marks)

Write a YARA rule that detects a file containing characteristics of a generic ransomware dropper. Your rule should look for:
1. The string "Your files have been encrypted" (common ransomware message)
2. The string ".locked" or ".encrypted" (ransomware file extensions)
3. The MZ header (`4D 5A`) — indicates a Windows PE executable
4. Any Bitcoin address pattern (regex: `/1[a-zA-Z0-9]{25,34}/`)

Your rule must fire only when the MZ header AND at least one of the string conditions are present.

**Test it:** Use the `yara` command-line tool to scan a directory:
```bash
yara ransomware_detector.yar /path/to/test/files/
```

**Submit:** `ransomware_detector.yar` on GitHub with test results screenshot.

**Marking:**
- Valid YARA syntax: 8 marks
- Correct condition logic (MZ + strings): 10 marks
- Rule tested and screenshot provided: 7 marks

---

## Task 3: Build a Simple SOAR Playbook (25 marks)

Using **Shuffle** (free at shuffler.io) or any diagramming tool (draw.io, Miro), design an automated playbook for the following scenario:

**Trigger:** SIEM alert fires for "Multiple Failed Logins from Same IP" (>10 in 5 minutes)

**Your playbook must automate these steps:**
1. Extract the attacking IP from the alert
2. Check the IP against AbuseIPDB API (free tier available)
3. Check if the IP is an internal RFC1918 address (if so — escalate differently, may be internal threat)
4. If external and score > 50 on AbuseIPDB → automatically create firewall block rule
5. Create ticket in ticketing system (or simulate this step)
6. Notify the analyst via email/Slack with summary
7. If the IP later has a successful login → escalate to P1 incident immediately

**Deliverable:** Screenshot of your Shuffle workflow OR a flowchart diagram clearly showing each step, decision points, and outputs.

**Marking:**
- All 7 steps represented: 14 marks
- Decision logic for internal vs external IP: 6 marks
- Escalation path for successful login: 5 marks

---

## Task 4: Portfolio Milestone (25 marks)

This is the Month 6 job-ready milestone. Publish your cybersecurity portfolio to GitHub and LinkedIn.

**GitHub Portfolio must include:**
- README.md explaining your 6-month journey and skills gained
- `/homelab/` — homelab build documentation with network diagram
- `/siem/` — at least one SIEM dashboard screenshot and detection setup
- `/incident-reports/` — at least one investigation report (from Month 5 lab)
- `/detection-rules/` — your Sigma rule and YARA rule from Tasks 1 & 2

**LinkedIn Post:**
- Post about completing 6 months of cybersecurity training
- Tag your portfolio link
- Include a screenshot of one impressive artefact (dashboard, detection hit, or report)
- Use hashtags: #CyberSecurity #SOC #LearningInPublic

**Marking:**
- GitHub README complete: 8 marks
- All 4 portfolio folders with content: 12 marks
- LinkedIn post published with portfolio link: 5 marks

---

## Rubric

| Criteria | Full Marks | Good (75%) | Needs Work (50%) |
|----------|-----------|------------|-----------------|
| Sigma rule | Valid YAML, correct logic, MITRE tags | Valid YAML, minor logic issues | Invalid syntax or missing key fields |
| YARA rule | Correct condition, tested with screenshot | Working rule but untested | Syntax errors or incorrect logic |
| SOAR playbook | All steps, decision logic, escalation | Most steps, missing escalation | Basic diagram only |
| Portfolio | All folders, LinkedIn post | GitHub only, no LinkedIn | README only |
