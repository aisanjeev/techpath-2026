# Month 4 — Resources: SOC Operations & SIEM

## Tools to Download & Install

### 1. Splunk Enterprise (Free Trial / Developer License)
- **URL:** https://www.splunk.com/en_us/download/splunk-enterprise.html
- **Version:** Latest (9.x)
- **Notes:** Free developer license allows 500 MB/day ingestion — sufficient for homelab
- **Also install:** Splunk Universal Forwarder for log shipping

### 2. Security Onion (Free Open-Source NSM/SIEM)
- **URL:** https://securityonion.net/
- **ISO Download:** https://github.com/Security-Onion-Solutions/securityonion/releases
- **Notes:** Full SOC-in-a-box — Elastic backend, Kibana dashboards, Suricata IDS, Zeek NSM
- **Minimum:** 4 CPU cores, 16 GB RAM, 200 GB disk

### 3. Elastic Stack / ELK (Open Source)
- **URL:** https://www.elastic.co/downloads/
- **Docker Compose:** https://github.com/elastic/elasticsearch/tree/main/distribution/docker
- **Winlogbeat (Windows log shipper):** https://www.elastic.co/downloads/beats/winlogbeat
- **Notes:** Free and open-source version sufficient for labs

### 4. Sysmon (System Monitor by Microsoft)
- **URL:** https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
- **Config (SwiftOnSecurity):** https://github.com/SwiftOnSecurity/sysmon-config
- **Notes:** Essential for enriching Windows Event Logs — install before any SIEM lab

### 5. MITRE ATT&CK Navigator
- **Online:** https://mitre-attack.github.io/attack-navigator/
- **GitHub (self-host):** https://github.com/mitre-attack/attack-navigator
- **Notes:** Map your detection coverage to ATT&CK tactics; export layer files for portfolio

---

## Online Learning Resources

### 1. TryHackMe — SOC Level 1 Learning Path
- **URL:** https://tryhackme.com/path/outline/soclevel1
- **Topics:** Cyber defense, Splunk, ELK, network traffic analysis
- **Cost:** Free tier available; some rooms require subscription

### 2. Splunk Free Training (Splunk Training Portal)
- **URL:** https://www.splunk.com/en_us/training/free-courses/splunk-fundamentals-1.html
- **Course:** Splunk Fundamentals 1 (free, self-paced, ~9 hours)
- **Also:** Splunk Search Expert and Splunk Enterprise Security courses

### 3. Microsoft Learn — Microsoft Sentinel Training
- **URL:** https://learn.microsoft.com/en-us/training/paths/security-ops-sentinel/
- **Topics:** KQL, analytics rules, workbooks, SOAR playbooks
- **Cost:** Free

### 4. MITRE ATT&CK Official Website
- **URL:** https://attack.mitre.org/
- **ATT&CK for Enterprise:** https://attack.mitre.org/matrices/enterprise/
- **Notes:** Primary reference for all TTP mapping in detection work

### 5. Elastic SIEM Tutorial (Elastic Blog)
- **URL:** https://www.elastic.co/blog/elastic-siem-free-and-open
- **KQL Detection Rules repo:** https://github.com/elastic/detection-rules
- **Notes:** Includes pre-built detection rules you can review and adapt

---

## Practice Datasets

| Dataset | URL | Use Case |
|---------|-----|----------|
| BOTS (Boss of the SOC) | https://github.com/splunk/botsv3 | Splunk CTF-style dataset |
| EVTX Sample Logs | https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES | Real Windows logs mapped to ATT&CK |
| Mordor (OTRF) | https://github.com/OTRF/Security-Datasets | Simulated attack telemetry |
