# Month 4 — Assignment: SOC Operations & SIEM
**Total Marks: 100 | Submission: ZIP folder + PDF report**

---

## Task 1 — Homelab SIEM Deployment (25 marks)

Set up a working SIEM environment in your homelab that ingests real Windows Event Logs.

**Requirements:**
- Install Splunk Enterprise (free trial) OR Security Onion on a VM
- Configure a Windows endpoint to forward logs using the Universal Forwarder (Splunk) or Winlogbeat (ELK)
- Verify at least 500 events are indexed
- Capture a screenshot of the SIEM receiving live events

**Deliverables:**
- Screenshot of Splunk/ELK search showing indexed Windows events
- Screenshot of the data input configuration panel
- A 1-paragraph written description of your architecture (what sends logs where)

**Marking Breakdown:**

| Criterion | Marks |
|-----------|-------|
| SIEM installed and accessible | 5 |
| Log forwarder configured and sending data | 8 |
| At least 500 events visible in the interface | 7 |
| Architecture description is accurate and clear | 5 |

---

## Task 2 — SPL / KQL Detection Queries (25 marks)

Write detection queries targeting real attacker behaviour. Use your homelab data or the provided sample dataset.

**Write queries for each of the following scenarios:**

1. Detect accounts with more than 5 failed logins in 15 minutes (brute force)
2. Find any process that launched `cmd.exe` or `powershell.exe` from a non-standard parent (e.g. Word, Outlook)
3. Identify accounts that logged on after 11 PM local time
4. Find new scheduled tasks created in the last 24 hours (Event ID 4698)

For each query, include:
- The raw SPL or KQL query (your choice of platform)
- One screenshot of the query result (real or sample data)
- A sentence explaining what the query detects and why it matters

**Marking Breakdown:**

| Criterion | Marks |
|-----------|-------|
| All 4 queries are syntactically correct | 12 |
| Queries use appropriate fields and thresholds | 8 |
| Screenshots provided for each | 3 |
| Explanations are accurate and concise | 2 |

---

## Task 3 — Alert Investigation Report (30 marks)

You are given a simulated Splunk alert: **"Multiple failed RDP logins followed by successful logon from the same IP"**.

Investigate the scenario using the provided sample log file (`task3-sample-logs.json`) and write a structured investigation report including:

1. **Executive Summary** (2-3 sentences: what happened, impact, status)
2. **Timeline of Events** (table: timestamp, event, significance)
3. **IOCs Identified** (IP addresses, usernames, process names)
4. **MITRE ATT&CK Mapping** (at least 2 techniques with IDs)
5. **Recommended Actions** (immediate containment + long-term tuning)

**Marking Breakdown:**

| Criterion | Marks |
|-----------|-------|
| Executive summary is clear and non-technical | 4 |
| Timeline is accurate and complete | 8 |
| IOCs correctly identified | 6 |
| ATT&CK techniques correctly mapped with IDs | 6 |
| Recommendations are practical and specific | 6 |

---

## Task 4 — SOC Detection Dashboard (20 marks)

Build a single-page SIEM dashboard that a L1 analyst could use at the start of their shift.

**Required Panels (minimum 4):**
- Failed login attempts over time (timechart)
- Top 10 accounts with failed logins (bar chart)
- Top source IPs triggering alerts (table)
- New processes launched in last 4 hours (table)

**Bonus:** Add a panel showing MITRE ATT&CK technique coverage from your data (+3 marks)

**Marking Breakdown:**

| Criterion | Marks |
|-----------|-------|
| Dashboard loads and displays real or sample data | 5 |
| All 4 required panels present | 10 |
| Dashboard is clearly labelled and usable | 3 |
| Bonus MITRE panel | 3 (bonus) |

---

## Submission Checklist

- [ ] ZIP file containing: screenshots, query files (.spl or .kql), dashboard export
- [ ] PDF report: Tasks 2 and 3 written responses
- [ ] All queries tested (include error-free screenshot or output)
- [ ] Naming convention: `assignment-04-[your-name].zip`

## Rubric Summary

| Task | Marks |
|------|-------|
| Task 1 — SIEM Deployment | 25 |
| Task 2 — Detection Queries | 25 |
| Task 3 — Investigation Report | 30 |
| Task 4 — SOC Dashboard | 20 |
| **Total** | **100** |
