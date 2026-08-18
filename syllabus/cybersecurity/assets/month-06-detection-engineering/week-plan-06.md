# Month 6 — Week-by-Week Study Plan
## Detection Engineering: Sigma, YARA, and SOAR

**Total study time: ~80 hours over 4 weeks**

---

## Week 1 — Sigma: The Universal Detection Language

**Goal:** Write, test, and deploy Sigma rules to detect real attacker techniques.

### Day 1 — Why Sigma Exists and How It Works
- **Read:** `01-sigma-yara-detection.md` — Sigma section
- **The problem Sigma solves:** Detection rules written for Splunk don't work in Elastic or Sentinel. Every SIEM has its own query language. Sigma is a vendor-neutral YAML format that translates to any SIEM.
- **Sigma rule anatomy:**
  ```yaml
  title: Suspicious PowerShell Download Cradle
  id: 6e897651-f157-4d8f-aaeb-df8151488385   # unique UUID
  status: experimental
  description: Detects PowerShell downloading and executing code from internet
  author: Your Name
  date: 2024/01
  references:
    - https://attack.mitre.org/techniques/T1059/001/
  tags:
    - attack.execution
    - attack.t1059.001
  logsource:
    category: process_creation
    product: windows
  detection:
    selection:
      CommandLine|contains|all:
        - 'powershell'
        - 'DownloadString'
    filter_legitimate:
      CommandLine|contains:
        - 'WindowsUpdate'
    condition: selection and not filter_legitimate
  falsepositives:
    - Legitimate software updates using PowerShell
  level: high
  ```
- **Key fields:** `logsource` (where to look), `detection` (what to find), `condition` (logical combination), `level` (critical/high/medium/low/informational)

### Day 2 — Field Modifiers and Advanced Conditions
- **Field modifiers — these are critical:**
  ```yaml
  # contains: substring match
  CommandLine|contains: 'mimikatz'
  
  # startswith / endswith
  Image|startswith: 'C:\Windows\Temp\'
  
  # contains|all: ALL strings must match
  CommandLine|contains|all:
    - '-enc'
    - 'powershell'
  
  # contains|any: ANY string matches
  CommandLine|contains|any:
    - 'mimikatz'
    - 'sekurlsa'
    - 'lsadump'
  
  # re: full regex match
  CommandLine|re: '(?i)invoke-(mimikatz|expression|shellcode)'
  
  # cidr: IP range matching
  DestinationIp|cidr:
    - '10.0.0.0/8'
    - '192.168.0.0/16'
  
  # fieldref: compare two fields
  ParentImage|fieldref: Image  # parent and child same process = suspicious
  ```
- **Condition operators:**
  ```yaml
  condition: selection                          # Simple: selection matches
  condition: selection and not filter           # Selection BUT NOT filter
  condition: selection1 or selection2           # Either selection
  condition: all of selection*                  # All selection_* keywords
  condition: 1 of filter_*                      # At least 1 filter_* keyword
  condition: selection | count() by ip > 100    # Aggregation: count IPs
  ```

### Day 3 — Convert Sigma Rules with pySigma
- **Install pySigma:**
  ```bash
  pip install sigma-cli
  pip install pysigma-backend-splunk
  pip install pysigma-backend-elasticsearch
  pip install pysigma-pipeline-windows  # Fieldname mappings for Windows logs
  ```
- **Convert Sigma → Splunk SPL:**
  ```bash
  sigma convert -t splunk -p windows/sysmon rule.yml
  # Output: EventCode=4688 (CommandLine="*powershell*" AND CommandLine="*DownloadString*")
  # AND NOT (CommandLine="*WindowsUpdate*")
  ```
- **Convert Sigma → KQL (Microsoft Sentinel):**
  ```bash
  sigma convert -t microsoft365defender rule.yml
  ```
- **Batch convert a directory of rules:**
  ```bash
  sigma convert -t splunk -p windows/sysmon /path/to/sigma/rules/windows/
  ```

### Day 4 — Writing Rules for 5 ATT&CK Techniques
- **Write Sigma rules for each of these (one per hour):**

  1. **T1059.001 — PowerShell encoded command**
  2. **T1003.001 — LSASS memory dumping (procdump -ma lsass)**
  3. **T1548.002 — UAC bypass via fodhelper.exe**
  4. **T1071.001 — Web shell command (IIS spawning cmd.exe or powershell.exe)**
  5. **T1105 — Certutil downloading a file (certutil -urlcache -f http://...)**

- **Template for each:**
  ```yaml
  title: [Technique name]
  id: [generate UUID: python -c "import uuid; print(uuid.uuid4())"]
  description: [What it detects]
  logsource:
    category: process_creation
    product: windows
  detection:
    selection:
      [your detection logic]
    condition: selection
  level: high
  tags:
    - attack.t[NUMBER]
  ```

### Day 5 — Test Rules Against Real Logs
- **Set up Sigma testing:**
  ```bash
  # Install sigma-cli with a backend
  pip install sigma-cli pysigma-backend-splunk pysigma-pipeline-windows
  
  # Convert your rule
  sigma convert -t splunk -p windows/sysmon my_rule.yml
  
  # Test against your SIEM with the converted query
  ```
- **Use Atomic Red Team for testing:**
  - atomicredteam.io — community library of test executions for each ATT&CK technique
  - Download Invoke-AtomicRedTeam PowerShell module
  - In a lab VM: run the atomic test → check if your Sigma rule detects it
  ```powershell
  # Install Atomic Red Team
  IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/redcanaryco/invoke-atomicredteam/master/install-atomicredteam.ps1')
  # Run test for T1059.001 (PowerShell)
  Invoke-AtomicTest T1059.001
  ```
- **Complete quiz questions 1-7 from `quiz-06.json`**

---

## Week 2 — YARA Rules: Hunting Malware by Pattern

**Goal:** Write YARA rules to identify malware families by their code patterns.

### Day 6 — YARA Rule Structure
- **Read:** `01-sigma-yara-detection.md` — YARA section
- **Install YARA:**
  ```bash
  # Linux
  sudo apt install yara
  
  # Windows: download from virustotal/yara/releases
  
  # Python library
  pip install yara-python
  ```
- **YARA rule anatomy:**
  ```yara
  rule DetectMimikatz {
      meta:
          description = "Detects Mimikatz credential dumping tool"
          author = "Your Name"
          date = "2024-01"
          reference = "https://github.com/gentilkiwi/mimikatz"
          severity = "critical"
      
      strings:
          // Text strings
          $s1 = "sekurlsa::logonpasswords" nocase
          $s2 = "privilege::debug" nocase
          $s3 = "lsadump::dcsync" nocase
          
          // Hex bytes (version-independent)
          $hex1 = { 6B 65 72 62 65 72 6F 73 }  // "kerberos" in hex
          
          // Wide strings (UTF-16LE, common in Windows binaries)
          $w1 = "mimikatz" wide nocase
          $w2 = "Benjamin Delpy" wide nocase
          
      condition:
          // 2 or more string matches
          2 of ($s*) or
          1 of ($hex*) or
          $w2  // Author string is very specific
  }
  ```

### Day 7 — String Types and Condition Operators
- **String modifiers:**
  ```yara
  $s1 = "MZ"                    // Exact ASCII match (PE header magic bytes)
  $s2 = "mimikatz" nocase      // Case-insensitive
  $s3 = "sekurlsa" ascii wide  // Match both ASCII and Unicode
  $s4 = "calc.exe" fullword    // Must be surrounded by non-word chars
  
  // Regex strings
  $r1 = /http:\/\/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/
  $r2 = /[A-Za-z0-9+/]{40,}==?/  // Base64 strings
  
  // Hex strings with wildcards
  $h1 = { 55 8B EC ?? ?? ?? 00 }  // ?? = any byte
  $h2 = { 55 8B EC [2-4] 00 }     // [2-4] = 2 to 4 any bytes
  ```
- **Condition operators:**
  ```yara
  condition:
    all of them                     // All strings must match
    any of them                     // At least one string matches
    2 of ($s*)                      // 2 of the $s* strings match
    $s1 and not $s2                 // $s1 matches, $s2 doesn't
    $s1 at 0                        // $s1 found at file offset 0 (PE header check)
    $s1 in (0..1024)                // $s1 in first 1024 bytes
    #s1 > 3                         // $s1 appears more than 3 times
    filesize < 1MB                  // File size constraint
    uint16(0) == 0x5A4D             // PE magic bytes ("MZ") at offset 0
  ```

### Day 8 — Run YARA Against Files
- **Scanning with YARA:**
  ```bash
  # Scan a single file
  yara my_rule.yar suspicious.exe
  
  # Scan a directory recursively
  yara -r my_rule.yar /suspect/directory/
  
  # Use multiple rule files
  yara rules1.yar rules2.yar target.exe
  
  # Output: rule name + filename for matches
  
  # Python integration
  import yara
  rules = yara.compile('my_rule.yar')
  matches = rules.match('/path/to/file.exe')
  for match in matches:
      print(f"Rule: {match.rule}, Strings: {match.strings}")
  ```
- **Safe malware samples for testing:** YARA rules → test against samples from:
  - theZoo (github.com/ytisf/theZoo) — deactivated malware samples
  - MalwareBazaar (bazaar.abuse.ch) — live malware samples (handle with extreme care in isolated VM only)

### Day 9 — Complete Lab-06-a: Sigma Detection Rule Lab
- **Complete `lab-06-a.json`** — all 5 steps
- **Write a YARA rule for a real malware family:**
  - Research: look at any.run sandbox report for Emotet or AgentTesla
  - Find 3 distinctive strings or hex patterns unique to that family
  - Write the YARA rule
  - Test against a clean file (should NOT match) and a reported sample hash on VirusTotal (check if your rule would match based on the strings)

### Day 10 — Build a YARA Rule Test Suite
- **Complete `lab-06-b.json`** — all 5 steps
- **Build a Python YARA scanner:**
  ```python
  import yara, os, hashlib, json
  from datetime import datetime
  
  def scan_directory(target_dir: str, rules_dir: str) -> list:
      # Compile all YARA rules
      rules = yara.compile(filepath=rules_dir + '/combined_rules.yar')
      findings = []
      
      for root, _, files in os.walk(target_dir):
          for fname in files:
              fpath = os.path.join(root, fname)
              try:
                  matches = rules.match(fpath)
                  if matches:
                      with open(fpath, 'rb') as f:
                          sha256 = hashlib.sha256(f.read()).hexdigest()
                      for m in matches:
                          findings.append({
                              "timestamp": datetime.now().isoformat(),
                              "file": fpath,
                              "sha256": sha256,
                              "rule": m.rule,
                              "tags": m.tags
                          })
              except (yara.Error, PermissionError, FileNotFoundError):
                  pass
      
      return findings
  
  results = scan_directory('/suspect_folder', '/yara_rules')
  print(json.dumps(results, indent=2))
  ```

---

## Week 3 — SOAR: Automating the SOC

**Goal:** Build real SOAR playbooks that automate alert triage.

### Day 11 — SOAR Concepts and Platforms
- **Read:** `02-soar-career-prep.md` — SOAR section
- **Set up Shuffle SOAR (free, open-source):**
  ```bash
  # Docker install
  docker-compose up -d
  # Access at http://localhost:3001
  # Create free account
  ```
- **First workflow: IP reputation check on alert**
  1. Trigger: Webhook (simulates receiving an alert)
  2. Action: HTTP GET to AbuseIPDB API with the IP from the alert
  3. Condition: If abuse score > 80 → create high priority ticket
  4. Action: Send Slack notification with IP details

### Day 12 — Build Phishing Triage Playbook
- **Phishing triage playbook steps:**
  1. **Trigger:** Email security gateway fires alert for suspected phishing
  2. **Extract:** Sender domain, URLs in email, attachment hash
  3. **Enrich:** Check sender domain age (WHOIS), check URLs in VirusTotal, check attachment hash in MalwareBazaar
  4. **Score:** Build risk score based on enrichment results
  5. **Decision branch:**
     - Score > 80: Quarantine email, block sender domain in email gateway, notify security team (human decision on endpoint scan)
     - Score 40-80: Flag for analyst review, add to watch list
     - Score < 40: Auto-close as low confidence, add sender to monitoring
  6. **Notify:** Send Slack/Teams message to analyst with all enrichment data pre-populated

### Day 13 — Detection Engineering Lifecycle
- **The full lifecycle:**
  1. **Identify gap:** Threat hunting found a technique with no detection coverage
  2. **Write rule:** Sigma (detection logic)
  3. **Test:** Run Atomic Red Team test, verify rule fires
  4. **Tune:** Generate false positives intentionally, add exceptions
  5. **Deploy:** Push to SIEM via pipeline
  6. **Monitor:** Track alert volume and FP rate
  7. **Review:** Quarterly review — is the rule still relevant? FP rate acceptable?
- **Build a detection engineering backlog:** List 10 ATT&CK techniques you want coverage for. Prioritise by: likelihood in your environment + current coverage gap. Assign owners and target dates.

### Day 14 — GitHub Portfolio: Detection Content
- **Create a public GitHub repository:** `detection-content`
- **Structure:**
  ```
  detection-content/
  ├── sigma/
  │   ├── windows/
  │   │   ├── proc_creation_powershell_encoded.yml
  │   │   ├── proc_creation_lsass_dump.yml
  │   │   └── ...
  │   └── linux/
  ├── yara/
  │   ├── malware/
  │   │   ├── detect_mimikatz.yar
  │   │   └── detect_cobalt_strike.yar
  │   └── test_files/
  ├── soar/
  │   └── phishing_triage_playbook.json
  └── README.md  (explain each rule, the ATT&CK technique, and detection logic)
  ```
- **This is your most visible portfolio asset** — hiring managers in detection engineering roles will look at this directly

### Day 15 — Complete Exercises and Review
- **Complete:** `exercises-06.md` questions 1-15
- **Complete:** `detection-interactive.html` — all 3 panels (Sigma builder, YARA builder, Pyramid of Pain)
- **Read:** At least 3 detection blog posts from:
  - blog.menasec.net (Sigma rule analysis)
  - uncoder.io (Sigma rule converter — online tool)
  - github.com/SigmaHQ/sigma — browse existing rules

---

## Week 4 — Mastery, Assignment, and Portfolio

### Day 16-17 — Assignment Tasks 1-2
- Complete `assignment-06.md` Tasks 1 and 2 (Sigma + YARA rules)

### Day 18-19 — Assignment Tasks 3-4
- Complete `assignment-06.md` Tasks 3 and 4 (SOAR playbook + GitHub portfolio)

### Day 20 — Final Assessment
- **Complete:** `exercises-06.md` questions 16-25
- **Quiz:** `quiz-06.json` — all 15 questions
- **Competency checklist:**
  - [ ] Write a Sigma rule from scratch for a PowerShell-based ATT&CK technique
  - [ ] Convert a Sigma rule to Splunk SPL and KQL using sigma-cli
  - [ ] Write a YARA rule with text strings, hex patterns, and a complex condition
  - [ ] Run YARA against a directory of files and interpret results
  - [ ] Explain the Pyramid of Pain and why TTPs are hardest to change
  - [ ] Build a basic SOAR playbook with at least 3 steps in Shuffle
  - [ ] Explain the detection engineering lifecycle (identify → write → test → deploy → monitor)
  - [ ] Push at least 5 detection rules to a public GitHub portfolio repo
  - [ ] Explain the difference between a Sigma rule and a YARA rule — when to use each
  - [ ] Describe 3 SOC interview scenarios and how you would answer them
