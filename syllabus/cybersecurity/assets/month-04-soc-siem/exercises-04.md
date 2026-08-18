# Month 4 — Practice Exercises: SOC Operations & SIEM

**25 exercises with worked answers.**

---

## Section A: SOC Fundamentals (Questions 1-7)

**Q1.** You are an L1 SOC analyst and receive this alert: "Antivirus detected and quarantined `Trojan.GenericKD.47893` on host LAPTOP-JK42 (user: jkumar@company.com) at 14:23." Walk through your complete triage process, step by step.

**Answer:**
**Step 1 — Classify:** True Positive confirmed by AV (detected and quarantined = AV is confident it's malicious). Category: Endpoint malware detection.

**Step 2 — Scope it:** Is LAPTOP-JK42 one isolated case or widespread?
```spl
index=av | stats count by hostname, signature | where signature="Trojan.GenericKD.47893"
```

**Step 3 — Timeline reconstruction:** What happened before the detection?
```spl
index=* host=LAPTOP-JK42 | sort by _time | head 50
```
Look for: recent file downloads, email attachments opened, USB insertion, suspicious process creation.

**Step 4 — Network containment check:** Has this host talked to external C2?
```spl
index=network src_host=LAPTOP-JK42 | stats count by dest_ip | where dest_ip!="192.168.*"
```

**Step 5 — User check:** Contact jkumar — did they download anything unusual? Is the laptop physically accessible?

**Step 6 — Escalate to L2:** Provide: hostname, user, timestamp, malware name, quarantine status, any external IP connections found, timeline

**Step 7 — Document:** Close ticket with: classification (TP - malware), root cause (suspected phishing attachment or download), actions taken, open items

---

**Q2.** What is the difference between a true positive (TP), false positive (FP), true negative (TN), and false negative (FN) in the context of SIEM alerts? Give an example of the consequences of a high false negative rate in a SOC.

**Answer:**
| | Alert fires | No alert |
|-|-------------|---------|
| **Threat present** | TP — correct detection | FN — missed detection |
| **No threat** | FP — false alarm | TN — correct quiet |

**High FP rate consequence:** Analysts become desensitised (alert fatigue). When 98 out of 100 alerts are false alarms, analysts stop investigating carefully — they start clicking through alerts quickly. A real attack hidden in the noise gets closed as "FP" without proper investigation. This is called the "cry wolf" problem.

**High FN rate consequence (more dangerous):** Real attacks are not detected at all. The attacker operates undetected. For example, if your SIEM has no rule for PowerShell encoded commands, an attacker using `powershell.exe -enc <base64>` would never trigger an alert. The attacker moves laterally, escalates privileges, and exfiltrates data with zero visibility.

---

**Q3.** Write Splunk SPL to detect brute force attacks: more than 10 failed logins from the same source IP within 5 minutes, followed by a successful login within the next 10 minutes.

**Answer:**
```spl
# Step 1: Find IPs with >10 failures in 5-minute windows
index=windows EventCode=4625
| bucket _time span=5m
| stats count as failures by src_ip, _time
| where failures > 10

# Step 2: Join with successful logins within 10 minutes after
| join type=inner src_ip [
    search index=windows EventCode=4624
    | eval success_time = _time
]
| where success_time >= _time AND success_time <= _time + 600

# Step 3: Format for analyst review
| table src_ip failures success_time _time
| eval time_to_success = round((success_time - _time) / 60, 1)
| rename _time as failure_window_start, success_time as first_success
| sort -failures
```

Alternative with `transaction`:
```spl
index=windows EventCode IN (4624, 4625)
| transaction src_ip maxspan=15m keepevicted=true
| where eventcount > 10
| eval has_success = if(match(EventCode, "4624"), 1, 0)
| where has_success=1
| table _time src_ip eventcount Account_Name
```

---

**Q4.** Explain what MITRE ATT&CK is and how it should be used in a SOC. Give 3 specific ways a SOC team uses ATT&CK in their daily operations.

**Answer:** MITRE ATT&CK (Adversarial Tactics, Techniques, and Common Knowledge) is a framework documenting real-world adversary behaviour — how attackers actually operate, structured by Tactic (why: persistence, lateral movement) and Technique (how: registry run keys, PsExec).

**3 SOC applications:**

1. **Alert classification:** When you detect `powershell.exe -enc <base64>`, tag it to ATT&CK T1059.001 (Command and Scripting Interpreter: PowerShell). This lets you track which techniques attackers are using against you, and see patterns in your threat landscape.

2. **Detection gap analysis:** Map your existing SIEM rules to ATT&CK. Which techniques have zero detection rules? These are your blind spots. "We have nothing detecting T1055 (Process Injection) — need to add Sysmon rules."

3. **Threat intelligence integration:** When you receive CTI about a new threat actor, map their TTPs to ATT&CK. "APT29 uses T1078 (Valid Accounts) + T1021.001 (RDP) + T1074 (Data Staged)" → immediately check if you can detect those techniques with existing rules.

---

**Q5.** Your SIEM fires an alert: "DNS query to known malware C2 domain `update.bad-cdn.ru` from host `10.0.5.22`." The host is a Windows server. List the next 8 investigation steps in priority order.

**Answer:**
1. **Isolate from network** (if policy permits immediate isolation — balance against forensic value of live traffic)
2. **Identify the host:** `nslookup 10.0.5.22` — what is this server? Web server? DB server? What does it do?
3. **Query SIEM for scope:** Did any other hosts also query `update.bad-cdn.ru`?
   ```spl
   index=dns query="update.bad-cdn.ru" | stats count by src_ip
   ```
4. **Get full network context:** What other external IPs has `10.0.5.22` connected to in the last 24 hours?
5. **Timeline before the C2 query:** What processes ran on `10.0.5.22` in the 2 hours before this alert? (Event 4688)
6. **Identify the calling process:** What process initiated the DNS query? (Sysmon Event 22 — DNS query includes process name)
7. **Check VirusTotal/ThreatIntel for the domain:** What is `update.bad-cdn.ru`? What malware family uses it? When was it registered?
8. **Escalate to L2/DFIR** with: full timeline, scope (single host vs multiple), calling process, any other C2 communications

---

**Q6.** What is "alert fatigue" in a SOC? Describe 4 strategies to reduce it without reducing security coverage.

**Answer:** Alert fatigue occurs when analysts receive so many alerts (especially false positives) that they become overwhelmed and desensitised, potentially missing real incidents.

**4 strategies:**
1. **Tune and suppress false positives at the source:** When a rule consistently fires on known-legitimate activity (e.g., vulnerability scanner IP triggering port scan alerts), add an exclusion for that specific IP. Don't suppress the rule — suppress the known-legitimate exception.

2. **Risk-based alerting:** Instead of alerting on every event, assign risk scores and only alert when a threshold is reached. Single failed login = no alert. 50 failed logins from foreign IP to admin account = high priority alert. Combine multiple weak signals into one meaningful alert.

3. **Alert consolidation:** Group related alerts. Instead of 500 individual "failed login" alerts, aggregate them into one: "IP 185.x.x.x made 500 failed login attempts against 15 accounts over 10 minutes."

4. **Automated triage for known-good patterns:** Build automation (SOAR playbooks) to automatically close alerts when they match a known-good pattern (e.g., scheduled task created by deployment tool X on host Y during maintenance window Z) — only alert the human if the pattern doesn't match.

---

**Q7.** Explain the difference between a SIEM and an EDR. When would you use each for an investigation?

**Answer:**
**SIEM (Security Information and Event Management):**
- Aggregates and correlates logs from many sources (network devices, servers, cloud, endpoints)
- Works with structured log data that devices send to it
- Excellent for: correlating events across many systems, compliance reporting, network-level visibility, detecting patterns over time
- Limitation: only sees what devices log and forward; can't drill into process memory or file content

**EDR (Endpoint Detection and Response):**
- Agent installed on each endpoint, providing deep visibility into process behaviour
- Sees: exact process execution trees, file system changes, registry modifications, DLL loads, network connections by process
- Excellent for: investigating malware on a specific endpoint, hunting for fileless threats, memory analysis, taking response actions (kill process, quarantine file, isolate host)
- Limitation: only sees individual endpoints, not network-wide patterns

**Investigation workflow:**
- **SIEM first** to identify the affected hosts and understand the scope (which IPs, which accounts, which timeframes)
- **EDR second** to deep-dive into a specific infected host — see exactly what the malware did, what it called, what it dropped

---

## Section B: SIEM Platform Skills (Questions 8-15)

**Q8.** Write Splunk SPL searches to detect each of these MITRE ATT&CK techniques:
a) T1070.001 — Clear Windows Event Logs  
b) T1547.001 — Registry Run Key persistence  
c) T1566.001 — Spear Phishing Attachment (detect email with .exe attachment)

**Answer:**
```spl
# a) T1070.001 — Clear Windows Event Logs
# Event 1102 (Security log cleared) or 104 (System log cleared)
index=windows EventCode IN (1102, 104)
| table _time host Account_Name SubjectUserName

# b) T1547.001 — Registry Run Key Persistence
# Sysmon Event 13 (Registry Value Set) to Run keys
index=sysmon EventID=13
| where like(TargetObject, "%\\CurrentVersion\\Run%")
| table _time Computer User TargetObject Details

# c) T1566.001 — Phishing with executable attachment
# Requires email security log ingestion (Proofpoint, Exchange)
index=email
| where match(attachment_name, "\.(exe|bat|vbs|js|ps1|scr|pif|com|lnk|hta)$")
| table _time sender recipient subject attachment_name
| sort -_time
```

---

**Q9.** You need to build a Splunk dashboard for the daily SOC briefing. Describe what 6 panels it should include, what each shows, and what SPL generates each panel.

**Answer:**
```spl
# Panel 1: Alert Volume by Severity (last 24h)
index=soc_alerts
| timechart count by severity span=1h

# Panel 2: Top 10 Alerted Hosts
index=soc_alerts earliest=-24h
| stats count by hostname | sort -count | head 10

# Panel 3: MITRE ATT&CK Technique Heatmap
index=soc_alerts earliest=-24h
| stats count by mitre_technique | sort -count

# Panel 4: New External IPs Seen Today
index=network earliest=-24h dest_zone=external
| stats count by dest_ip | sort -count | head 20

# Panel 5: Unresolved High/Critical Alerts
index=soc_tickets status IN ("open", "investigating") severity IN ("high", "critical")
| table _time hostname alert_type assigned_to age_hours | sort -age_hours

# Panel 6: Top Targeted Usernames (failed logins)
index=windows EventCode=4625 earliest=-24h
| stats count by Account_Name | sort -count | head 10
```

---

**Q10.** What is KQL (Kusto Query Language) and how is it used in Microsoft Sentinel? Rewrite this Splunk SPL in KQL:
```spl
index=windows EventCode=4625
| stats count as failures by Account_Name, src_ip
| where failures > 5
| sort -failures
```

**Answer:** KQL is the query language used in Microsoft Sentinel, Azure Monitor, and Azure Data Explorer. It uses a pipe-based syntax similar to Splunk SPL but different syntax.

```kql
// Microsoft Sentinel / KQL equivalent
SecurityEvent
| where EventID == 4625
| summarize failures = count() by Account = TargetAccount, src_ip = IpAddress
| where failures > 5
| order by failures desc
```

Key differences from SPL:
- `where` instead of `| where` (can be used without pipe after `|`)
- `summarize` instead of `stats`
- `count()` instead of `count`
- `order by` instead of `sort`
- `by` parameters can be renamed inline `Account = TargetAccount`

---

**Q11.** Explain what "dwell time" is in cybersecurity. What does the average dwell time for attackers tell you about SOC effectiveness, and how does a SOC reduce dwell time?

**Answer:** **Dwell time** is the number of days an attacker is inside a network before they are detected and removed. Industry average has historically been 200+ days (Mandiant M-Trends reports), though this has improved to ~16-24 days in recent years for organisations with mature security programs.

**What it tells you:** High dwell time means: attackers have time to explore, escalate privileges, understand the environment, identify valuable data, and establish multiple persistence mechanisms. Lower dwell time = less damage.

**How to reduce:**
1. **Improve detection rules** — add ATT&CK coverage, especially for early-stage techniques (Initial Access, Discovery)
2. **Threat hunting program** — proactively search for attacker TTPs already in your network
3. **Network segmentation** — limit lateral movement so attackers can't reach all systems silently
4. **Deception technology (honeypots)** — place fake assets that no legitimate user should touch; any access = immediate alert
5. **Asset discovery** — you can't detect an attacker on a system you don't know exists
6. **Log centralization** — ensure ALL systems forward logs; dark spots are where attackers hide

---

**Q12.** Design a Splunk correlation search that detects a "low and slow" brute force attack — one that spreads attempts over many hours to evade threshold-based rules.

**Answer:**
```spl
# Detect >50 failed logins from the same IP over a 24-hour period
# (threshold too low to trigger immediate brute force rules)
index=windows EventCode=4625 earliest=-24h
| bucket _time span=1h
| stats count as hourly_failures by src_ip, _time
| eventstats sum(hourly_failures) as total_failures, 
             dc(_time) as active_hours by src_ip
| where total_failures > 50 AND active_hours >= 6  # spread across 6+ hours
| dedup src_ip
| join type=inner src_ip [
    search index=windows EventCode=4624 earliest=-24h
    | stats min(_time) as first_success by src_ip
]
| eval attack_type = "Low and Slow Brute Force - " + toString(total_failures) + " attempts over " + toString(active_hours) + " hours"
| table src_ip total_failures active_hours first_success attack_type
```

---

**Q13.** What is a SOAR platform? List 5 specific tasks that are well-suited to SOAR automation, and 3 tasks that should always involve a human analyst.

**Answer:** SOAR (Security Orchestration, Automation, and Response) platforms automate repeatable security tasks and orchestrate tools. Examples: Splunk SOAR, Palo Alto XSOAR, Tines, Shuffle.

**Well-suited to automation (no human needed):**
1. **IP reputation lookup:** On every alert, automatically query VirusTotal, AbuseIPDB, ThreatIntel for the involved IPs — attach results to the ticket
2. **Alert de-duplication:** Automatically identify and close duplicate alerts (same signature, same host, within 30 minutes)
3. **Known good suppression:** Automatically close alerts from known-legitimate sources (vulnerability scanner, IT admin tool) — track suppression in a log
4. **Phishing triage (initial):** Parse the email, extract URLs and attachments, check against VirusTotal, generate a risk score — analyst gets pre-analysed results
5. **Blocking known-bad IPs:** When an alert fires on a confirmed malware C2 IP, automatically add the IP to the firewall blocklist within 30 seconds

**Must involve a human:**
1. **Host isolation decision:** Taking a server offline could impact critical business operations — a human must assess the business impact first
2. **Escalation to law enforcement:** Legal decisions require human judgment and approval
3. **Communications to customers/regulators:** Breach notifications have legal implications — must have legal/management sign-off

---

**Q14.** Write an ELK (Elasticsearch/Kibana) query to find all Windows logon events (Event 4624) where the logon type was RemoteInteractive (RDP, type 10) outside of business hours (before 8am or after 6pm).

**Answer:**
```json
GET winlogbeat-*/_search
{
  "query": {
    "bool": {
      "must": [
        {"term": {"winlog.event_id": 4624}},
        {"term": {"winlog.event_data.LogonType": "10"}}
      ],
      "filter": [
        {
          "script": {
            "script": {
              "source": "int hour = doc['@timestamp'].value.getHour(); return hour < 8 || hour >= 18;"
            }
          }
        }
      ]
    }
  },
  "aggs": {
    "by_user": {
      "terms": {"field": "winlog.event_data.TargetUserName.keyword"},
      "aggs": {
        "by_source_ip": {
          "terms": {"field": "winlog.event_data.IpAddress.keyword"}
        }
      }
    }
  }
}
```

---

**Q15.** Explain the difference between reactive and proactive security monitoring. Give an example of each and explain why a mature SOC needs both.

**Answer:**
**Reactive monitoring:** Responding to alerts generated by rules. Something happens → rule detects it → alert fires → analyst investigates. Dependent on having a rule for the specific threat. You can only detect what you have a rule for.

Example: Firewall blocks a known malware C2 IP → alert fires → analyst confirms and closes. Reactive response is fast and automated but blind to novel attacks.

**Proactive monitoring (threat hunting):** Analysts proactively search for indicators of compromise or attacker behaviour, even without a rule firing. Hypothesis-driven: "Given the recent news about APT41 targeting our industry using living-off-the-land techniques, let me search for unusual PowerShell usage in our environment."

Example: Hunter writes query searching for processes that spawned cmd.exe with network connections, finds two cases of legitimate admin tools and one unknown process that spawned a suspicious shell — no rule would have caught this.

**Why both are needed:** Reactive is your first line — it catches known threats automatically at scale. Proactive catches unknown threats and builds better reactive rules over time. Without hunting, attackers can live in your network for months using techniques that don't trigger rules. Without reactive, analysts are overwhelmed trying to manually find everything.

---

## Section C: Incident Triage Scenarios (Questions 16-20)

**Q16.** At 3:17am, your SIEM fires: "Scheduled task created on DC01 (Domain Controller) — task name: 'WindowsUpdateHelper', runs C:\Windows\Temp\svchost32.exe, triggered at system startup." Classify this alert and describe your immediate response.

**Answer:** **Classification: HIGH PRIORITY — Potential APT Persistence / Domain Compromise.**

Red flags: (1) Scheduled task on a Domain Controller — DCs should rarely have new scheduled tasks added, (2) Path `C:\Windows\Temp\` — legitimate Windows binaries live in `C:\Windows\System32\`, not Temp, (3) `svchost32.exe` — the real Windows file is `svchost.exe` (no "32"); this naming is a common evasion technique to blend in, (4) 3:17am creation — outside business hours.

**Immediate response:**
1. Check if `C:\Windows\Temp\svchost32.exe` exists on DC01 — what is its SHA256 hash?
2. Search VirusTotal for the hash
3. Check process creation logs — what process created this scheduled task? (Sysmon Event 1 → parent process of `schtasks.exe`)
4. Query all other DCs for the same file and scheduled task
5. Do NOT delete the file yet — collect forensic evidence first (memory dump if possible)
6. Immediately escalate to L3/DFIR — this pattern indicates a likely domain compromise

---

**Q17.** You are reviewing a Splunk search result and see:
```
Host: WS-FINANCE-01
User: jsmith
Time: 14:23 to 15:47 (84 minutes)
Events:
  14:23 - net user administrator /active:yes (4688)
  14:25 - net localgroup administrators jsmith /add (4688)
  14:30 - whoami /all (4688)
  14:35 - ipconfig /all (4688)
  14:40 - net view (4688)
  15:01 - dir \\\\fileserver\\finance\\accounts (4688)
  15:30 - xcopy \\\\fileserver\\finance\\accounts C:\temp /e /y (4688)
  15:47 - powershell.exe -enc JABjAG0AZAAgAD0AIA... (4688)
```
What MITRE ATT&CK techniques are being used? Is this a real incident?

**Answer:** This is almost certainly a **real incident** — a threat actor who has compromised jsmith's credentials on WS-FINANCE-01 is now:

| Action | MITRE ATT&CK |
|--------|-------------|
| `net user administrator /active:yes` | T1098 — Account Manipulation (enabling built-in admin) |
| `net localgroup administrators jsmith /add` | T1078 — Valid Accounts + T1098 — Account Manipulation |
| `whoami /all`, `ipconfig /all`, `net view` | T1033/T1016/T1135 — System Owner Discovery, Network Discovery |
| `dir \\fileserver\finance\accounts` | T1083 — File and Directory Discovery |
| `xcopy` to `C:\temp` | T1074 — Data Staged (staging data for exfiltration) |
| `powershell.exe -enc` | T1059.001 — Command and Scripting Interpreter + T1140 — Deobfuscate |

**Immediate response:** (1) Isolate WS-FINANCE-01 from the network, (2) Disable jsmith's AD account, (3) Reset built-in administrator password on the host, (4) Identify what was in `C:\temp` — was it exfiltrated? Check network logs at 15:30-15:47 for outbound transfers, (5) Check if jsmith's account was used on any other hosts in this timeframe, (6) Declare incident and engage IR team.

---

**Q18.** Write a threat hunting query in Splunk to detect "living off the land" binary (LOLBin) abuse — specifically, looking for legitimate Windows tools being used to make unusual network connections.

**Answer:**
```spl
# LOLBin network connection detection
# These Windows binaries should rarely make external network connections
index=sysmon EventID=3  
| eval lolbin = case(
    match(Image, "(?i)\\\\(regsvr32|certutil|mshta|rundll32|wscript|cscript|bitsadmin|msiexec|wmic|cmd|powershell)\.exe$"), 
    lower(replace(Image, ".*\\\\", "")), 
    true(), null()
)
| where isnotnull(lolbin)
| where NOT match(DestinationIp, "^(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.|127\.)")
| stats count, values(DestinationIp) as external_ips, 
         values(CommandLine) as cmds, 
         values(ParentImage) as parents 
  by Computer, User, lolbin
| sort -count
| where count < 5  # low count = more suspicious (high count = likely legitimate scheduled scan)
```

**Hunting hypothesis:** Attackers use legitimate Windows binaries (`certutil`, `mshta`, `regsvr32`) to download payloads or phone home to C2. These tools are trusted by AV but have no business reason to connect to random external IPs.

---

**Q19.** You are given the following SIEM alert to investigate. Write the investigation plan including all SIEM queries you would run:

"Alert: Exfiltration Suspected — Host WEB-PROD-02 sent 4.2GB to IP 104.21.65.100 (Cloudflare) over 3 hours via HTTPS (port 443)"

**Answer:**
**Initial thought:** 4.2GB is large, but Cloudflare proxies thousands of legitimate sites. Could be legitimate file backup/sync (OneDrive, Dropbox, SharePoint all use Cloudflare IPs).

**Investigation queries:**
```spl
# 1. Is 4.2GB unusual for this host? (Baseline)
index=network src_host=WEB-PROD-02
| timechart sum(bytes_out) span=1d
| eval gb = bytes_out / 1073741824

# 2. What other IPs did this host talk to today?
index=network src_host=WEB-PROD-02 earliest=-24h
| stats sum(bytes_out) as total_bytes, count as connections by dest_ip
| sort -total_bytes

# 3. What process initiated these connections? (Sysmon)
index=sysmon EventID=3 Computer=WEB-PROD-02 DestinationIp=104.21.65.100
| table _time Image CommandLine ParentImage User

# 4. Any sensitive file access before the transfer?
index=sysmon EventID=11 Computer=WEB-PROD-02 earliest=-3h
| where like(TargetFilename, "%.csv%") OR like(TargetFilename, "%.sql%") OR like(TargetFilename, "%.xls%")
| table _time User TargetFilename

# 5. DNS lookups by this host in the same period (what domain is 104.21.65.100?)
index=dns src_host=WEB-PROD-02 earliest=-4h
| stats count by query | sort -count
```

**Decision:** If the process is a known backup agent (Veeam, Azure Backup) and the destination domain (from DNS logs) is a known cloud storage provider → likely FP, close with documentation. If the process is unusual, or the domain is unknown/recently registered → escalate as potential exfiltration.

---

**Q20.** Write a Splunk scheduled search that automatically creates an alert ticket when it detects a user account that has been inactive for 90 days and then suddenly logs in. Explain why this detection matters.

**Answer:**
```spl
# Find accounts with 90+ day gap between last and current login
index=windows EventCode=4624 earliest=-24h
| stats max(_time) as last_login by Account_Name

# Join against historical login data to find previous login
| join type=inner Account_Name [
    search index=windows EventCode=4624 earliest=-180d latest=-90d
    | stats max(_time) as prev_login by Account_Name
]

| eval days_dormant = round((last_login - prev_login) / 86400, 0)
| where days_dormant >= 90

| eval alert_message = Account_Name + " logged in after " + toString(days_dormant) + " days of inactivity"
| table Account_Name last_login prev_login days_dormant alert_message
```

**Why this matters:** Dormant accounts are a classic attacker persistence technique:
1. Attacker compromises an unused service account with no MFA
2. The account sits unused for months — no one notices activity because no one expected it
3. When the attacker needs to return, they log in using the dormant account
4. A dormant account suddenly active is a strong indicator of attacker use, not legitimate user activity — employees on leave or who left the company shouldn't be authenticating

---

## Section D: Threat Intelligence and Reporting (Questions 21-25)

**Q21.** Explain the Pyramid of Pain (David Bianco). Which indicators are hardest for attackers to change? How should this influence your detection strategy?

**Answer:** The Pyramid of Pain ranks IoCs by how difficult they are for attackers to change if you detect and block them:

```
     [Hardest]
     TTPs — Techniques, Tactics, Procedures (behavioural patterns)
     Tools — Specific malware/tool signatures
     Network/Host Artefacts — Registry keys, filenames in specific paths
     Domain Names — C2 domains
     IP Addresses — C2 server IPs
     Hash Values — Specific file hashes
     [Easiest]
```

**Bottom of pyramid (easy for attackers):** Hash values — attacker recompiles code with one different byte → entirely new hash. IP addresses — attacker rents a new VPS for £5. Blocking these is reactive and requires constant updates.

**Top of pyramid (hard for attackers):** TTPs — if you detect the behaviour pattern "certutil downloading executable from internet then running it with regsvr32", the attacker must fundamentally change their operational approach — retrain, rebuild tooling. Blocking TTPs is expensive for the attacker.

**Detection strategy implication:** Invest most in TTP-based detections (behaviour, not indicators). Don't ignore hashes/IPs (they're still useful for quick wins), but don't rely on them exclusively — attackers rotate them trivially.

---

**Q22.** Write a Python script that queries the Shodan API to get information about an IP address involved in a security incident.

**Answer:**
```python
import shodan, json

def investigate_ip(ip: str, api_key: str) -> dict:
    """Query Shodan for open ports, services, and vulnerabilities for an IP."""
    api = shodan.Shodan(api_key)
    
    try:
        host = api.host(ip)
    except shodan.APIError as e:
        return {"error": str(e), "ip": ip}
    
    summary = {
        "ip": ip,
        "country": host.get('country_name', 'Unknown'),
        "org": host.get('org', 'Unknown'),
        "isp": host.get('isp', 'Unknown'),
        "last_update": host.get('last_update', 'Unknown'),
        "open_ports": [],
        "vulns": host.get('vulns', []),
        "hostnames": host.get('hostnames', []),
        "tags": host.get('tags', [])  # tor, vpn, cloud, etc.
    }
    
    for service in host.get('data', []):
        port_info = {
            "port": service['port'],
            "transport": service.get('transport', 'tcp'),
            "service": service.get('product', ''),
            "version": service.get('version', '')
        }
        if 'http' in service:
            port_info['http_title'] = service['http'].get('title', '')
        summary['open_ports'].append(port_info)
    
    return summary

# Usage (sign up at shodan.io for free API key)
# result = investigate_ip("185.220.101.100", "YOUR_API_KEY")
# print(json.dumps(result, indent=2))
# 
# Look for: is it a Tor exit node? VPN provider? Cloud hosting?
# What ports are open? A C2 server often has port 4444, 8080, or custom ports open
# Any known CVEs (vulns field)?
```

---

**Q23.** What is threat intelligence sharing? Explain STIX and TAXII and how they enable automated threat intel sharing between organisations.

**Answer:**
**Threat intelligence sharing:** Organisations share indicators (IPs, domains, hashes) and TTPs so defenders can proactively block threats that have targeted other organisations.

**STIX (Structured Threat Information eXpression):** A standardised language for describing cyber threat information. Defines objects (Indicator, Campaign, Threat Actor, Malware, Attack Pattern, etc.) and relationships between them in JSON format.

```json
{
  "type": "indicator",
  "id": "indicator--8e2e2d2b-17d4-4cbf-938f-98129f1cd1c7",
  "name": "Malicious URL",
  "indicator_types": ["malicious-activity"],
  "pattern": "[url:value = 'http://malicious.example.com/payload']",
  "valid_from": "2024-01-01T00:00:00Z"
}
```

**TAXII (Trusted Automated eXchange of Indicator Information):** The transport protocol for sharing STIX data. Defines API endpoints (Collection, Channel) for publishing and subscribing to threat intelligence feeds.

**How it works in practice:**
1. CERT-In detects a new malware campaign and creates STIX indicators
2. They publish to their TAXII server
3. Your SIEM has a TAXII connector that automatically pulls new indicators every hour
4. The indicators are automatically imported into your blocklists and detection rules
5. You are now protected from that campaign within an hour — without any analyst effort

**Example feeds:** MISP (open source threat sharing platform), AlienVault OTX, FS-ISAC (financial sector), Mandiant Advantage.

---

**Q24.** Calculate the following SOC metrics from this data and explain what each tells you about SOC performance:
- 100 alerts generated this week
- 78 closed as false positives
- 22 confirmed true positives
- Average time from alert to ticket: 8 minutes
- Average time from ticket to closure: 4.5 hours for P2, 12 hours for P3
- SLA: P2 must be closed within 4 hours

**Answer:**
**Calculations:**
- **False Positive Rate:** 78/100 = 78%. High FP rate — significant tuning opportunity. Industry benchmark: aim for <50% for mature rules.
- **True Positive Rate (Precision):** 22/100 = 22%. Only 1 in 5 alerts is real — analyst effort is heavily wasted on FPs.
- **MTTD (Mean Time to Detect):** Not directly calculable from this data — would need time from attacker entry to first alert. The 8-minute alert-to-ticket time is "Mean Time to Acknowledge" (MTTA), not MTTD.
- **MTTA (Mean Time to Acknowledge):** 8 minutes — good. Industry benchmark: <15 minutes for P2.
- **MTTR for P2:** 4.5 hours. **SLA BREACH** — P2 SLA is 4 hours. 30 minutes over target.
- **MTTR for P3:** 12 hours — reasonable for lower priority.

**Actions:** (1) Tune rules to reduce 78% FP rate — pick top 10 highest-volume FP rules and add exclusions, (2) Investigate P2 MTTR — is it analyst capacity? Complexity? Tool access issues? Add 30 minutes buffer or improve playbooks to meet SLA.

---

**Q25.** You are presenting the SOC's monthly security report to the CISO. What are the 6 key metrics you include, what do each mean to a non-technical executive, and how do you visualise them?

**Answer:**

| Metric | What to say to CISO | Visualisation |
|--------|---------------------|--------------|
| **MTTD (avg 4.2 days)** | "On average, it takes us 4.2 days to detect an attacker after they enter our network. Industry average is 16 days — we're significantly better." | Single number with trend arrow + industry benchmark line |
| **MTTR P1 (avg 45 min)** | "When a critical incident occurs, our team contains it in 45 minutes on average." | Gauge chart with SLA target (60 min) |
| **Alert-to-True-Positive rate (22%)** | "78% of our automated alerts turn out to be harmless — we're working to improve this so analysts spend time on real threats." | Donut chart: TP vs FP vs TN |
| **Incident count by category** | "This month we had 3 malware incidents, 1 data access violation, and 2 policy violations — down from 8 last month." | Bar chart by category with month-over-month comparison |
| **Mean Dwell Time** | "The one confirmed breach this month was detected within 2 hours — significantly below our 24-hour target." | Timeline showing compromise → detect → contain |
| **Top attack vectors** | "Phishing was the initial vector in 70% of incidents this month — we recommend targeted training for Finance and HR departments." | Pie chart with recommendation callout |

**Presentation tip:** Don't present raw log counts or technical alert details. Present business risk: "we detected X incidents, these were the potential impacts, we responded in Y time, here's the trend, here's what we need."
