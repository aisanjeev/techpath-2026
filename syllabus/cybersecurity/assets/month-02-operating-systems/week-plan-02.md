# Month 2 — Week-by-Week Study Plan
## Operating Systems: Linux Fundamentals, Windows Internals & Active Directory

**Total study time: ~80 hours over 4 weeks**

---

## Week 1 — Linux Mastery: The Attacker and Defender's OS

**Goal:** Achieve genuine Linux CLI fluency — navigating, managing files, processes, and users.

### Day 1 — Linux Philosophy and File System
- **Read:** `01-linux-fundamentals.md` — file system hierarchy section
- **Hands-on setup:** If you don't have Linux, install Ubuntu 22.04 LTS in VirtualBox (free). Allocate 2 CPU, 4GB RAM, 25GB disk
- **Navigation drill (do 30 times each until instant):**
  ```bash
  pwd; ls -la; cd /etc; ls -la; cd ~; ls -la
  cat /etc/passwd | head -5
  file /bin/bash
  stat /etc/hosts
  ```
- **File system mapping task:** Draw the Linux directory tree from memory. Include: `/`, `/bin`, `/etc`, `/home`, `/var`, `/tmp`, `/usr`, `/opt`, `/proc`, `/dev`. Write 1-line purpose for each
- **Important files to know cold:**
  - `/etc/passwd` — user accounts (not passwords)
  - `/etc/shadow` — hashed passwords (root only)
  - `/etc/group` — group memberships
  - `/etc/hosts` — local DNS
  - `/etc/crontab` — scheduled tasks
  - `/var/log/auth.log` — authentication events

### Day 2 — Text Processing and File Operations
- **Core command mastery:**
  ```bash
  # Create and manipulate files
  touch test.txt
  echo "hello world" > test.txt
  echo "second line" >> test.txt
  cat test.txt
  
  # Search and filter
  grep -i "root" /etc/passwd
  grep -rn "password" /etc/         # Recursive search (security use case)
  grep -v "^#" /etc/ssh/sshd_config # Exclude comments
  
  # Text processing pipelines
  cat /etc/passwd | cut -d: -f1     # Extract usernames
  cat /etc/passwd | awk -F: '{print $1, $3}' | sort -n -k2
  
  # Find files
  find / -name "*.conf" 2>/dev/null
  find / -perm -4000 2>/dev/null    # SUID files (critical for security!)
  find /tmp -mtime -1               # Modified in last 24 hours
  ```
- **Security exercise:** Run `find / -perm -4000 2>/dev/null` on your Linux VM. List every SUID binary you find. Research what each one does. Which ones could be dangerous?

### Day 3 — User and Permission Management
- **Read:** `01-linux-fundamentals.md` — permissions section
- **Permissions deep dive:**
  ```bash
  # Understanding permission bits
  ls -la /etc/shadow     # Should show: ---------- 1 root shadow
  ls -la /bin/passwd     # Should show: -rwsr-xr-x (SUID bit!)
  
  # Change permissions
  chmod 755 script.sh    # rwxr-xr-x
  chmod 600 private_key  # rw------- (SSH key should always be this)
  chmod 644 config.txt   # rw-r--r--
  
  # Change ownership
  chown user:group file
  sudo chown root:root important.conf
  
  # Special permissions
  chmod 4755 file       # Set SUID bit (runs as owner, not caller)
  chmod 2755 dir        # Set SGID bit (new files inherit group)
  chmod 1777 /tmp       # Sticky bit (only owner can delete files)
  ```
- **Challenge:** Create a user `testuser`, create a file owned by root that `testuser` cannot read. Now set the SUID bit on a script that reads the file. Explain why this is a security risk.

### Day 4 — Processes and System Investigation
- **Process investigation tools:**
  ```bash
  ps aux                  # All processes, all users
  ps aux | grep apache    # Find specific process
  top                     # Interactive, press 'q' to quit
  htop                    # Better interactive (install: sudo apt install htop)
  
  # Process tree (who spawned what — critical for incident response)
  pstree
  pstree -p              # With PIDs
  
  # Network connections by process
  ss -tlnp               # Listening ports with process names
  ss -tnp state established   # Active connections
  
  # Investigate a PID
  ls -la /proc/1234/       # Process 1234's virtual directory
  cat /proc/1234/cmdline   # What command is it running?
  ls -la /proc/1234/fd/    # Open file descriptors (what files is it using?)
  ```
- **Security scenario:** You're investigating a Linux server and see an unfamiliar process named `svc_updater`. Walk through every command you would run to understand: what is it, who is running it, what files does it use, what network connections does it have?

### Day 5 — Log Analysis and Security Monitoring
- **Linux logs that matter for security:**
  ```bash
  # Authentication logs
  cat /var/log/auth.log | grep "Failed password" | tail -20
  cat /var/log/auth.log | grep "Accepted password" | tail -20
  
  # Count failed logins by IP
  cat /var/log/auth.log | grep "Failed password" | \
    awk '{print $11}' | sort | uniq -c | sort -rn | head -10
  
  # Who is logged in right now
  w
  who
  last | head -20         # Recent login history
  lastb | head -20        # Failed login attempts
  
  # System logs
  journalctl -xe          # systemd journal
  journalctl -u ssh       # SSH service logs only
  journalctl --since "2024-01-01" --until "2024-01-02"
  ```
- **Lab:** On your VM, make 5 failed SSH login attempts (wrong password). Then analyse `/var/log/auth.log` to find them. What information is logged? IP, username, timestamp?
- **Complete:** First 3 steps of `lab-02-a.json`

---

## Week 2 — Windows Internals and Active Directory

**Goal:** Understand Windows from a security perspective — registry, processes, Event IDs, and AD architecture.

### Day 6 — Windows Architecture Deep Dive
- **Read:** `02-windows-active-directory.md` — Windows internals section
- **Setup:** Use a Windows VM (Windows 10/11 or Server 2019 eval from Microsoft — free 180-day trial)
- **Windows investigation commands:**
  ```powershell
  # System information
  systeminfo
  Get-ComputerInfo
  
  # Running processes
  Get-Process
  Get-Process | Sort-Object CPU -Descending | Select-Object -First 10
  
  # Network connections
  netstat -ano
  Get-NetTCPConnection | Where-Object State -eq "Established"
  
  # Services
  Get-Service | Where-Object Status -eq "Running"
  sc query
  
  # Scheduled tasks
  Get-ScheduledTask | Where-Object State -ne "Disabled"
  schtasks /query /fo LIST /v
  ```
- **Security task:** Run `netstat -ano` on your Windows machine. For each established connection, find the PID. Then look up that PID in Task Manager (Details tab). Are there any connections you don't recognise?

### Day 7 — Windows Registry Security
- **Registry deep dive:**
  - Open `regedit.exe` — explore the 5 hives: HKLM, HKCU, HKCR, HKU, HKCC
  - **Persistence locations attackers use:**
    ```
    HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
    HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
    HKLM\SYSTEM\CurrentControlSet\Services
    HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon
    ```
- **Hands-on:** Navigate to `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`. What programs autostart? Are there any you don't recognise?
- **Autoruns:** Download Sysinternals Autoruns (free from Microsoft). Run it. How many more autostart locations does it find vs just checking the registry key above?
- **Research task:** Look up "T1547.001 Boot or Logon Autostart Execution: Registry Run Keys" in the MITRE ATT&CK framework. What techniques do attackers use? How do defenders detect them?

### Day 8 — Windows Event Logs and Key Event IDs
- **Critical Event IDs to memorise:**
  | Event ID | Meaning | Why it matters |
  |----------|---------|----------------|
  | 4624 | Successful logon | Baseline activity |
  | 4625 | Failed logon | Brute force detection |
  | 4648 | Logon with explicit credentials (Pass-the-Hash) | Lateral movement |
  | 4672 | Special privileges assigned to new logon | Admin logon |
  | 4688 | New process created | Malware execution |
  | 4698 | Scheduled task created | Persistence |
  | 4720 | User account created | Privilege escalation |
  | 4732 | Member added to security group | Privilege change |
  | 7045 | New service installed | Persistence |
- **Hands-on Event Log analysis:**
  ```powershell
  # View security event log in PowerShell
  Get-EventLog -LogName Security -Newest 50
  Get-EventLog -LogName Security -InstanceId 4625 -Newest 20  # Failed logons
  Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4624} -MaxEvents 10
  ```
- **Scenario:** You receive an alert that there were 200 failed logon attempts (Event 4625) in 2 minutes on a Windows server, followed by one successful logon (Event 4624) from the same IP. Walk through exactly what you would investigate next.

### Day 9 — Active Directory Architecture
- **Read:** `02-windows-active-directory.md` — Active Directory section
- **AD concepts to master:**
  - Domain, Forest, Organisational Unit (OU), Trust
  - Domain Controller (DC) — the authentication authority
  - Kerberos authentication flow (AS-REQ, AS-REP, TGT, TGS)
  - LDAP — how AD stores and queries objects
  - Group Policy Objects (GPOs) — how security policy is enforced
- **PowerShell AD commands (on a domain-joined machine or AD lab):**
  ```powershell
  # If you have RSAT tools or an AD lab:
  Get-ADUser -Filter * | Select-Object Name, Enabled, LastLogonDate
  Get-ADGroupMember "Domain Admins"
  Get-ADComputer -Filter * | Select-Object Name, OperatingSystem
  Get-ADOrganizationalUnit -Filter * | Select-Object Name, DistinguishedName
  ```
- **Free AD lab:** Set up TryHackMe's "Active Directory Basics" room (free with account) — provides a browser-based Windows AD environment

### Day 10 — Active Directory Attacks (Theory + Detection)
- **Complete:** `lab-02-a.json` and `lab-02-b.json` — all 5 steps each
- **AD attack taxonomy:**
  1. **Credential harvesting:** Dumping LSASS memory (`mimikatz sekurlsa::logonpasswords`)
  2. **Kerberoasting:** Requesting TGS for SPNs and cracking offline
  3. **Pass-the-Hash:** Using NTLM hash without cracking it
  4. **Pass-the-Ticket:** Using stolen Kerberos ticket
  5. **DCSync:** Impersonating a DC to replicate all password hashes
  6. **Golden Ticket:** Forging a Kerberos TGT with KRBTGT hash
  7. **BloodHound:** Graph-based AD attack path discovery
- **Detection exercise:** For each attack above, write the Windows Event IDs that would detect it. (Research: "detecting kerberoasting event logs", etc.)

---

## Week 3 — Security Hardening and Incident Investigation

**Goal:** Apply defensive knowledge — harden systems, investigate incidents, write detection rules.

### Day 11 — Linux Hardening
- **SSH hardening (edit `/etc/ssh/sshd_config`):**
  ```bash
  Protocol 2
  PermitRootLogin no
  PasswordAuthentication no          # Key-based auth only
  MaxAuthTries 3
  AllowUsers specificuser
  Banner /etc/ssh/banner.txt
  ClientAliveInterval 300
  ClientAliveCountMax 2
  ```
- **Complete hardening checklist for a Linux web server:**
  - [ ] Disable root SSH login
  - [ ] Key-based authentication only
  - [ ] UFW/iptables firewall configured
  - [ ] Fail2ban installed (brute force protection)
  - [ ] Unneeded services disabled
  - [ ] `auditd` configured to log file changes
  - [ ] `/tmp` mounted with noexec option
  - [ ] Automatic security updates enabled
- **Hands-on:** Apply all of the above to your Ubuntu VM. Test each one works.

### Day 12 — Windows Hardening
- **Windows security hardening tasks:**
  ```powershell
  # Disable autorun
  Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" -Name "NoDriveTypeAutoRun" -Value 255
  
  # Enable Windows Defender (if disabled)
  Set-MpPreference -DisableRealtimeMonitoring $false
  
  # Check and enable Windows Firewall
  Get-NetFirewallProfile
  Set-NetFirewallProfile -All -Enabled True
  
  # Disable SMBv1 (EternalBlue target)
  Set-SmbServerConfiguration -EnableSMB1Protocol $false
  
  # Enable audit policies
  auditpol /set /subcategory:"Logon" /success:enable /failure:enable
  auditpol /set /subcategory:"Process Creation" /success:enable
  ```
- **Research task:** Why did the WannaCry ransomware spread so fast in 2017? What Windows vulnerability did it exploit? What patch would have prevented it? When was the patch available?

### Day 13 — Building a Home Security Lab
- **Homelab architecture exercise:**
  - Set up VirtualBox/VMware with: Ubuntu Server VM + Windows 10 VM
  - Configure: Host-only network so VMs can talk to each other but not internet
  - On Ubuntu: install Splunk Free (or ELK stack), configure to receive Windows event logs
  - On Windows: configure Windows Event Forwarding to send logs to your Ubuntu collector
- **If full lab isn't feasible:** Use TryHackMe "Windows Fundamentals" learning path (free) — provides a pre-built Windows environment

### Day 14 — Linux CTF Challenge
- **Complete "Bandit" wargame from OverTheWire (bandit.labs.overthewire.org):**
  - Levels 0-10: Basic file navigation, finding hidden files, reading files in weird encodings
  - Levels 11-20: Base64, ROT13, Unix pipes, SSH key auth
  - Document: for each level, write the command you used and why it worked
- **This is the best free Linux practice available** — don't rush it. If you get stuck, the solution is okay to look up, but understand it first

### Day 15 — Synthesis Day
- **Complete:** `exercises-02.md` — questions 1-15
- **Complete:** `linux-terminal-interactive.html` — all panels
- **Write a 1-page incident response brief:** "At 3am, you receive an alert that an unknown process on a Linux server is making outbound connections to 5.5.5.5. Walk through your investigation step by step. What commands do you run? What do you look for? When do you escalate?"

---

## Week 4 — Mastery, Assignment, and Portfolio

### Day 16-17 — Assignment Tasks 1-2
- Complete `assignment-02.md` Tasks 1 and 2

### Day 18-19 — Assignment Tasks 3-4
- Complete `assignment-02.md` Tasks 3 and 4
- Push all lab outputs to `/month-02-os-linux/` in your GitHub portfolio

### Day 20 — Final Review and Assessment
- **Complete:** `exercises-02.md` — questions 16-25
- **Final quiz:** `quiz-02.json` — all 15 questions
- **Competency self-check (can you do these without notes?):**
  - [ ] Navigate Linux file system and explain the purpose of 8 key directories
  - [ ] Read and explain `/etc/passwd` and `/etc/shadow` entries
  - [ ] Interpret `ls -la` output including SUID, SGID, and sticky bits
  - [ ] Find all SUID binaries on a Linux system and explain why they matter
  - [ ] Identify the 5 critical Windows Event IDs and explain what each means
  - [ ] Explain Kerberos authentication in 8 steps
  - [ ] Navigate the Windows Registry and identify persistence locations
  - [ ] Explain what Active Directory is and why it's a prime attacker target
  - [ ] Write a firewall rule in iptables syntax
  - [ ] Explain the difference between Pass-the-Hash and Kerberoasting
