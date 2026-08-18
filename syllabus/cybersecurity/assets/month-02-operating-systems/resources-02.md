# Month 2 Resources — Operating Systems & Linux

## Virtual Machines to Download

### 1. Kali Linux
**Purpose:** Penetration testing distro — pre-installed with security tools used throughout Phase 2  
**Download:** https://www.kali.org/get-kali/#kali-virtual-machines  
**Format:** Pre-built VirtualBox/VMware image (saves hours of setup)  
**Size:** ~3 GB compressed  
**Notes:** Download the VirtualBox image. Default credentials: `kali` / `kali`. Run `sudo apt update && sudo apt upgrade` on first boot.

---

### 2. Ubuntu Server 22.04 LTS
**Purpose:** The Linux server you'll defend, log, and administer throughout the course  
**Download:** https://ubuntu.com/download/server  
**Format:** ISO (install into a new VM)  
**Notes:** During install, enable OpenSSH Server when prompted. Use static IP for homelab. Ubuntu is the most common server OS in cloud environments.

---

### 3. Windows Server Evaluation (Optional)
**Purpose:** Active Directory lab — set up a Domain Controller  
**Download:** https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2022  
**Format:** ISO (180-day free evaluation)  
**Notes:** Required only if you want hands-on AD experience for the portfolio. Needs 4 GB RAM minimum. Run as a VM alongside your Kali and Ubuntu VMs.

---

### 4. Sysmon (System Monitor)
**Purpose:** Extended Windows event logging — captures process creation, network connections, file hash events that standard Event Viewer misses  
**Download:** https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon  
**Install:**
```powershell
.\Sysmon64.exe -accepteula -i sysmonconfig.xml
```
**Config file:** https://github.com/SwiftOnSecurity/sysmon-config (Swift on Security's config — widely used)  
**Notes:** Install on your Windows VM. Sysmon Event IDs 1 (process create), 3 (network connect), 11 (file create) are extremely useful for detection.

---

### 5. Windows Sysinternals Suite
**Purpose:** Advanced Windows diagnostics and investigation tools  
**Download:** https://learn.microsoft.com/en-us/sysinternals/downloads/sysinternals-suite  
**Key tools:**
- **Process Explorer**: Better Task Manager — shows parent-child process relationships
- **Autoruns**: Lists every auto-start location in the registry (persistence hunting)
- **TCPView**: Real-time network connections per process
- **ProcMon**: Real-time file/registry/network activity per process

---

## Online Learning Resources

### 1. TryHackMe — Linux Fundamentals Path
**URL:** https://tryhackme.com/path/outline/linux  
**Rooms:** Linux Fundamentals Part 1–3 (browser-based Linux terminal — no VM needed to start)  
**Covers:** Filesystem, permissions, processes, package management, logs, bash scripting

---

### 2. OverTheWire: Bandit (Linux CLI Practice)
**URL:** https://overthewire.org/wargames/bandit/  
**What it is:** 34-level command-line puzzle game over SSH. Each level requires Linux skills to find a password.  
**Why:** The best hands-on Linux CLI training that exists. Complete at least Level 0–15 by end of Month 2.
```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220   # Level 0 start
```

---

### 3. Microsoft Learn — Active Directory Fundamentals
**URL:** https://learn.microsoft.com/en-us/training/paths/active-directory-domain-services/  
**What it covers:** AD objects, group policy, authentication, Kerberos, LDAP. Free, self-paced, Microsoft official.

---

### 4. EventID.net — Windows Event ID Reference
**URL:** https://www.eventid.net/  
**What it is:** Searchable database of every Windows Event ID with descriptions and context. Bookmark this — you'll use it constantly.

---

### 5. Linux Journey
**URL:** https://linuxjourney.com/  
**What it covers:** Interactive browser-based lessons on Linux fundamentals — grasshopper through networking and advanced topics. Excellent visual reference with embedded quizzes.

---

## Reference Documents

| Resource | URL | Use |
|---------|-----|-----|
| Linux man pages (online) | https://man7.org/linux/man-pages/ | Any command reference |
| Bash scripting guide | https://tldp.org/LDP/abs/html/ | Scripting reference |
| Windows Event Log reference | https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/basic-audit-logon-events | Official Event ID docs |
| MITRE ATT&CK — Persistence | https://attack.mitre.org/tactics/TA0003/ | AD attack techniques |
| GTFOBins — Linux privesc | https://gtfobins.github.io/ | SUID/sudo abuse reference |
