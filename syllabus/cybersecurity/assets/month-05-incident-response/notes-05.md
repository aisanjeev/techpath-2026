# Month 5 — Quick Revision Notes: Incident Response & Threat Intelligence

## NIST Incident Response Lifecycle

| Phase | Goal | Key Activities |
|-------|------|---------------|
| **1. Prepare** | Be ready before incidents occur | IR plan, runbooks, tool deployment, training |
| **2. Identify** | Detect and confirm an incident | Alert triage, initial investigation, severity assessment |
| **3. Contain** | Stop the spread | Network isolation, account lockout, firewall block |
| **4. Eradicate** | Remove the threat | Malware removal, patch CVE, close access |
| **5. Recover** | Restore normal operations | System rebuild, credential reset, monitoring uplift |
| **6. Learn** | Prevent recurrence | Post-incident review, playbook update, detection rule improvement |

## Chain of Custody — Key Requirements

- **Document everything**: who collected evidence, when, where, chain of custody form
- **Hash the evidence**: record SHA-256 before and after any copy
- **Write-block**: use hardware or software write-blocker to prevent modifying originals
- **Store securely**: evidence must be tamper-evident (sealed bag, locked storage)
- **Access log**: record every person who accessed evidence and for what purpose

```
Evidence Item → SHA256 calculated → Forensic copy made → Original sealed
                                          ↓
                                 Work on forensic copy only
```

## Volatility 3 — Essential Commands

```bash
# List running processes (plain list)
python vol.py -f memory.dmp windows.pslist.PsList

# Process tree with parent-child relationships
python vol.py -f memory.dmp windows.pstree.PsTree

# Command-line arguments for each process
python vol.py -f memory.dmp windows.cmdline.CmdLine

# Active and closed network connections
python vol.py -f memory.dmp windows.netstat.NetStat

# Find code injection / suspicious memory regions
python vol.py -f memory.dmp windows.malfind.Malfind

# Dump a process to disk for further analysis
python vol.py -f memory.dmp windows.dumpfiles.DumpFiles --pid 1234

# List loaded DLLs per process
python vol.py -f memory.dmp windows.dlllist.DllList

# Scan for running services
python vol.py -f memory.dmp windows.svcscan.SvcScan

# Detect hidden processes (cross-reference methods)
python vol.py -f memory.dmp windows.psscan.PsScan
```

## Autopsy — Key Analysis Modules

| Module | What It Finds |
|--------|-------------|
| Recent Activity | Browser history, downloads, recent files, recycle bin |
| Hash Lookup | Matches against NSRL (clean) and custom malware hash sets |
| File Type ID | Finds files disguised with wrong extensions |
| Keyword Search | Searches for text strings across unallocated and allocated space |
| Timeline Analysis | Reconstructs file system activity as a chronological timeline |
| Email Parser | Extracts email artifacts from .pst, .eml, Thunderbird profiles |
| Registry Analysis | Examines registry hives for persistence mechanisms, user activity |
| Data Carving | Recovers deleted files from unallocated space |

## Sysmon — Critical Event IDs

| Sysmon ID | Meaning | Why It Matters |
|-----------|---------|----------------|
| 1 | Process creation | Full command line + hash — detects LOLBins, suspicious launches |
| 2 | File creation time changed | File timestomping (defense evasion) |
| 3 | Network connection | Outbound connections per process — C2 detection |
| 7 | Image loaded | DLL hijacking, unsigned DLL loads |
| 8 | Create remote thread | Process injection (T1055) |
| 10 | Process access | LSASS access — credential dumping |
| 11 | File created | Dropped payloads, new executables |
| 12/13 | Registry event | Persistence via run keys, CLSID hijacking |
| 15 | File stream created | MOTW bypass, ADS abuse |
| 22 | DNS query | C2 DNS resolution — matches process to domain |

## Threat Intelligence Hierarchy

```
Pyramid of Pain (from easiest to change to hardest):

Hash values         ← Trivial for attacker to change
IP addresses        ← Easy to rotate (VPS, VPN)
Domain names        ← Harder but still cheap
Network artefacts   ← Specific TLS certs, user agents
Host artefacts      ← Registry keys, file paths
Tools               ← Recompile costs time
TTPs                ← Changing behaviour = most expensive for attacker
```

## Threat Intelligence Sources

| Platform | Type | Key Use |
|----------|------|---------|
| VirusTotal | File/URL/IP analysis | Quick hash/URL check against 70+ AV engines |
| AlienVault OTX | Community threat feeds | IOC feeds: IPs, domains, hashes, YARA rules |
| MISP | Threat intel sharing | Share IOCs across orgs; self-hosted or cloud |
| OpenCTI | Structured CTI platform | Store and visualise TTPs, campaigns, actors |
| Shodan | Attack surface intel | Find attacker infrastructure exposed on internet |
| AbuseIPDB | IP reputation | Check if IP has been reported for abuse |

## Velociraptor — Key Concepts

- **Enterprise-scale** endpoint visibility and forensic collection tool (free, open source)
- Uses a **client-agent** deployed to endpoints reporting to a central server
- **VQL** (Velociraptor Query Language) for artefact collection
- Pre-built **artefacts** for common IR tasks: process listing, network connections, file timeline
- Hunt across **thousands of endpoints simultaneously**

```vql
-- Collect suspicious network connections
SELECT * FROM netstat() WHERE remote_port in (4444, 1337, 8080)

-- Find recently created executables
SELECT * FROM find(path="C:/", glob="**/*.exe") WHERE Mtime > now() - 86400
```

## IR Documentation Template

```
INCIDENT ID: INC-2026-001
Severity:    High
Analyst:     [Name]
Start Time:  2026-08-03 14:00 UTC

TIMELINE:
  14:00 - Alert received: repeated failed RDP from 185.x.x.x
  14:10 - Confirmed TP: same IP succeeded at 13:58
  14:20 - Endpoint isolated, account disabled
  14:45 - Memory dump acquired from affected host
  15:30 - Malware identified: Cobalt Strike beacon in lsass.exe
  16:00 - Eradication: AV scan + reimaging started

IOCS:
  IP: 185.220.101.47 (C2)
  Hash: a3b2c1... (payload.dll)
  Domain: update-service[.]com

MITRE:
  T1566.001 Phishing attachment (initial access)
  T1055 Process injection → LSASS
  T1071.001 HTTP C2
```
