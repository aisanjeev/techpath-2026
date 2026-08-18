# Month 5 — Week-by-Week Study Plan
## Incident Response & Digital Forensics

**Total study time: ~80 hours over 4 weeks**

---

## Week 1 — NIST Incident Response Lifecycle

**Goal:** Master the 4-phase NIST IR model and be able to apply it to real scenarios.

### Day 1 — Preparation Phase: Building the IR Programme
- **Read:** `01-incident-response.md` — Preparation section
- **Key deliverables every IR programme needs:**
  - Incident Response Plan (IRP) — the high-level policy document
  - Incident Response Playbooks — step-by-step for specific incident types (ransomware, BEC, DDoS)
  - Communication tree — who calls whom, in what order, under what conditions
  - Asset inventory — you can't investigate what you don't know exists
  - Evidence collection procedures — admissibility requirements for legal action
  - Forensic toolkit — approved tools pre-installed on a jump kit
- **Create an IR Contact Matrix:**
  | Role | Name | Phone | Email | When to call |
  |------|------|-------|-------|--------------|
  | CISO | | | | All P1 incidents |
  | Legal Counsel | | | | Data breach, law enforcement |
  | PR / Communications | | | | Customer-impacting incidents |
  | External IR Firm | | | | Major breaches, forensics beyond internal capability |
  | Cyber Insurance | | | | File claim for major incidents |

### Day 2 — Detection and Analysis Phase
- **Read:** `01-incident-response.md` — Detection and Analysis section
- **Incident classification matrix:**
  | Severity | Definition | Response SLA | Escalation |
  |----------|-----------|-------------|------------|
  | P1 — Critical | Active breach, data exfiltration, ransomware spreading | Respond within 15 min, all-hands | CISO + CEO |
  | P2 — High | Malware on single system, account compromise | Respond within 1 hour | CISO |
  | P3 — Medium | Policy violation, failed attack | Respond within 4 hours | SOC Manager |
  | P4 — Low | Vulnerability detected, low-risk FP | Respond within 24 hours | Team Lead |
- **Exercise:** Classify each of these incidents as P1-P4 and justify: (a) Ransomware note found on 3 file servers; (b) Single workstation with detected and quarantined malware; (c) Employee emailing company financials to personal Gmail; (d) Outdated TLS certificate discovered; (e) Domain Controller receiving port scan from internal IP

### Day 3 — Containment Strategies
- **Short-term vs long-term containment:**
  - **Short-term (immediate):** Network isolation of affected host, account suspension, firewall rule to block C2 IP. Goal: stop the bleeding
  - **Long-term (sustainable):** Patching the vulnerability, rebuilding the compromised system from clean image, password reset for all potentially exposed accounts
- **The isolation decision:** Before isolating a server, consider:
  - Will isolation cause business disruption? (payment processing server — coordinate with business)
  - Is the attacker monitoring for isolation and will delete evidence if detected?
  - Can you capture memory first before isolating? (Volatile evidence)
- **Containment options (least to most disruptive):**
  1. Block specific C2 IP at firewall
  2. Disable the compromised user account
  3. Move host to isolated VLAN (still accessible for forensics)
  4. Disconnect network cable (complete isolation, but must physically access)

### Day 4 — Eradication and Recovery
- **Eradication checklist for a compromised Windows host:**
  - [ ] Remove all malware (antivirus + manual removal)
  - [ ] Remove all attacker persistence mechanisms (scheduled tasks, services, registry keys, cron jobs)
  - [ ] Reset ALL passwords that could have been exposed (not just the victim account)
  - [ ] Revoke any compromised certificates or API keys
  - [ ] Identify and close the initial access vector (patch, MFA, firewall rule)
  - [ ] Verify no other systems were compromised
- **Recovery decision: restore vs rebuild:** 
  - Restore from backup: fast but may restore compromised state if backup was taken after initial compromise. When was the system last known good?
  - Rebuild from scratch: slow but clean. For high-value systems (DCs, production databases) this is often the right choice after a significant breach.
- **Verification before returning to production:**
  - Re-scan with AV/EDR on the cleaned/rebuilt system
  - Verify no unauthorized accounts exist
  - Verify all security patches are applied
  - Monitor for 24-48 hours after returning to production

### Day 5 — Post-Incident Activity and Lessons Learned
- **The Post-Incident Review (PIR) / After-Action Review:**
  - Conduct within 72 hours of incident closure (while memory is fresh)
  - Attendees: everyone involved in the response (not a blame session — focus on process improvement)
  - Key questions to answer:
    1. How did the attacker get in? (Root cause)
    2. Why didn't we detect it sooner? (Detection gap)
    3. What slowed our response? (Process gap)
    4. What did we do well? (Reinforce)
    5. What specific actions will we take to prevent recurrence? (Action items with owners and due dates)
- **Complete:** `ir-interactive.html` — work through all panels

---

## Week 2 — Digital Forensics: Evidence Collection and Analysis

**Goal:** Learn forensic methodology and work with real forensic tools.

### Day 6 — The Order of Volatility and Evidence Collection
- **Read:** `02-digital-forensics.md` — evidence collection section
- **Order of volatility (most volatile first — collect in this order):**
  1. CPU registers, cache
  2. Routing table, ARP cache, process table
  3. Memory (RAM)
  4. Temporary file systems (`/tmp`, pagefile.sys)
  5. Disk (HDD/SSD)
  6. Remote logging and monitoring data
  7. Physical configuration, topology
  8. Archival media (backups, tapes)
- **Hands-on memory acquisition (legal test on your own VM):**
  ```bash
  # Linux: acquire memory with LiME (Linux Memory Extractor)
  # Install: modprobe lime-6.x.x-xxx
  # sudo insmod lime.ko "path=/tmp/memory.lime format=lime"
  
  # Windows: Use WinPmem or Volatility3 with raw acquisition
  # WinPmem.exe -o C:\temp\memory.raw
  
  # For practice: use one of Volatility Foundation's free sample memory images
  # Download from: github.com/volatilityfoundation/volatility/wiki/Memory-Samples
  ```

### Day 7 — Volatility Memory Forensics
- **Install Volatility3:**
  ```bash
  pip3 install volatility3
  # Or download from github.com/volatilityfoundation/volatility3
  ```
- **Core Volatility3 commands (work through with a sample .raw image):**
  ```bash
  # Identify OS and profile
  vol.py -f memory.raw windows.info
  
  # List running processes
  vol.py -f memory.raw windows.pslist    # By process list (can be hidden by rootkits)
  vol.py -f memory.raw windows.pstree   # Show parent/child relationships
  vol.py -f memory.raw windows.cmdline  # Show command line arguments
  
  # Network connections at time of capture
  vol.py -f memory.raw windows.netstat
  
  # Find injected code in processes
  vol.py -f memory.raw windows.malfind   # Find suspicious executable regions in process memory
  
  # Dump a suspicious process for analysis
  vol.py -f memory.raw windows.dumpfiles --pid 1234
  
  # Registry analysis from memory
  vol.py -f memory.raw windows.registry.hivelist
  vol.py -f memory.raw windows.registry.printkey --key "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
  ```

### Day 8 — Disk Forensics with Autopsy
- **Install Autopsy (free, open-source):** autopsy.com
- **Autopsy workflow:**
  1. Create a new case (case name, examiner name)
  2. Add data source: disk image, local disk, or logical files
  3. Run ingest modules: hash lookup, keyword search, web artifacts, recent activity
  4. Explore: timeline analysis, file types, deleted files, web history, email
- **Forensic artefacts to examine:**
  - **Browser artefacts:** History, downloads, saved credentials (Firefox in `places.sqlite`, Chrome in `History` SQLite)
  - **Prefetch files** (`C:\Windows\Prefetch\*.pf`): Shows what programs were executed and how many times
  - **Windows registry**: SAM, SOFTWARE, SYSTEM hives — user accounts, autorun entries
  - **Event logs**: Examine Windows EVTX files as a timeline
  - **Recent files**: `%APPDATA%\Microsoft\Windows\Recent\` — LNK files showing recently opened documents
  - **Shellbags**: Registry keys showing folder navigation history — even for external drives
- **Exercise:** Download a forensic challenge from ctf.osdfcon.org or forensicscontest.com — these provide disk images with embedded questions to answer.

### Day 9 — Log Forensics and Timeline Analysis
- **Complete `lab-05-a.json`** — all 5 steps
- **Timeline creation with log2timeline/plaso:**
  ```bash
  # Install: pip3 install plaso
  # Create super-timeline from disk image
  log2timeline.py timeline.plaso /path/to/disk.E01
  # Filter and export
  psort.py -o l2tcsv timeline.plaso -w timeline.csv
  # Open in Timeline Explorer (free tool) or Autopsy timeline view
  ```
- **Manual timeline construction:** For a Windows incident, combine these sources into a chronological spreadsheet:
  - System Event Log (7045 — service installed)
  - Security Event Log (4624, 4625, 4688, 4698)
  - Sysmon events (process create, network connect, file create)
  - $MFT (Master File Table — file system timestamps)
  - Prefetch (execution timestamps)
  - Browser history (if attacker used a browser)

### Day 10 — Complete Lab 05-b + Full IR Report Writing
- **Complete `lab-05-b.json`** — all 5 steps
- **Incident report writing:**
  
  **Executive summary (1 page):** What happened, when, what was affected, what was done, current status. Write for a non-technical CISO.
  
  **Technical report (3-5 pages):** Timeline, indicators of compromise, attack chain (MITRE ATT&CK mapped), root cause, evidence collected, actions taken.
  
  **Appendix:** Raw evidence (log excerpts, screenshots, command outputs).
  
  **Write a practice report** using this scenario: "At 09:15 on Monday, the SOC detected DNS queries to a known C2 domain from LAPTOP-HR-07. Investigation revealed a malicious Word macro had been executed via a phishing email received Friday afternoon. The malware established persistence via a scheduled task and exfiltrated 45MB of HR files before containment at 10:40."

---

## Week 3 — Advanced IR Scenarios and Tools

### Day 11 — Ransomware Incident Response
- **Ransomware-specific IR considerations:**
  1. **Scope rapidly:** Which file servers have .encrypted/.locked files? Walk the network quickly
  2. **Do NOT pay immediately:** Contact cyber insurance first; they have relationships with decryptors. Contact law enforcement (they may have decryption keys from previous busts)
  3. **Isolate the patient zero:** Find the initial infection point; this machine may hold the malware still running
  4. **Identify the ransomware family:** Check ransomware notes, file extensions on nomoreransom.org — is there a free decryptor?
  5. **Backup assessment:** Which backups are clean? Were network shares backed up to the same storage that got encrypted?
  6. **Rebuild strategy:** Based on RTO (Recovery Time Objective), what is the business priority for restoration?
- **Practice:** Read a real ransomware incident report (many are public — search "ransomware incident report case study")

### Day 12 — Business Email Compromise (BEC) Response
- **BEC scenario:** Finance receives email appearing to be from CEO asking for £250,000 wire transfer. Finance completes the transfer. What do you do?
- **BEC investigation steps:**
  1. **Determine if mailbox was compromised** (attacker sent from real CEO account) or **spoofed** (fake email from lookalike domain)
  2. Check: email headers (`Received-from` chain), login activity to CEO's email account (any unusual location/device?)
  3. If compromised: reset CEO's account password + MFA immediately, check all sent items for forwarding rules set up by attacker
  4. **Contact the bank immediately** — wire recalls must happen within hours. Many banks can recall funds if reported quickly
  5. Report to: cyber insurance, legal counsel, local police cyber crime unit, RBI's CERT-In
  6. Check if other employees received similar requests — may be part of a wider campaign

### Day 13 — Malware Analysis Introduction (Static)
- **Static analysis tools:**
  ```bash
  # Check file type and metadata
  file suspicious.exe
  exiftool suspicious.exe
  
  # Extract readable strings
  strings suspicious.exe | grep -i "http\|cmd\|powershell\|temp\|user"
  strings -el suspicious.exe   # Wide character strings (Unicode)
  
  # Check PE headers with PE-bear or Detect-It-Easy (free GUI tools)
  # Look for: sections with high entropy (packed/encrypted), import functions used,
  # compiler timestamp (was it compiled today?), code signing status
  
  # Hash for threat intel lookup
  sha256sum suspicious.exe
  ```
- **CFF Explorer (free):** GUI PE header viewer — see imports, exports, sections without running the file

### Day 14 — CTF Forensics Practice
- **Complete forensics challenges:**
  - BlueteamLabs.online — free forensics investigations
  - forensicscontest.com — classic packet capture forensics
  - Hack The Box — Forensics challenges (free tier available)
- **Document each challenge:** Write a mini-report for each: what was the artifact, what tools did you use, what did you find, what was the answer.

### Day 15 — Review and Exercises
- **Complete:** `exercises-05.md` questions 1-15
- **Tabletop exercise:** Run yourself through a full simulated incident
  1. Scenario: You receive at 2am: "SQL Server DB-PROD-01 is unreachable. DBA can't log in. 500 error on all web apps."
  2. Walk through: how do you assess if this is an incident vs technical failure? What steps? Who do you call?

---

## Week 4 — Mastery, Assignment, and Portfolio

### Day 16-17 — Assignment Tasks 1-2
- Complete `assignment-05.md` Tasks 1 and 2

### Day 18-19 — Assignment Tasks 3-4
- Complete `assignment-05.md` Tasks 3 and 4
- Push IR playbooks, forensic tool outputs, investigation reports to `/month-05-ir/` GitHub

### Day 20 — Final Assessment
- **Complete:** `exercises-05.md` questions 16-25
- **Quiz:** `quiz-05.json` — all 15 questions
- **Competency checklist:**
  - [ ] Recite the 4 NIST IR phases from memory with 3 activities each
  - [ ] Calculate dwell time from a given timeline
  - [ ] Run Volatility3 to list processes and network connections on a memory image
  - [ ] Identify the order of volatility and explain why volatile evidence must be collected first
  - [ ] Write an executive incident summary for a non-technical CISO
  - [ ] Explain when to isolate vs not isolate a compromised host
  - [ ] List 6 forensic artefacts found on a Windows system and what each reveals
  - [ ] Explain what chain of custody means and why it matters for legal proceedings
  - [ ] Describe a ransomware-specific IR approach
  - [ ] Use Autopsy to ingest a disk image and find recently deleted files
