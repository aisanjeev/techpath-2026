# Month 6 — Practice Exercises: Detection Engineering

**25 exercises with worked answers.**

---

## Section A: Sigma Rules (Questions 1-8)

**Q1.** Write a complete Sigma rule to detect the Kerberoasting technique (T1558.003). A Kerberoasting attack will generate Windows Event 4769 with encryption type 0x17 (RC4) and ticket options 0x40800000.

**Answer:**
```yaml
title: Kerberoasting Activity Detected
id: 4a3f71a5-6b3c-4d8e-9f20-a1b2c3d4e5f6
status: stable
description: Detects Kerberoasting — requesting Kerberos service tickets using RC4 encryption
  which is the default for cracking. Legitimate services use AES (0x12 or 0x18).
references:
  - https://attack.mitre.org/techniques/T1558/003/
  - https://adsecurity.org/?p=3458
author: Detection Engineering Team
date: 2024/01/15
tags:
  - attack.credential_access
  - attack.t1558.003
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4769                          # Kerberos service ticket requested
    TicketEncryptionType: '0x17'           # RC4-HMAC — weak, used for offline cracking
    TicketOptions: '0x40800000'            # Typical Kerberoasting ticket options
  filter_computer_accounts:
    AccountName|endswith: '$'              # Exclude computer accounts (normal RC4 usage)
  filter_krbtgt:
    ServiceName: 'krbtgt'                  # Exclude normal TGT requests
  condition: selection and not 1 of filter_*
falsepositives:
  - Legacy applications that don't support AES Kerberos encryption
  - Older services configured with RC4 — investigate and upgrade to AES
level: high
```

---

**Q2.** Convert the following Sigma rule to Splunk SPL and KQL (Microsoft Sentinel) using the correct field name mappings for Windows Security events.

```yaml
detection:
  selection:
    EventID: 4720
    SubjectUserName|not|endswith: '$'
  condition: selection
```

**Answer:**
**Splunk SPL:**
```spl
index=windows source="WinEventLog:Security" EventCode=4720
NOT SubjectUserName="*$"
| table _time Computer SubjectUserName TargetUserName
```

**KQL (Microsoft Sentinel):**
```kql
SecurityEvent
| where EventID == 4720
| where SubjectUserName !endswith "$"
| project TimeGenerated, Computer, SubjectUserName, TargetUserName, TargetSid
| order by TimeGenerated desc
```

**Field name mapping for Windows Event 4720 (Account Created):**

| Sigma field | Splunk field | KQL field |
|------------|-------------|----------|
| EventID | EventCode | EventID |
| SubjectUserName | SubjectUserName | SubjectUserName |
| TargetUserName | TargetUserName (new account) | TargetUserName |
| Computer | ComputerName | Computer |

---

**Q3.** Write a Sigma rule to detect "living off the land" (LOLBin) abuse — specifically, `certutil.exe` being used to decode a Base64-encoded file or download from a URL.

**Answer:**
```yaml
title: CertUtil Abuse — Decoding or Downloading Files
id: 2a3b4c5d-6e7f-8a9b-0c1d-2e3f4a5b6c7d
status: stable
description: >
  Detects certutil.exe being used to decode Base64 files or download content from URLs.
  Certutil is a Windows built-in tool commonly abused by attackers to download payloads
  (LOLBin technique). Legitimate certutil usage manages certificate services.
references:
  - https://attack.mitre.org/techniques/T1140/
  - https://attack.mitre.org/techniques/T1105/
  - https://lolbas-project.github.io/lolbas/Binaries/Certutil/
author: Detection Engineering
date: 2024/01
tags:
  - attack.defense_evasion
  - attack.t1140
  - attack.command_and_control
  - attack.t1105
logsource:
  category: process_creation
  product: windows
detection:
  selection_img:
    Image|endswith: '\certutil.exe'
  selection_decode:
    CommandLine|contains|any:
      - '-decode'
      - '-urlcache'
      - '-verifyctl'    # Also abused to download
      - '-f '           # Force flag — often paired with download
  filter_legitimate:
    CommandLine|contains:
      - 'CertSvc'       # Certificate Services management
      - 'CertStore'
  condition: selection_img and selection_decode and not filter_legitimate
falsepositives:
  - IT teams using certutil for legitimate certificate management
  - Should be very rare in normal environments
level: high
```

---

**Q4.** You write a Sigma rule that generates 500 alerts per day, and 490 of them are false positives. Describe your tuning process to reduce the FP rate to below 20%.

**Answer:**
**Step 1 — Understand the false positives**
```bash
# Convert rule and run in Splunk, examine FP results
# Sample 20-30 false positive alerts and look for common patterns
```

Questions to ask:
- What HOSTS are generating FPs? (Specific servers, vulnerability scanners?)
- What USERS are generating FPs? (IT admins, service accounts?)
- What PARENT PROCESSES are generating FPs? (Legitimate software?)
- What COMMAND LINE patterns appear in FPs but not in TPs?

**Step 2 — Add targeted exclusions to Sigma**
```yaml
# Example: if 80% of FPs come from a specific admin tool
filter_admin_tool:
  ParentImage|endswith: '\admin_tool.exe'
  
# If FPs come from specific hosts
filter_known_hosts:
  ComputerName|startswith:
    - 'SCANNER-'
    - 'VULN-'

# If FPs have a specific path pattern
filter_legitimate_path:
  Image|startswith: 'C:\Program Files\Legitimate\'
```

**Step 3 — Raise the specificity threshold**
Add condition requirements that make the rule fire only on stronger indicators:
```yaml
# Before: any certutil decode
detection:
  selection: CommandLine|contains: '-decode'

# After: certutil decode + output to temp directory (more specific)
detection:
  selection:
    CommandLine|contains: '-decode'
    CommandLine|contains|any:
      - '\Temp\'
      - '\AppData\'
      - '\Downloads\'
```

**Step 4 — Validate each exclusion** — run the rule with and without each filter. Verify the exclusion doesn't suppress real TPs.

**Step 5 — Document the exclusions** in the rule's `falsepositives:` field so future engineers understand why they're there.

---

**Q5.** Write a Sigma rule for detecting suspicious scheduled task creation where the task's action points to a location that is unusual for legitimate tasks.

**Answer:**
```yaml
title: Suspicious Scheduled Task Created with Unusual Execution Path
id: 7c8d9e0f-1a2b-3c4d-5e6f-7a8b9c0d1e2f
status: experimental
description: >
  Detects creation of scheduled tasks that execute files from unusual locations
  (temp directories, user profiles, AppData). Attackers use scheduled tasks for
  persistence and often place malware in these locations to avoid detection.
references:
  - https://attack.mitre.org/techniques/T1053/005/
author: Detection Engineering
date: 2024/01
tags:
  - attack.persistence
  - attack.t1053.005
logsource:
  product: windows
  service: security
detection:
  selection:
    EventID: 4698          # Scheduled task created
    TaskContent|contains|any:
      - '\AppData\Local\Temp'
      - '\AppData\Roaming'
      - '\Users\Public'
      - '\Windows\Temp'
      - 'C:\Temp'
      - '%TEMP%'
      - '%APPDATA%'
  filter_known_legit:
    TaskName|contains|any:
      - 'MicrosoftEdge'
      - 'GoogleUpdate'
      - 'OneDrive'
  condition: selection and not filter_known_legit
falsepositives:
  - Some legitimate software installers temporarily use temp paths
  - Investigate and whitelist if confirmed legitimate
level: high
```

---

**Q6.** What is the SigmaHQ GitHub repository? Explain how to use it as a SOC analyst and how to contribute back to it.

**Answer:** github.com/SigmaHQ/sigma is the community repository of Sigma detection rules — the largest free collection of detection content. It contains thousands of rules organised by OS, product, and ATT&CK technique.

**Using as a SOC analyst:**
```bash
# Clone the repository
git clone https://github.com/SigmaHQ/sigma.git
cd sigma

# Browse rules by category
ls rules/windows/process_creation/    # Windows process-based detections
ls rules/cloud/aws/                   # AWS detections
ls rules/linux/                       # Linux detections

# Convert all Windows process creation rules to Splunk
sigma convert -t splunk -p windows/sysmon \
    rules/windows/process_creation/ \
    --output splunk_rules.txt

# Filter by ATT&CK technique
grep -r "t1059.001" rules/ --include="*.yml" -l  # List all PowerShell rules

# Filter by severity
grep -r "level: critical" rules/ --include="*.yml" -l
```

**Contributing back:**
1. Write a new rule following the Sigma schema exactly
2. Test it (convert + run against real logs; verify TP fires and no obvious FP)
3. Fork the SigmaHQ/sigma repository on GitHub
4. Add your rule to the appropriate category folder
5. Submit a Pull Request with:
   - Description of what the rule detects
   - ATT&CK mapping
   - How you tested it
   - Known false positive sources
6. Community review (maintainers + other contributors) — typically 1-2 week review cycle

---

**Q7.** Explain what "detection drift" is and how to prevent it in a SOC detection programme.

**Answer:** **Detection drift** occurs when detection rules become less effective over time because: the environment changes (new software added that triggers FPs), attackers change their TTPs (update malware to evade your rule), log sources change format (vendor update breaks field names), or new legitimate admin activity matches the detection.

**Consequences:** Rules that were effective 6 months ago may now generate so many FPs that analysts ignore them, or may miss new attack variants.

**Prevention:**
1. **Quarterly rule review process:** For every rule, check: current FP rate, last time it detected a real TP, whether it still covers the relevant ATT&CK technique, whether the fields it queries still exist in your log source
2. **Version control for detection content:** Store rules in Git. Track changes, see history, roll back bad changes.
3. **Detection testing pipeline:** Use Atomic Red Team or DetectionLab to run simulated attacks against your detection rules regularly — automated regression tests.
4. **ATT&CK Navigator coverage review:** Quarterly review of which techniques are covered vs not, as new techniques are added to ATT&CK.
5. **Threat intelligence correlation:** When new threat intel arrives about an active campaign in your industry, immediately check if existing rules cover their TTPs.

---

**Q8.** A colleague suggests "we should just import all 3,000 Sigma rules from the SigmaHQ repository into our SIEM at once." What problems would this create? What approach would you recommend instead?

**Answer:** Problems with importing all 3,000 rules at once:

1. **Alert storm:** Thousands of rules firing simultaneously would generate an unmanageable volume of alerts, overwhelming analysts and defeating the purpose of the SIEM
2. **Irrelevant rules:** Many rules target technologies you don't use (Cisco, Palo Alto, specific cloud services) — they'll fire FPs or simply never match your log sources
3. **Unmaintained FP hell:** Each rule has its own FP profile unique to your environment. Without tuning, analysts lose trust in alerts.
4. **Performance impact:** Thousands of complex searches running continuously puts heavy load on your SIEM
5. **No prioritisation:** Not all detections are equally important. An "informational" rule gets same attention as a "critical" rule.

**Recommended approach:**
1. **Start with the highest-value rules:** Filter by `level: critical` and `level: high` only — typically 300-400 rules
2. **Filter by your technology stack:** Only import rules for Windows (if you're a Windows shop), the cloud platform you use, etc.
3. **Prioritise by ATT&CK coverage gaps:** Run a coverage analysis — where do you have zero detection? Import rules for those techniques first.
4. **Deploy in batches of 20-30:** Monitor FP rate for each batch before adding the next. Tune before adding more.
5. **Set up a staging environment:** Test rules against historical logs before deploying to production — see what fires before it's in front of analysts.

---

## Section B: YARA Rules (Questions 9-13)

**Q9.** Write a YARA rule to detect CobaltStrike Beacon based on its default configuration and known byte patterns.

**Answer:**
```yara
rule CobaltStrike_Beacon_Default {
    meta:
        description = "Detects CobaltStrike Beacon — common APT post-exploitation framework"
        author = "Detection Engineering"
        date = "2024-01"
        reference = "https://github.com/MichaelKoczwara/Awesome-CobaltStrike-Defence"
        severity = "critical"
        tags = "cobalt strike, beacon, rat, apt"
    
    strings:
        // CobaltStrike Beacon default sleep/jitter config markers
        $config_marker = { 2E 2F 2E 2F 2E 2C }    // Default XOR key marker
        
        // HTTP beacon URIs (default profiles)
        $uri1 = "/updates.rss" ascii
        $uri2 = "/dpixel" ascii
        $uri3 = "__utm.gif" ascii
        $uri4 = "/cx" ascii
        
        // Known shellcode patterns
        $shellcode1 = { FC E8 89 00 00 00 60 89 E5 31 D2 64 8B 52 30 }
        $shellcode2 = { FC E8 82 00 00 00 60 89 E5 31 C0 64 8B 50 30 }
        
        // Named pipe patterns (Cobalt Strike default)
        $pipe1 = "\\pipe\\msagent_" wide
        $pipe2 = "\\pipe\\MSSE-" wide
        
        // Default user agents
        $ua1 = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)" ascii
        $ua2 = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727)" ascii
        
    condition:
        (
            1 of ($shellcode*) and
            (1 of ($uri*) or 1 of ($pipe*))
        ) or
        (
            2 of ($uri*) and 1 of ($ua*)
        ) or
        $config_marker
}
```

---

**Q10.** Explain the difference between YARA string types: plain text, hex, and regex. Give an example of when each type is most appropriate.

**Answer:**
**Plain text strings:** ASCII or Unicode text matching. Most readable, fast to scan.
```yara
$s1 = "sekurlsa::logonpasswords" nocase  // Match regardless of case
$s2 = "CreateRemoteThread" ascii wide    // Match both ASCII and Unicode (Windows APIs)
```
**Best for:** Tool author strings, error messages, URLs, API function names — any human-readable text.

**Hex strings:** Match raw bytes. Use wildcards (`??`) and jumps (`[N-M]`) for flexibility.
```yara
// PE magic bytes at offset 0 (every Windows executable starts with MZ = 4D 5A)
$mz_header = { 4D 5A }
// XOR key + byte sequence with 2 wildcard bytes
$xor_pattern = { EB ?? 5B 53 ?? ?? ?? 00 }
// Jump of 4-8 bytes between known values
$gap_pattern = { DE AD BE EF [4-8] CA FE BA BE }
```
**Best for:** Binary data patterns, shellcode signatures, version-independent byte sequences, crypto constants.

**Regex strings:** Full regular expression matching. Most powerful but slowest to scan.
```yara
// Match any IPv4 address in the binary
$ip_regex = /\b(?:\d{1,3}\.){3}\d{1,3}\b/
// Match base64-encoded data blocks (often used to encode payloads)
$b64_regex = /[A-Za-z0-9+\/]{40,}={0,2}/
// Match registry persistence path
$reg_regex = /SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run/i
```
**Best for:** Variable patterns (URLs with changing domains), data format detection (base64, encoded strings), anything requiring character classes or quantifiers.

---

**Q11.** A YARA rule for detecting a banking trojan is generating false positives on legitimate banking software. Walk through the debugging and tuning process.

**Answer:**
**Step 1 — Identify which strings are matching in the FP:**
```python
import yara

rules = yara.compile('banking_trojan.yar')
# Scan the legitimate banking software
matches = rules.match('/path/to/legitimate_banking_app.exe')
for match in matches:
    print(f"Matched: {match.rule}")
    for string in match.strings:
        print(f"  String '{string.identifier}' at offset {string.instances[0].offset}: {string.instances[0].matched_data[:50]}")
```

**Step 2 — Analyse which specific strings triggered the FP:**
Example: the string `$s1 = "POST /login"` triggered because the legitimate banking app also uses HTTP POST to `/login`. This string is too generic.

**Step 3 — Increase specificity:**
```yara
// Too generic — matches any POST request
$generic = "POST /login"

// More specific — combine with other patterns unique to the trojan
$specific1 = "POST /gate.php"  // Trojan-specific endpoint
$specific2 = { 67 61 74 65 2E 70 68 70 }  // "gate.php" in hex
```

**Step 4 — Add explicit exclusions:**
```yara
rule BankingTrojan_Zeus {
    strings:
        $s1 = "gate.php" nocase
        $s2 = "bot_id=" nocase
        $s3 = { 83 EC 30 53 55 56 57 8B F9 }  // ZeuS-specific code pattern
        
        // Legitimate banking software indicators — if found, exclude
        $legit1 = "VERIFIED PUBLISHER: Acme Bank Software Ltd" wide
        $legit2 = "Copyright 2023 Acme Financial"
    
    condition:
        // 2 of the suspicious strings AND NOT the legitimate certificate
        2 of ($s*) and not 1 of ($legit*)
}
```

**Step 5 — Test both scenarios:** 
- Run against known malware sample → should match
- Run against legitimate banking software → should NOT match
- Document the tuning in the rule's meta section

---

**Q12.** Write a Python script that scans a directory with YARA rules and generates a JSON report of all detections with their severity, detected rule, and file metadata.

**Answer:**
```python
import yara, os, hashlib, json, re
from datetime import datetime
from pathlib import Path

def get_file_metadata(filepath: str) -> dict:
    stat = os.stat(filepath)
    with open(filepath, 'rb') as f:
        content = f.read()
    return {
        "path": filepath,
        "size_bytes": stat.st_size,
        "sha256": hashlib.sha256(content).hexdigest(),
        "md5": hashlib.md5(content).hexdigest(),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "created": datetime.fromtimestamp(stat.st_ctime).isoformat()
    }

def compile_rules(rules_directory: str) -> yara.Rules:
    """Compile all .yar files in a directory"""
    rule_files = {}
    for f in Path(rules_directory).glob("**/*.yar"):
        namespace = f.stem.replace('-', '_').replace(' ', '_')
        rule_files[namespace] = str(f)
    return yara.compile(filepaths=rule_files)

def scan_directory(target_dir: str, rules_dir: str) -> dict:
    rules = compile_rules(rules_dir)
    report = {
        "scan_timestamp": datetime.now().isoformat(),
        "target_directory": target_dir,
        "rules_directory": rules_dir,
        "total_files_scanned": 0,
        "total_detections": 0,
        "findings": []
    }
    
    for root, _, files in os.walk(target_dir):
        for fname in files:
            fpath = os.path.join(root, fname)
            report["total_files_scanned"] += 1
            
            try:
                matches = rules.match(fpath, timeout=10)
                if matches:
                    meta = get_file_metadata(fpath)
                    for match in matches:
                        severity = match.meta.get("severity", "unknown")
                        finding = {
                            "file": meta,
                            "rule_name": match.rule,
                            "rule_namespace": match.namespace,
                            "severity": severity,
                            "tags": match.tags,
                            "matched_strings": [
                                {
                                    "identifier": s.identifier,
                                    "offset": s.instances[0].offset,
                                    "preview": repr(s.instances[0].matched_data[:32])
                                }
                                for s in match.strings[:5]  # Limit to 5 matched strings
                            ]
                        }
                        report["findings"].append(finding)
                        report["total_detections"] += 1
            except (yara.TimeoutError, PermissionError, FileNotFoundError, yara.Error):
                pass
    
    # Sort by severity (critical first)
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "unknown": 4}
    report["findings"].sort(key=lambda x: severity_order.get(x["severity"], 4))
    
    return report

# Usage
report = scan_directory("/suspect/directory", "/yara/rules")
print(json.dumps(report, indent=2))

# Save report
with open(f"yara_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", 'w') as f:
    json.dump(report, f, indent=2)
    
print(f"\nScan complete: {report['total_files_scanned']} files, {report['total_detections']} detections")
```

---

**Q13.** Explain the Pyramid of Pain with specific examples of each tier. Why do most commercial threat intelligence feeds focus on the bottom tiers, and why is this a problem?

**Answer:**

| Tier | Example | Ease of change for attacker |
|------|---------|---------------------------|
| **Hashes** | MD5: `d41d8cd98f00b204e9800998ecf8427e` | Trivial — recompile with one changed byte |
| **IP Addresses** | C2: `185.220.101.100` | Easy — rent new VPS for $5/month |
| **Domain Names** | `update.bad-cdn.ru` | Easy — register new domain for $10 |
| **Network/Host Artefacts** | Registry key: `HKCU\...\Run\MSUpdate`, User-Agent: `Mozilla/4.0 (Winword)` | Moderate — requires changing tooling |
| **Tools** | Mimikatz.exe signature, CobaltStrike beacon profile | Hard — requires rebuilding tool or buying new one |
| **TTPs** | "Uses certutil to download, then regsvr32 to execute, beacons every 60s" | Very hard — must change entire operational approach |

**Why commercial feeds focus on lower tiers:** They're easier to generate at scale — automated systems extract hashes and IPs from malware samples and phishing emails by the millions. IOC feeds with 10,000 hashes look impressive.

**Why this is a problem:**
1. **Hash rotation:** Malware-as-a-service operations now recompile every download with a unique hash. By the time a hash appears in a threat feed, that exact binary is no longer being deployed.
2. **IP rotation:** C2 infrastructure rotates IPs constantly. The IP you block today is abandoned tomorrow, and the attacker is already on a new IP.
3. **False confidence:** Organisations that rely on hash/IP blocking feel protected but miss attacks from the same group using new infrastructure.

**Better investment:** TTP-based detection (Sigma rules for techniques) defeats the attacker even when they change all their infrastructure, because the behaviour stays similar. A rule detecting "certutil downloading from internet → regsvr32 executing" catches the attack regardless of which IP or hash is involved.

---

## Section C: SOAR and Detection Lifecycle (Questions 14-20)

**Q14.** Design a SOAR playbook for responding to a "Ransomware Encryption Activity Detected" alert from your EDR. Show the decision tree and automation steps.

**Answer:**
```
TRIGGER: EDR Alert — Mass file extension modification (.xlsx → .locked)
         On host: HOST-X | User: jsmith | Time: 14:23

STEP 1 — AUTOMATED SCOPE CHECK
  Action: Query SIEM for same file extension modification pattern across all hosts
  Query: "*.locked extension creation in last 10 minutes" across all endpoints
  Branch:
    → 1 host: contain this host (proceed to Step 2)
    → 2-10 hosts: ESCALATE P1, notify on-call + CISO, proceed to Step 2
    → 10+ hosts: ESCALATE P1 CRITICAL, initiate mass containment (all affected hosts),
                 notify executive team, consider network segmentation

STEP 2 — AUTOMATED THREAT INTEL
  Action: Extract SHA256 of modifying process from EDR
  Action: Query VirusTotal for hash
  Action: Check ransomware family on ID-Ransomware.malwarehunterteam.com (via API)
  Output: Attach all results to incident ticket

STEP 3 — AUTOMATED CONTAINMENT (requires pre-approved policy)
  Action: Isolate HOST-X via EDR (network isolation command)
  Action: Disable jsmith's AD account
  Action: Block the process hash at AV/EDR policy level across all endpoints
  Action: Take memory snapshot of HOST-X (forensic capture)

STEP 4 — HUMAN DECISION REQUIRED
  Notify: L2 analyst + IR lead with full enrichment package
  Wait for human: Approve or override automated containment?
  
STEP 5 — AUTOMATED NOTIFICATIONS
  Action: Create incident ticket in JIRA/ServiceNow
  Action: Notify CISO via SMS (P1 incident)
  Action: Send Slack message to #soc-alerts: "RANSOMWARE DETECTED on HOST-X - contained"
  Action: Start incident timer for SLA tracking

STEP 6 — HUMAN: PROCEED WITH FULL IR
  Manual steps: Memory forensics, patient zero investigation,
                backup assessment, recovery planning
```

---

**Q15.** What is Atomic Red Team? How does it fit into the detection engineering workflow? Write a procedure for using it to test a specific Sigma rule.

**Answer:** Atomic Red Team (by Red Canary) is a library of small, focused test cases — "atomic tests" — that replicate specific MITRE ATT&CK techniques in a controlled way. Each test is minimal, verifiable, and safely reversible.

**Workflow: Atomic Tests in Detection Engineering**
```
Write detection rule → Test with Atomic Red Team → Verify rule fires → Tune → Deploy
```

**Procedure for testing T1059.001 (PowerShell download cradle) rule:**
```powershell
# STEP 1: Set up test environment (isolated lab VM)
# Install Invoke-AtomicRedTeam module
IEX (New-Object Net.WebClient).DownloadString(
    'https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/install-atomicredteam.ps1')
Import-Module Invoke-AtomicRedTeam

# STEP 2: Review the test before running
Get-AtomicTest T1059.001        # See what the test will do
# Shows: description, prerequisites, command to execute, cleanup

# STEP 3: Ensure your detection rule is deployed and SIEM is collecting logs

# STEP 4: Run the atomic test
Invoke-AtomicTest T1059.001 -TestNumbers 1  # Test #1: Download and execute via IEX

# STEP 5: Check your SIEM within 2 minutes
# Expected: Your Sigma rule fires an alert
# Check: EventCode=4688, CommandLine contains "Invoke-Expression" or "DownloadString"

# STEP 6: If rule did NOT fire
# Diagnose: Was Event 4688 logged with CommandLine? (Check if Command Line Logging is enabled)
# Fix: Enable Advanced Audit Policy → Process Creation → include command line
# Tune the rule if field names don't match

# STEP 7: Cleanup
Invoke-AtomicTest T1059.001 -TestNumbers 1 -Cleanup
# Removes any artefacts created by the test

# STEP 8: Document results
# In your detection rule YAML, add: "validated: 2024-01-15 via Atomic T1059.001 test #1"
```

---

**Q16.** Describe 5 key metrics to track for a detection engineering programme and explain how each indicates programme health.

**Answer:**

| Metric | How to measure | Healthy indicator |
|--------|---------------|-----------------|
| **MITRE ATT&CK coverage %** | Number of techniques with ≥1 detection rule / total techniques × 100 | Increasing over time; >60% for critical tactics (TA0001-TA0006) |
| **Mean Time to Detection (MTTD)** | Average time between initial compromise (from IR) and first alert | Decreasing; target <24 hours |
| **Rule FP rate** | FP alerts / total alerts × 100, tracked per rule | <30% for any individual rule; average <20% overall |
| **Dwell time of detected threats** | Time from initial compromise to detection (from IR post-mortems) | Decreasing; industry median 10 days |
| **Detection content velocity** | New rules written per sprint/month | Increasing or stable; minimum 5-10 new rules/month to keep pace with evolving threats |

**Analysis example:** If MTTD is 45 days but ATT&CK coverage is 80%, the problem is probably rule quality (too many FPs suppressing alerts or too many rules targeting late-stage techniques). If MTTD is 2 days but coverage is 20%, rules are high quality but miss many techniques.

---

**Q17.** What is "detection-as-code"? Explain how applying software engineering practices (version control, CI/CD, testing) to detection rules improves a SOC's effectiveness.

**Answer:** Detection-as-code treats security detection rules as software: stored in version control, tested automatically, reviewed via pull requests, and deployed through a pipeline. Contrasted with the traditional approach of manually editing rules in a SIEM console with no version history and no testing.

**Benefits:**

1. **Version control (Git):** Every rule change is tracked — who changed it, when, why. Can roll back a bad rule change. Can see why a rule was tuned (PR description). Essential for a team.

2. **Code review (Pull Requests):** Before a rule goes to production, another detection engineer reviews it. Catches mistakes, suggests improvements, shares knowledge. Same quality control software engineers use.

3. **Automated testing (CI/CD):** Pipeline automatically runs Atomic Red Team tests against new rules in a test SIEM before promoting to production. New rule for T1003 → pipeline runs `Invoke-AtomicTest T1003` → verifies alert fires → if not, PR fails and engineer must fix.

4. **Automated deployment:** Approved rules automatically pushed to all SIEM instances (production, DR, cloud). No manual console work, no "I forgot to deploy the rule to the DR SIEM."

5. **Testing on historical data:** New rules can be run against 90 days of historical log data automatically — if they would have generated >100 FPs per day in history, the rule is flagged for tuning before it even reaches production.

**Real-world stack:** Sigma rules in Git → sigma-cli converts to SIEM format → GitHub Actions CI runs Atomic tests + historical FP rate check → approved → deploys to Splunk/Sentinel.

---

**Q18.** Write a Sigma rule for detecting PowerShell one-liner download-and-execute without writing to disk (fileless execution).

**Answer:**
```yaml
title: PowerShell Fileless Execution via Memory-Only Download
id: b3c4d5e6-f7a8-9b0c-1d2e-3f4a5b6c7d8e
status: experimental
description: >
  Detects PowerShell executing code downloaded directly into memory (fileless).
  Pattern: (New-Object Net.WebClient).DownloadString or similar, piped to IEX
  (Invoke-Expression). This leaves no file on disk — evades most file-based AV.
  Also detects Invoke-Expression on its own with suspicious arguments.
references:
  - https://attack.mitre.org/techniques/T1059/001/
  - https://attack.mitre.org/techniques/T1027/
author: Detection Engineering
date: 2024/01
modified: 2024/06
tags:
  - attack.execution
  - attack.t1059.001
  - attack.defense_evasion
  - attack.t1140
logsource:
  category: process_creation
  product: windows
detection:
  # Pattern 1: Classic IEX download cradle
  selection_iex_download:
    CommandLine|contains|all:
      - 'DownloadString'
    CommandLine|contains|any:
      - 'IEX'
      - 'Invoke-Expression'
      - '| &'       # Pipe to call operator
  
  # Pattern 2: Encoded command (hides IEX + download)
  selection_encoded:
    Image|endswith: '\powershell.exe'
    CommandLine|contains:
      - '-encodedcommand'
      - '-enc '
      - '-ec '
  CommandLine|re: '-[eE]([nN][cC]([oO][dD][eE][dD])?)?[cC]?[oO]?[mM]?[mM]?[aA]?[nN]?[dD]?'
  
  # Pattern 3: WebClient or WebRequest in script block
  selection_webclient:
    CommandLine|contains|any:
      - 'Net.WebClient'
      - 'Net.WebRequest'
      - 'Invoke-WebRequest'
      - 'Start-BitsTransfer'
    CommandLine|contains|any:
      - 'IEX'
      - 'Invoke-Expression'
      - 'DownloadFile'
      - 'DownloadData'
  
  # Filters for known legitimate usage
  filter_update_services:
    ParentImage|endswith:
      - '\WindowsUpdate.exe'
      - '\wuauclt.exe'
  
  condition: (1 of selection_*) and not 1 of filter_*
falsepositives:
  - Software management tools (SCCM, Chocolatey) — add specific exclusions
  - Development environments — monitor but may be expected in dev teams
level: high
```

---

**Q19.** What is purple teaming? How does it differ from traditional red and blue team exercises, and how does it improve detection engineering?

**Answer:**
**Traditional model:**
- **Red Team:** Attacks the organisation (simulated adversary) — tries to avoid detection
- **Blue Team:** Defends and detects — tries to find the red team
- **Result:** After the exercise, red team writes a report. Blue team gets the findings. Improvements may take months to implement. Red and blue teams don't collaborate during the exercise.

**Purple teaming:** Red and blue work together simultaneously and transparently.
- Red team executes a specific technique (e.g., `Invoke-AtomicTest T1055`)
- Blue team watches in real-time: "Did that generate an alert?"
- If YES → great, detection works. Document and move on.
- If NO → blue team and red team diagnose together: was the log generated? Was the log forwarded? Does the SIEM rule exist? Does the field name match?
- Fix the gap immediately during the exercise.

**Benefits for detection engineering:**
1. **Immediate feedback loop:** Gaps are identified and fixed in the same session — not months later after a full red team report
2. **Coverage mapping:** Systematically go through entire ATT&CK matrix together — no guessing which techniques you can detect
3. **Skill sharing:** Blue team learns HOW attacks are executed (helps write better rules); red team learns WHAT defenders can see (helps them build more realistic scenarios)
4. **Measurable output:** Start the day with X% ATT&CK coverage, end with X+Y% — tangible improvement

---

**Q20.** Design a detection rule for identifying "living off the land" binary (LOLBin) `mshta.exe` being used for code execution, as documented in MITRE ATT&CK T1218.005.

**Answer:**
```yaml
title: Mshta.exe Executing Remote or Encoded Script (LOLBin Abuse)
id: e5f6a7b8-c9d0-1e2f-3a4b-5c6d7e8f9a0b
status: stable
description: >
  mshta.exe (Microsoft HTML Application Host) is a Windows signed binary for running
  HTA (HTML Application) files. It is frequently abused to: execute remote HTA files
  (downloading and running code), execute VBScript/JScript inline, and bypass application
  whitelisting since mshta is a trusted Windows binary.
  
  Legitimate usage: mshta.exe only runs local .hta files as part of software installers.
  Remote execution and inline scripts are never legitimate.
references:
  - https://attack.mitre.org/techniques/T1218/005/
  - https://lolbas-project.github.io/lolbas/Binaries/Mshta/
author: Detection Engineering
date: 2024/01
tags:
  - attack.defense_evasion
  - attack.execution
  - attack.t1218.005
logsource:
  category: process_creation
  product: windows
detection:
  selection_base:
    Image|endswith: '\mshta.exe'
  
  # Pattern 1: Remote execution (most suspicious)
  selection_remote:
    CommandLine|contains|any:
      - 'http://'
      - 'https://'
      - 'ftp://'
      - '\\\\'          # UNC path — network share execution
  
  # Pattern 2: Inline script execution (second most suspicious)
  selection_inline:
    CommandLine|contains|any:
      - 'vbscript:'
      - 'javascript:'
      - 'JScript:'
      - 'VBScript.Encode'
  
  # Pattern 3: Spawned by unusual parent (mshta shouldn't be spawned by Office)
  selection_suspicious_parent:
    Image|endswith: '\mshta.exe'
    ParentImage|endswith|any:
      - '\winword.exe'
      - '\excel.exe'
      - '\powerpnt.exe'
      - '\outlook.exe'
      - '\cmd.exe'
      - '\wscript.exe'
      - '\cscript.exe'
  
  # Filter legitimate uses (software installers)
  filter_installers:
    CommandLine|contains:
      - 'C:\Program Files'
      - 'C:\Windows\Installer'
  
  condition: (selection_base and (selection_remote or selection_inline or selection_suspicious_parent)) and not filter_installers
falsepositives:
  - Some older enterprise software uses mshta — review and whitelist specifically
  - Software installers using local HTA files (covered by filter)
level: high
```

---

## Section D: Career and Portfolio (Questions 21-25)

**Q21.** A hiring manager asks you: "Walk me through a detection rule you've written from scratch." Using the Sigma rule you wrote for certutil abuse, give a complete interview answer.

**Answer:**
*"I wrote a Sigma rule to detect certutil abuse for the LOLBin technique T1105 (Ingress Tool Transfer). The problem I was addressing: certutil.exe is a legitimate Windows Certificate Services tool, but attackers discovered it could download files from the internet using the `-urlcache -f` flags — completely bypassed many security products because it's a signed Microsoft binary.*

*My approach: I researched how certutil is legitimately used — it manages certificate stores, validates certificate chains, nothing involving downloading arbitrary files. So any certutil with `-urlcache`, `-decode`, or an HTTP URL in its arguments is essentially never legitimate.*

*For the Sigma rule, I used process creation logs (Sysmon Event 1 or Windows Event 4688). The detection logic had two components: first, the image path ends with `certutil.exe`; second, the command line contains suspicious flags. I added a filter for Certificate Services management operations (`CertSvc`, `CertStore`) which use certutil legitimately.*

*I tested it with Atomic Red Team test T1105-001 which runs exactly this technique. The rule fired correctly. I ran it against 30 days of historical logs — got 2 FPs, both from IT running legitimate certificate management. I added their specific command line patterns to the filter.*

*What I learned: the specificity of the condition matters a lot. My first version was too broad and got 50 FPs. The key was requiring BOTH the suspicious flag AND the absence of Certificate Services context."*

---

**Q22.** What are the key differences between working as a SOC analyst (L1/L2) versus a detection engineer? Which career path interests you more and what skills does each require?

**Answer:**

| | SOC Analyst (L1/L2) | Detection Engineer |
|-|--------------------|--------------------|
| **Focus** | Reactive — investigate and triage alerts | Proactive — build the systems that generate alerts |
| **Time horizon** | Minutes to hours (incident response) | Days to weeks (rule development) |
| **Output** | Closed alert tickets, incident reports | Detection rules, playbooks, coverage reports |
| **Key skills** | Alert triage, log analysis, communication, SIEM query writing | Programming, ATT&CK expertise, threat intelligence, pipeline automation |
| **Tools** | SIEM, EDR, ticketing system, OSINT | SIEM, Git, Python/Sigma/YARA, CI/CD, Atomic Red Team |
| **Work pressure** | High — multiple active incidents simultaneously | Lower urgency — but accountability for detection gaps |
| **Career growth** | L2 → L3 → Threat Hunter → IR Lead | → Senior Detection Eng → Detection Architect → Security Engineer |

**Required to transition from SOC to Detection Engineering:**
- Develop Python skills (automation, parsing, API integration)
- Learn Git and GitHub (version control for detection content)
- Master MITRE ATT&CK deeply — not just awareness but the ability to map any technique to log artifacts
- Build public detection content (GitHub portfolio of Sigma/YARA rules)
- Understand CI/CD pipelines (how to automate testing and deployment of rules)

---

**Q23.** Write a job description posting for a Detection Engineer role at a financial services company. Include required skills, preferred skills, and responsibilities.

**Answer:**

---
**Detection Engineer — Cybersecurity Operations**  
*Location: Mumbai / Bengaluru / Remote*  
*Level: Mid-Senior (4-7 years experience)*

**About the Role**  
You will design and build the detection capabilities that protect our customers' financial data from advanced threats. You'll work at the intersection of threat intelligence, data engineering, and security operations — translating attacker techniques into detection logic that runs at scale.

**Responsibilities**
- Develop and maintain detection content (Sigma rules, KQL, Splunk SPL) mapped to MITRE ATT&CK
- Operate the detection engineering lifecycle: research → write → test → deploy → monitor → tune
- Build and maintain SOAR playbooks for automated alert triage and response
- Conduct purple team exercises to validate detection coverage
- Partner with Threat Intelligence team to translate CTI into detections within hours of new threat reporting
- Measure and report on detection coverage, FP rates, and MTTD
- Mentor L1/L2 SOC analysts on detection logic and investigation techniques

**Required Skills**
- 4+ years in Security Operations (SOC Analyst L2+ or Detection Engineering)
- Proficiency in at least 2 of: Splunk SPL, KQL (Sentinel), ELK (KQL), Chronicle
- Strong knowledge of MITRE ATT&CK framework
- Experience writing detection rules (Sigma, YARA, or native SIEM query language)
- Python scripting for automation and log parsing
- Understanding of Windows/Linux internals relevant to attacker techniques

**Preferred Skills**
- Sigma rule contribution to SigmaHQ (public portfolio)
- Experience with SOAR platforms (Palo Alto XSOAR, Splunk SOAR, Tines, Shuffle)
- Red team or pen testing knowledge (understanding how attacks work improves detections)
- CI/CD experience (GitHub Actions, GitLab CI)
- Relevant certifications: GCIA, GCDA, CEH, OSCP

**Why Join Us**  
Modern security stack (Sentinel + CrowdStrike + Chronicle). Detection-as-code with CI/CD pipeline. Budget for conferences and certifications. Remote-first with flexible hours.

---

**Q24.** Explain how you would build a "threat-informed defence" programme at a mid-sized Indian fintech company (500 employees, handles UPI payments, AWS-based infrastructure).

**Answer:** Threat-informed defence uses knowledge of SPECIFIC threats targeting your industry and geography to prioritise defensive investment — instead of trying to defend against everything equally.

**Step 1 — Identify relevant threat actors:**
- Who targets Indian fintechs? Research: CERT-In advisories, RBI cybersecurity bulletins, Mandiant/CrowdStrike India reports
- Key threats: ransomware groups (Lockbit, Akira), FIN-tier financial fraud actors, state-sponsored actors (North Korean actors targeting crypto), local cybercriminal groups targeting UPI fraud

**Step 2 — Map their TTPs to ATT&CK:**
- From threat intelligence, extract the techniques these groups use
- Input into ATT&CK Navigator to visualise coverage gaps

**Step 3 — Assess current detection coverage:**
- Run ATT&CK evaluations: for each relevant TTP, do you have a detection rule?
- Identify gaps: "We have zero coverage for T1190 (Exploit Public-Facing Application) and T1505.003 (Web Shell)"

**Step 4 — Prioritise by impact:**
- P0: Techniques that, if successful, mean regulatory breach (payment data access, customer PII exfiltration)
- P1: Techniques that lead to fraud (credential theft, session hijacking)
- P2: Operational techniques (lateral movement, persistence)

**Step 5 — Build detections, configure controls, and validate:**
- For each P0/P1 gap: write Sigma rule, configure WAF rule, harden configuration
- Purple team exercise to validate detection fires
- Quarterly repeat as threat landscape evolves

---

**Q25.** You are building a public GitHub portfolio for detection engineering roles. What should it include, and how should you structure it to impress a hiring manager?

**Answer:**

**Repository structure:**
```
detection-portfolio/
├── README.md          ← Most important file — your "cover letter"
├── sigma/
│   ├── windows/
│   │   ├── proc_creation/  (15-20 rules for common Windows techniques)
│   │   └── registry/       (5-10 rules for persistence)
│   ├── linux/              (5-10 rules)
│   └── cloud/              (5-10 rules for AWS/Azure)
├── yara/
│   ├── malware_families/   (5+ rules for known families)
│   └── generic/            (generic patterns — packed PE, etc.)
├── soar/
│   └── playbooks/          (2-3 documented playbooks)
├── hunting/
│   └── queries/            (5-10 threat hunting queries with context)
└── blog/
    └── writeups/           (2-3 write-ups explaining techniques and detections)
```

**README.md should include:**
- Brief bio: your role, specialisations, ATT&CK coverage focus
- Coverage heatmap: ATT&CK Navigator export showing what you can detect
- Highlight 3 "best" rules with explanation of: the threat, the detection logic, how you tested it
- What tools you use (SIEM, EDR, automation)
- Certifications and relevant training

**Quality over quantity:** 10 well-documented, tested, production-quality rules beat 100 rules copied from the internet. Each rule should have:
- Clear description and ATT&CK mapping
- Testing methodology documented in comments
- Known false positive sources listed
- Tuning guidance

**What impresses hiring managers:**
1. Rules that solve REAL problems (not textbook exercises)
2. Evidence of testing (Atomic Red Team validation noted in meta)
3. Blog posts explaining the "why" behind a detection — shows you understand the threat
4. Contribution to public projects (SigmaHQ PRs accepted)
