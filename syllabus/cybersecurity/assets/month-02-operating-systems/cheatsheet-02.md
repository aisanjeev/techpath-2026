# Month 2 Cheatsheet — Operating Systems & Linux

## Windows Critical Event IDs
| Event ID | Log | Event | Alert On |
|---------|-----|-------|---------|
| 4624 | Security | Successful logon | Unusual hours, unknown IPs |
| 4625 | Security | Failed logon | >5 in 1 min = brute force |
| 4634 | Security | Logoff | — |
| 4648 | Security | Explicit credential logon | Lateral movement |
| 4672 | Security | Special privilege logon | Admin sessions |
| 4688 | Security | Process created | `cmd.exe`, `powershell.exe` spawned by Office |
| 4698 | Security | Scheduled task created | Persistence |
| 4720 | Security | User account created | Backdoor account |
| 4728 | Security | Added to global group | Privilege escalation |
| 4732 | Security | Added to local group | Privilege escalation |
| 4768 | Security | Kerberos TGT requested | Kerberoasting |
| 7045 | System | Service installed | Malware persistence |
| 1102 | Security | Audit log cleared | Anti-forensics attempt |

## Linux File Permissions
| Mode | Symbolic | Who Can | Common Use |
|------|---------|---------|-----------|
| 400 | r-------- | Owner reads | Private keys (~/.ssh/id_rsa) |
| 600 | rw------- | Owner reads/writes | /etc/shadow, private configs |
| 644 | rw-r--r-- | Owner rw, all read | Web files, config files |
| 700 | rwx------ | Owner full | Scripts, directories |
| 755 | rwxr-xr-x | Owner full, all r+x | Binaries, public dirs |
| 777 | rwxrwxrwx | Everyone full | NEVER in production |
| 4755 | rwsr-xr-x | SUID bit | Run as file owner (root) |
| 1777 | rwxrwxrwt | Sticky bit | /tmp — only owner deletes |

**Octal formula:** Owner | Group | Other, each = R(4)+W(2)+X(1)

## Linux Command Reference
| Command | Purpose | Example |
|---------|---------|---------|
| `ls -la` | Long list with hidden files | `ls -la /etc/` |
| `find` | Search files | `find / -perm -4000 2>/dev/null` (SUID) |
| `grep -rn` | Recursive search with line nums | `grep -rn "password" /etc/` |
| `awk` | Field processing | `awk -F: '{print $1}' /etc/passwd` |
| `sed` | Stream editor | `sed 's/old/new/g' file.txt` |
| `cut` | Extract columns | `cut -d: -f1,3 /etc/passwd` |
| `sort \| uniq -c` | Count occurrences | `cut -d: -f1 /etc/passwd \| sort` |
| `netstat -tlnp` | Listening services with PIDs | Ports open and who owns them |
| `ss -tlnp` | Modern replacement for netstat | `ss -tlnp \| grep :22` |
| `lsof -i :80` | What process uses port 80 | `lsof -i :443` |
| `ps aux` | All processes, all users | `ps aux \| grep nginx` |
| `chmod` | Change permissions | `chmod 755 /var/www/html` |
| `chown` | Change owner | `chown www-data:www-data /var/www` |
| `sudo -l` | List sudo rights | Run as any user |
| `crontab -l` | List cron jobs | `crontab -e` to edit |
| `history` | Command history | `cat ~/.bash_history` |
| `last` | Login history | `lastb` for failures |
| `who / w` | Logged-in users | Current sessions |
| `tar -czf` | Compress | `tar -czf archive.tar.gz /dir/` |

## /etc/passwd Format
```
username:x:UID:GID:comment:home:shell
root:x:0:0:root:/root:/bin/bash
alice:x:1001:1001:Alice Smith:/home/alice:/bin/bash
nobody:x:65534:65534::/nonexistent:/usr/sbin/nologin
```
- `x` = password hash in /etc/shadow
- UID 0 = root (any account with UID 0 has root privileges)
- Shell of `/usr/sbin/nologin` = no interactive login

## /etc/shadow Format
```
username:$hash_type$salt$hash:last_changed:min:max:warn:inactive:expire
```
- `$6$` = SHA-512 | `$5$` = SHA-256 | `$1$` = MD5 (weak) | `$y$` = yescrypt

## Systemd Quick Reference
| Command | Purpose |
|---------|---------|
| `systemctl status <svc>` | Current status and last log lines |
| `systemctl start/stop/restart` | Control service |
| `systemctl enable/disable` | Auto-start on boot |
| `systemctl list-units --type=service` | All services |
| `journalctl -u <svc>` | Service-specific logs |
| `journalctl -f` | Follow all logs live |
| `journalctl --since "2024-01-01"` | Logs since date |
| `journalctl -p err` | Errors only |

## Active Directory Quick Reference
| Object | Description | Tool |
|--------|-------------|------|
| User | Account for a person | ADUC, net user /domain |
| Computer | Machine account | ADUC |
| Group | Collection of users | ADUC, net group /domain |
| GPO | Group Policy Object — config push | gpmc.msc |
| OU | Organisational Unit — container | ADUC |
| DC | Domain Controller — auth server | dcpromo |

## PowerShell Security Commands
| Command | Purpose |
|---------|---------|
| `Get-Process` | Running processes |
| `Get-Service` | Windows services |
| `Get-LocalUser` | Local accounts |
| `Get-LocalGroupMember Administrators` | Who's admin? |
| `Get-NetTCPConnection -State Listen` | Open ports |
| `Get-WinEvent -LogName Security` | Security event log |
| `Get-ItemProperty HKLM:\...\Run` | Startup entries |
| `Invoke-WebRequest` | HTTP requests |
| `Test-NetConnection -Port 445` | Port connectivity test |
| `Get-FileHash -Algorithm SHA256` | File hash |
