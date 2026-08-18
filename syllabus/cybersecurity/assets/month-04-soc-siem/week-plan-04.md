# Month 4 — Week-by-Week Study Plan
## SOC Operations & SIEM: Detection, Triage, and Threat Hunting

**Total study time: ~80 hours over 4 weeks**

---

## Week 1 — SOC Fundamentals and the Analyst Workflow

**Goal:** Understand how a Security Operations Centre works, what analysts do all day, and how to structure alert triage.

### Day 1 — SOC Architecture and Roles
- **Read:** `01-soc-operations.md` — fully
- **Study the SOC tier model:**
  - **L1 Analyst (you start here):** Monitor dashboards, acknowledge alerts, basic triage, escalate to L2. Typically rotational shifts. Volume: 100-200 alerts/day
  - **L2 Analyst:** Deep dive investigation, correlate events across systems, respond to escalations from L1, tune SIEM rules to reduce false positives
  - **L3 Analyst / Threat Hunter:** Proactive hunt for threats not caught by rules, reverse engineer malware, develop new detection content
  - **SOC Manager:** Team management, KPIs, stakeholder reporting, vendor relationships
  - **DFIR (Digital Forensics & Incident Response):** Called in for major incidents, forensic acquisition, root cause analysis
- **Research task:** Find 3 job postings for SOC Analyst roles in India (Naukri, LinkedIn). What tools do they require? What certifications? What experience level? Document your findings.
- **Question:** If a SOC receives 500 alerts per day and each takes 5 minutes to triage, how many analysts are needed for a single 8-hour shift (assume 80% of time is triage)? Calculate your answer.

### Day 2 — Alert Triage Methodology
- **The 5-step triage process:**
  1. **Classify:** What alert type is this? (Malware, brute force, data exfiltration, policy violation?)
  2. **Investigate context:** Is this host/user normally expected to do this? (Baselining)
  3. **Gather indicators:** IP addresses, domain names, file hashes, user accounts involved
  4. **Correlate:** Any related alerts? Other hosts affected? Timeline of events?
  5. **Decide:** True positive → escalate with evidence. False positive → close with documentation. Tune rule to prevent repeat.
- **Alert triage decision tree:** Draw a flowchart for triaging a "Suspicious PowerShell execution" alert. Include: what questions you ask, what information you gather, what makes it a TP vs FP.
- **Common false positive scenarios:**
  - Port scan from your vulnerability scanner IP
  - Known admin tool (PsExec) used by IT for legitimate maintenance
  - Antivirus quarantine triggering its own alert
  - Penetration test without a "get-out-of-jail-free card" issued

### Day 3 — Setting Up Free Splunk/ELK
- **Option A: Splunk Free (recommended for learning):**
  1. Create free account at splunk.com
  2. Download Splunk Enterprise Free (60-day trial, 500MB/day limit for free tier)
  3. Install on Windows/Linux VM
  4. Configure: `Settings → Add Data → Monitor → /var/log/` (Linux) or Windows Event Logs
  5. Test search: `index=* | head 10`
- **Option B: ELK Stack (Docker):**
  ```bash
  # Quick ELK setup with docker-compose
  docker run -d -p 5601:5601 -p 9200:9200 sebp/elk
  # Access Kibana at http://localhost:5601
  ```
- **First Splunk searches:**
  ```
  index=* source=/var/log/auth.log | head 20
  index=* "Failed password" | stats count by src_ip | sort -count
  index=* | timechart count span=1h
  ```

### Day 4 — SIEM Data Sources and Log Ingestion
- **Study what logs each source provides:**
  | Source | Key events | Format |
  |--------|-----------|--------|
  | Windows Event Logs | 4624, 4625, 4688, 4698, 7045 | XML/EVTX |
  | Linux syslog/auth.log | SSH, sudo, cron | Syslog |
  | Firewall logs | Allow/deny, NAT, VPN | CEF/Syslog |
  | Web server (Apache/nginx) | HTTP requests, 4xx/5xx | Combined log format |
  | DNS server | Queries, responses, NXDOMAIN | Syslog/DNS log |
  | Endpoint (EDR) | Process, file, network events | JSON |
- **Hands-on data ingestion:** On your Splunk instance, ingest at least 3 different log types. Create a search that queries all of them together: `index=* | stats count by host, sourcetype`
- **Log format exercises:** Given a raw syslog line, identify: timestamp, hostname, process name, PID, message

### Day 5 — Week 1 Review: Splunk SPL Basics
- **Splunk SPL (Search Processing Language) fundamentals:**
  ```spl
  # Basic search with time range
  index=windows EventCode=4625 | head 100
  
  # Stats (count, sum, avg, distinct count)
  index=windows EventCode=4625 | stats count by Account_Name, src_ip
  
  # Table command — format results
  index=windows EventCode=4625 | table _time Account_Name src_ip
  
  # Where command — filter results
  index=windows | where EventCode IN (4624, 4625, 4688)
  
  # Rex — extract fields with regex
  index=* source=*/auth.log | rex field=_raw "from (?<src_ip>\d+\.\d+\.\d+\.\d+)" | stats count by src_ip
  
  # Eval — create calculated fields
  index=windows | eval risk_score=if(EventCode=4625, 10, 0) | stats sum(risk_score) by src_ip
  
  # Transaction — group related events
  index=windows EventCode IN (4625, 4624) | transaction src_ip maxpause=5m
  ```
- **Build your first dashboard:** Create a Splunk dashboard with 3 panels: Failed logins over time (timechart), Top source IPs by failed logins (bar chart), Recent successful logins (table)

---

## Week 2 — SIEM Platforms and Advanced Detection

**Goal:** Build detection rules, understand MITRE ATT&CK, and start writing correlation searches.

### Day 6 — MITRE ATT&CK Framework
- **Read:** `02-siem-platforms.md` — MITRE ATT&CK section
- **Navigate ATT&CK:**
  - Go to attack.mitre.org → Enterprise Matrix
  - Explore each tactic column: Initial Access, Execution, Persistence, Privilege Escalation, Defence Evasion, Credential Access, Discovery, Lateral Movement, Collection, C2, Exfiltration, Impact
  - Click on `T1003.001 - OS Credential Dumping: LSASS Memory` — study: description, sub-techniques, procedure examples, detection
- **ATT&CK Navigator exercise:**
  - Go to mitre-attack.github.io/attack-navigator
  - Create a "threat profile" for a ransomware actor — highlight all the techniques they typically use
  - Colour code green what you can detect, red what you can't yet
- **Question:** Find a recent threat intelligence report for an APT group (CISA, Mandiant, CrowdStrike — all have free reports). Map 5 of the TTPs described to specific ATT&CK technique IDs.

### Day 7 — Writing Detection Rules in Splunk
- **Build correlation searches for real threats:**

  **Detection 1: Brute force followed by success**
  ```spl
  index=windows EventCode=4625
  | stats count as failures, values(Account_Name) as accounts by src_ip
  | where failures > 20
  | join type=inner src_ip [
      search index=windows EventCode=4624
      | stats count as successes by src_ip
  ]
  | where successes > 0
  | table src_ip failures successes accounts
  ```

  **Detection 2: New local admin account created**
  ```spl
  index=windows EventCode=4720
  | join type=inner Security_ID [
      search index=windows EventCode=4732 Group_Name="Administrators"
      | rename Member_Security_ID as Security_ID
  ]
  | table _time Account_Name Created_By
  ```

  **Detection 3: PowerShell encoded command**
  ```spl
  index=windows EventCode=4688 Process_Name="*powershell*"
  | where like(Process_Command_Line, "%-enc%") OR like(Process_Command_Line, "%-encodedcommand%")
  | table _time Computer Account_Name Process_Command_Line
  ```

### Day 8 — Complete Lab 04-a: SIEM Detection Rules
- **Complete `lab-04-a.json`** — all 5 steps
- **Build 3 more detection rules for:**
  1. DNS requests to domains with newly registered status (> 15 unique domain queries per hour from one host)
  2. Outbound connections on unusual ports (anything not 80, 443, 53, 22, 25)
  3. Lateral movement (same account authenticating to multiple hosts within 1 hour)

### Day 9 — Threat Hunting Introduction
- **What is threat hunting?**
  - Proactive search for threats that have evaded automated detection
  - Hypothesis-driven: "I believe attacker X may have used technique Y. Let me search for evidence."
  - Outcome: either find the threat, or improve detection to catch it next time
- **Hunting methodology:**
  1. **Create hypothesis** from threat intelligence ("Ransomware groups often use PsExec for lateral movement")
  2. **Define indicators** (what would this technique look like in logs?)
  3. **Hunt** (write searches across all relevant log sources)
  4. **Analyse results** (filter noise, look for anomalies)
  5. **Document and improve** (if found → IR, if not found → create detection rule)
- **Hunt exercise — beacon detection:**
  ```spl
  # Find processes making very regular outbound connections (C2 beaconing pattern)
  index=network
  | stats count, values(dest_port) as ports, range(_time) as duration by src_ip, process_name
  | eval requests_per_minute = count / (duration / 60)
  | where requests_per_minute > 1 AND requests_per_minute < 2  # Looking for ~1/min regularity
  | sort -count
  ```

### Day 10 — Splunk Enterprise Security / Microsoft Sentinel Introduction
- **Complete `lab-04-b.json`** — all 5 steps
- **Microsoft Sentinel free lab:** Use the free tier of Microsoft Sentinel (Azure free account gives $200 credit)
  - Deploy Sentinel → Connect Windows Security Events data connector
  - Explore the built-in analytics rules (click "Analytics" in Sentinel)
  - Find a rule for "Scheduled Task Created or Modified" — what KQL does it use?
- **KQL vs SPL comparison:**
  ```kql
  // Microsoft Sentinel (KQL)
  SecurityEvent
  | where EventID == 4625
  | summarize count() by Account, IpAddress
  | order by count_ desc
  ```
  ```spl
  // Splunk (SPL)
  index=windows EventCode=4625
  | stats count by Account_Name, src_ip
  | sort -count
  ```

---

## Week 3 — Incident Detection and Response Integration

**Goal:** Handle a full simulated security incident from first alert through resolution.

### Day 11 — Tabletop Exercise: Ransomware Alert
- **Scenario:** Your SIEM fires an alert at 14:00: "Suspicious file extension creation (*.locked) detected on FILE-SERVER-01"
- **Work through the full incident:**
  1. What is your first action? (Do NOT immediately isolate — you need to understand scope first)
  2. What additional searches do you run in your SIEM?
  3. What other systems might be affected?
  4. At what point do you escalate to L3/IR team?
  5. What is the communication chain? (Technical team → Management → Legal?)
  6. What data do you need to preserve for forensics before isolating?
  7. Write a 1-paragraph incident update email suitable for sending to your manager

### Day 12 — SOC Metrics and Reporting
- **Key SOC metrics to track:**
  - MTTD (Mean Time to Detect): Average time from compromise to detection
  - MTTR (Mean Time to Respond): Average time from detection to containment
  - Alert-to-ticket ratio: What % of alerts become incidents?
  - False positive rate: What % of alerts are not real threats?
  - SLA compliance: What % of P1 alerts responded to within 15 minutes?
- **Build a SOC metrics dashboard in Splunk:**
  ```spl
  # Alert volume by day
  index=soc_alerts | timechart count span=1d
  
  # Average response time
  index=soc_cases | eval response_time = close_time - open_time
  | stats avg(response_time) as avg_mttr
  | eval avg_mttr_minutes = round(avg_mttr / 60, 1)
  ```

### Day 13 — LetsDefend.io Blue Team Practice
- **Sign up at letsdefend.io** (has a free tier)
- **Complete the "SOC Fundamentals" learning path:**
  - Work through the practice SOC alerts
  - The platform simulates real SIEM alerts and asks you to investigate and classify them
  - Document each alert: what was it? TP or FP? How did you determine this?
- **Target:** Complete at least 5 practice alerts from the LetsDefend alert feed

### Day 14 — Log Aggregation Architecture
- **Study log pipeline:**
  - **Collection:** Sysmon (Windows events), auditd (Linux), Filebeat/Winlogbeat (shipping agents)
  - **Transport:** Kafka (buffering), Logstash (parsing/enriching), Fluentd
  - **Storage:** Elasticsearch (SIEM), Splunk indexes, Azure Log Analytics
  - **Visualisation:** Kibana (dashboards), Splunk (dashboards), Sentinel (workbooks)
- **Sysmon deep dive:**
  - Download Sysmon from Microsoft Sysinternals (free)
  - Install with SwiftOnSecurity's sysmon config: `sysmon64.exe -accepteula -i sysmonconfig.xml`
  - Key Sysmon event IDs: 1 (Process Create), 3 (Network Connect), 7 (Image Load), 10 (Process Access), 11 (File Create), 13 (Registry Value Set)
  - Open Event Viewer → Applications and Services Logs → Microsoft → Windows → Sysmon

### Day 15 — Complete Exercises + Build Use Case Library
- **Complete:** `exercises-04.md` questions 1-15
- **Complete:** `siem-interactive.html` — all panels
- **Build your personal "use case library":** A document with 10 detection use cases you've built. For each: the ATT&CK technique, the business risk, the Splunk/KQL query, and the false positive sources

---

## Week 4 — Mastery, Assignment, and Portfolio

### Day 16-17 — Assignment Tasks 1-2
- Complete `assignment-04.md` Tasks 1 and 2

### Day 18-19 — Assignment Tasks 3-4
- Complete `assignment-04.md` Tasks 3 and 4
- Push SIEM queries, dashboard screenshots, and use case library to GitHub `/month-04-soc-siem/`

### Day 20 — Final Assessment
- **Complete:** `exercises-04.md` questions 16-25
- **Full quiz:** `quiz-04.json` — all 15 questions
- **Competency self-check:**
  - [ ] Build a Splunk search that finds brute force followed by successful login
  - [ ] Explain MITRE ATT&CK and navigate to a specific technique
  - [ ] Describe the 3 SOC tier model and what each tier does
  - [ ] Define MTTD and MTTR and explain why they matter
  - [ ] Write a Splunk search using stats, eval, and rex
  - [ ] Explain what threat hunting is and describe a hunting hypothesis
  - [ ] List 5 data sources that feed a SIEM and what events each provides
  - [ ] Describe the difference between a correlation rule and a threat hunt
  - [ ] Explain what UEBA is and what insider threat it can detect
  - [ ] Configure a Splunk dashboard with at least 3 panels
