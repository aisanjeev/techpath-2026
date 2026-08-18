# Month 2: Operating Systems & Linux — Revision Notes

## 1. Windows Process & Service Model

### Processes
- Every program runs as a **process** with a unique PID
- View in **Task Manager** (Ctrl+Shift+Esc) or via CLI:
  ```powershell
  Get-Process                        # All processes
  Get-Process -Name "notepad"        # Specific process
  tasklist /v                         # Verbose process list
  ```
- Critical system processes: `lsass.exe` (credential store), `winlogon.exe`, `csrss.exe`, `svchost.exe`
- `lsass.exe` is a prime malware target — credential dumping (Mimikatz)

### Windows Services
- Background processes managed by the Service Control Manager (SCM)
- Stored in registry: `HKLM\SYSTEM\CurrentControlSet\Services`
  ```powershell
  Get-Service                        # List all services
  Get-Service | Where-Object {$_.Status -eq "Running"}
  sc query                            # CLI equivalent
  sc start/stop <ServiceName>
  ```
- **Startup types**: Automatic, Automatic (Delayed), Manual, Disabled
- Persistence via malicious services is common (Event ID 7045 = new service installed)

---

## 2. Windows Registry

- Hierarchical database storing OS and application configuration
- **Hives**: `HKLM` (Local Machine), `HKCU` (Current User), `HKCR`, `HKU`, `HKCC`

| Key Path | Purpose |
|----------|---------|
| `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` | Auto-start on boot (all users) |
| `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` | Auto-start (current user) |
| `HKLM\SYSTEM\CurrentControlSet\Services` | Service definitions |
| `HKLM\SAM` | Local account hashes (locked) |
| `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion` | OS version, install info |

```powershell
# Check for persistence in Run keys
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
Get-ItemProperty "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
```

---

## 3. Windows Event Log — Critical Event IDs

| Event ID | Category | Meaning | Security Relevance |
|---------|----------|---------|-------------------|
| 4624 | Logon | Successful logon | Baseline normal activity |
| 4625 | Logon | Failed logon | Brute force indicator — watch for spikes |
| 4634/4647 | Logoff | Account logoff | Session duration analysis |
| 4648 | Logon | Logon with explicit credentials | Lateral movement indicator |
| 4672 | Logon | Special privileges assigned | Admin login |
| 4688 | Process | New process created | Malware execution, PowerShell abuse |
| 4698 | Task Scheduler | Scheduled task created | Persistence mechanism |
| 4720 | Account | New user account created | Backdoor account creation |
| 4728/4732 | Account | User added to security group | Privilege escalation |
| 4768 | Kerberos | Kerberos TGT requested | AD auth — Kerberoasting indicator |
| 7045 | Service | New service installed | Malware/persistence via service |

```powershell
# View failed logons in PowerShell
Get-EventLog -LogName Security -InstanceId 4625 -Newest 20
# Or with newer cmdlet:
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4625} -MaxEvents 20
```

---

## 4. Active Directory (AD)

### Core Concepts
- **Domain**: Logical grouping of users, computers, and resources
- **Domain Controller (DC)**: Server hosting AD — authenticates users, enforces policy
- **Forest**: Collection of one or more domains sharing a schema
- **OU (Organisational Unit)**: Container for organising objects; GPOs are linked here
- **GPO (Group Policy Object)**: Configuration pushed from DC to all machines in an OU

### Authentication Protocols
- **Kerberos** (default in AD): Ticket-based; DC issues TGT, services issue service tickets
- **NTLM**: Legacy challenge-response; used when Kerberos unavailable (weak — susceptible to Pass-the-Hash)

### Common AD Attack Paths
| Attack | Description |
|--------|-------------|
| Pass-the-Hash | Use NTLM hash without knowing plaintext password |
| Kerberoasting | Request service tickets; crack offline |
| AS-REP Roasting | Exploit accounts without pre-auth |
| DCSync | Mimic DC to dump all password hashes |
| Golden Ticket | Forge Kerberos TGT using krbtgt hash |

---

## 5. Linux Filesystem & Permissions

### Key Directories
| Path | Contents |
|------|---------|
| `/etc` | System configuration files |
| `/var/log` | Log files |
| `/home` | User home directories |
| `/root` | Root user home |
| `/tmp` | Temporary files (world-writable — persistence target) |
| `/bin`, `/usr/bin` | User binaries |
| `/sbin`, `/usr/sbin` | Admin binaries |
| `/proc` | Virtual filesystem — running process info |
| `/etc/passwd` | User accounts (readable by all) |
| `/etc/shadow` | Password hashes (root only) |
| `/etc/sudoers` | sudo privilege rules |

### File Permissions (rwx)
```
-rwxr-xr-- 1 alice devs 4096 Aug 1 12:00 script.sh
 ^^^ ^^^ ^^^
 |   |   └── Other: r-- (read only)
 |   └────── Group (devs): r-x (read + execute)
 └────────── Owner (alice): rwx (full)
```

| Permission | Symbolic | Octal |
|-----------|---------|-------|
| Read | r | 4 |
| Write | w | 2 |
| Execute | x | 1 |

**Common octal values:**
- `755` = rwxr-xr-x (web server files)
- `644` = rw-r--r-- (config files)
- `600` = rw------- (private keys, `/etc/shadow`)
- `777` = rwxrwxrwx (insecure — never use on production)

```bash
chmod 755 script.sh           # Set permissions
chown alice:devs file.txt     # Change owner and group
chmod +x script.sh            # Add execute permission
chmod -R 644 /var/www/html    # Recursive
```

---

## 6. Users & Privilege Model

```bash
whoami                        # Current user
id                            # UID, GID, groups
cat /etc/passwd               # All accounts (name:x:uid:gid:desc:home:shell)
sudo cat /etc/shadow          # Password hashes (root required)
sudo -l                       # What can current user sudo?
su - alice                    # Switch to user alice (needs password)
sudo su -                     # Become root via sudo
useradd -m -s /bin/bash bob   # Create user with home dir
passwd bob                    # Set password
usermod -aG sudo bob          # Add to sudo group
```

---

## 7. Essential Linux CLI

```bash
# Process management
ps aux                    # All running processes
top / htop                # Real-time process monitor
kill -9 <PID>             # Force-kill process
systemctl status nginx    # Service status
systemctl start/stop/restart nginx
crontab -l               # List cron jobs (current user)
cat /etc/cron*            # System-wide cron jobs

# Log analysis
tail -f /var/log/auth.log         # Live SSH/auth events
grep "Failed password" /var/log/auth.log
journalctl -u ssh --since "1 hour ago"
journalctl -p err                  # Errors only
last                               # Login history
lastb                              # Failed logins
who                                # Currently logged in

# Searching
find / -name "*.conf" 2>/dev/null  # Find config files
find /home -newer /tmp/ref         # Files modified recently
grep -rn "password" /etc/ 2>/dev/null
```

---

## 8. PowerShell Security Reference

```powershell
Get-Process | Where-Object {$_.CPU -gt 50}    # High CPU processes
Get-NetTCPConnection -State Listen             # Listening ports
Get-LocalUser                                  # Local user accounts
Get-LocalGroupMember Administrators            # Who's an admin?
Invoke-WebRequest -Uri "https://example.com"  # HTTP request
Get-WinEvent -LogName Security -MaxEvents 50   # Security events
Get-ChildItem -Path HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
Test-NetConnection -ComputerName 192.168.1.1 -Port 445  # Port check
```
