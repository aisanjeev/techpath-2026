# Month 7 — Ethical Hacking: Assignment

**Total Marks: 100**
**Submission:** PDF report + screenshots zip. Due end of Month 7 Week 4.

---

## Task 1 — OSINT Recon on a Target Domain (25 marks)

Choose any **public bug bounty target** from HackerOne or Bugcrowd with a defined scope (e.g., `*.example-bugbounty.com`). Perform passive reconnaissance only.

**Deliverables:**
- List of subdomains discovered (minimum 10)
- List of email addresses or employee names found
- At least one Shodan result showing open ports/services
- At least one Google dork returning interesting results
- Screenshot of Maltego graph or equivalent OSINT map

**Tools to use:** theHarvester, Amass, Shodan CLI, Google dorks, WHOIS

---

## Task 2 — Nmap Scanning & Enumeration (25 marks)

Set up **Metasploitable 2** or **TryHackMe "Vulnversity" room** as your target.

**Steps:**
1. Run a host discovery sweep on the subnet
2. Run a full port scan (-p-) with service version detection
3. Identify at least 3 services with known vulnerabilities from the output
4. Run at least 2 NSE scripts relevant to discovered services
5. Export results in XML format

**Deliverables:**
- Screenshot of each nmap command and output
- Short analysis paragraph (3-5 sentences) explaining the attack surface

---

## Task 3 — Exploitation & Privilege Escalation (35 marks)

Using **Metasploitable 2**, **HackTheBox Starting Point**, or **VulnHub** machine of your choice:

**Steps:**
1. Identify and document one exploitable vulnerability (CVE preferred)
2. Exploit it using Metasploit or a manual exploit — gain initial shell access
3. Run a post-exploitation recon script (e.g., `local_exploit_suggester`)
4. Escalate privileges to root/SYSTEM using at least one technique
5. Capture the root flag or equivalent proof

**Deliverables:**
- Screenshot of initial shell obtained
- Screenshot of privilege escalation steps
- Screenshot of root/SYSTEM prompt with `whoami` and `hostname`

---

## Task 4 — Penetration Test Report (15 marks)

Write a concise penetration test report covering Tasks 2 and 3. Structure:

- **Executive Summary** (5-8 sentences, non-technical)
- **Findings Table** (Finding | Severity | CVSS Score | Remediation)
- **Evidence** (screenshots inline with captions)

---

## Marking Rubric

| Task | Criteria | Marks |
|---|---|---|
| Task 1 | 10+ subdomains found | 8 |
| Task 1 | Email/employee OSINT evidence | 7 |
| Task 1 | Shodan + dork results documented | 10 |
| Task 2 | Full port scan with version detection | 10 |
| Task 2 | NSE scripts used and output explained | 8 |
| Task 2 | XML export + analysis paragraph | 7 |
| Task 3 | Exploit demonstrated with evidence | 15 |
| Task 3 | Privilege escalation to root/SYSTEM | 15 |
| Task 3 | Root flag captured | 5 |
| Task 4 | Executive summary quality | 5 |
| Task 4 | Findings table with CVSS scores | 5 |
| Task 4 | Remediation recommendations | 5 |
| **Total** | | **100** |

---

> **Ethics Reminder:** Only test systems you own or have explicit written permission to test. Bug bounty targets must be tested within their stated scope rules.
