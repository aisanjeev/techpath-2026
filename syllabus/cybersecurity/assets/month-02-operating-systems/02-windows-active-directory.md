# Windows Security and Active Directory

## Windows Architecture: A Defender's Perspective

### Process Model

Windows runs applications as processes, each isolated in its own virtual address space. The kernel (ntoskrnl.exe) runs in a privileged mode; user applications run in user mode with restricted hardware access.

**Security boundaries:**
- Each process has a security token defining its privileges and user identity
- Integrity Levels (Low, Medium, High, System) limit what processes can access
- UAC (User Account Control) enforces a privilege elevation prompt before High/System actions

**Key system processes (legitimate baseline):**
| Process | Description | Note |
|---------|-------------|------|
| `System` | Kernel and device drivers | PID 4, parent is none |
| `smss.exe` | Session Manager | Starts winlogon, csrss |
| `lsass.exe` | Local Security Authority | Manages auth tokens, stores creds |
| `winlogon.exe` | Windows Logon | Handles Ctrl+Alt+Del |
| `csrss.exe` | Client/Server Runtime | Windows subsystem |
| `services.exe` | Service Control Manager | Parent of all svchost.exe |
| `svchost.exe` | Service Host | Multiple instances, each hosting services |
| `explorer.exe` | Windows Shell | Desktop, file manager |

**Anomaly detection:** `lsass.exe` should have one instance, spawned by `wininit.exe`. If you see `lsass.exe` spawned by `cmd.exe` or with an unusual path — it's malware. Use Process Explorer (Sysinternals) to verify process paths and parent-child relationships.

---

## Windows Registry: Configuration and Persistence

The registry is a hierarchical database storing system and application settings. It is a primary persistence mechanism for malware.

### Hive Structure

| Hive | Abbreviation | Scope |
|------|-------------|-------|
| HKEY_LOCAL_MACHINE | HKLM | System-wide settings (all users) |
| HKEY_CURRENT_USER | HKCU | Current user settings |
| HKEY_CLASSES_ROOT | HKCR | File associations |
| HKEY_USERS | HKU | Settings for all user profiles |

### Critical Security Registry Paths

```
# Auto-start locations (persistence targets):
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce
HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce

# Services (each service has a key here):
HKLM\SYSTEM\CurrentControlSet\Services\

# Security Account Manager (user hashes — locked while OS runs):
HKLM\SAM

# OS version and install info:
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion
```

```powershell
# Inspect startup entries:
Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
Get-ItemProperty 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'

# Use Autoruns (Sysinternals) for comprehensive startup visibility — shows
# browser extensions, scheduled tasks, services, drivers, all in one view.
```

---

## Windows Event Log: Detection Reference

### Log Locations

| Log Name | Contents | File Path |
|----------|---------|----------|
| Security | Logon, privilege use, audit | `C:\Windows\System32\winevt\Logs\Security.evtx` |
| System | Service start/stop, hardware, crashes | `System.evtx` |
| Application | App errors and information | `Application.evtx` |
| Sysmon/Operational | Process, network, file activity | Requires Sysmon install |
| PowerShell/Operational | Script execution | `Microsoft-Windows-PowerShell%4Operational.evtx` |

### Logon Types (in Event ID 4624)

| Type | Value | Description | Attack Context |
|------|-------|-------------|---------------|
| Interactive | 2 | Local keyboard logon | Normal desktop |
| Network | 3 | SMB, RPC, named pipes | Lateral movement |
| Batch | 4 | Scheduled task logon | Task persistence |
| Service | 5 | Service startup logon | Malicious service |
| Remote Interactive | 10 | RDP logon | Remote access |
| Cached Interactive | 11 | Cached domain creds | Offline logon |

```powershell
# Filter logons by type (e.g., find all network logons):
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4624} |
  Where-Object {$_.Message -like '*Logon Type:*3*'} |
  Select-Object -First 10 | Format-List
```

---

## Active Directory Architecture

### Core Components

```
Forest (mycompany.com)
└── Domain (mycompany.com)
    ├── Domain Controller(s)  ← Auth server, hosts AD database (ntds.dit)
    ├── Organisational Units (OUs)
    │   ├── OU: London
    │   │   ├── Users: alice, bob
    │   │   ├── Computers: LAPTOP-001, DESKTOP-002
    │   │   └── GPO: London-Policy linked here
    │   └── OU: Servers
    │       ├── Computers: WEB-01, DB-01
    │       └── GPO: Server-Hardening linked here
    ├── Groups
    │   ├── Security Groups: Domain Admins, IT-Staff
    │   └── Distribution Groups: AllStaff (email lists)
    └── Group Policy Objects (GPOs)
```

### Authentication Flow (Kerberos)

```
1. User logs on → sends username to DC
2. DC verifies user exists → issues TGT (Ticket Granting Ticket)
   TGT encrypted with krbtgt account's hash — only DC can decrypt
3. User presents TGT to DC → requests service ticket for \\fileserver
4. DC issues service ticket encrypted with fileserver's account hash
5. User presents service ticket to fileserver
6. Fileserver decrypts ticket → grants access
```

**Why Kerberos matters for attacks:**
- **Kerberoasting**: Request a service ticket for any SPN — it's encrypted with the service account's hash → crack offline
- **AS-REP Roasting**: Accounts with "Do not require Kerberos preauthentication" → request TGT → crack offline
- **Golden Ticket**: Compromise krbtgt hash → forge any TGT → unlimited domain access
- **Pass-the-Ticket**: Steal a TGT/service ticket from memory (Mimikatz) → present it as your own

### Common AD Commands (Standard User Context)

```powershell
# Requires RSAT or must be run on domain-joined machine
# Query domain users
Get-ADUser -Filter * | Select-Object Name, SamAccountName, Enabled
Get-ADUser -Identity alice -Properties *

# Query groups
Get-ADGroup -Filter *
Get-ADGroupMember -Identity "Domain Admins"

# Query computers
Get-ADComputer -Filter * | Select-Object Name, IPv4Address, LastLogonDate

# Find accounts that haven't logged in for 90 days (stale accounts = risk)
$cutoff = (Get-Date).AddDays(-90)
Get-ADUser -Filter {LastLogonDate -lt $cutoff -and Enabled -eq $true}

# Find accounts with password never expires (risk)
Get-ADUser -Filter {PasswordNeverExpires -eq $true} | Select-Object Name
```

---

## PowerShell for Security Operations

### Execution Policy (Important First Step)

```powershell
Get-ExecutionPolicy -List           # Show current policy per scope
Set-ExecutionPolicy RemoteSigned    # Allow local scripts, require signing for remote
# Note: attackers bypass this with: powershell.exe -ep bypass -c "..."
```

### Security Investigation Workflows

```powershell
# --- Who is on the system? ---
Get-LocalUser | Select-Object Name, Enabled, LastLogon, PasswordLastSet
Get-LocalGroupMember -Group 'Administrators'

# --- What's running? ---
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10 Name, Id, CPU, Path
# Check for processes without a path (injected/reflective loading):
Get-Process | Where-Object {$_.Path -eq $null}

# --- What's listening on the network? ---
Get-NetTCPConnection -State Listen | Select-Object LocalAddress, LocalPort, OwningProcess |
  ForEach-Object {
    $proc = Get-Process -Id $_.OwningProcess -ErrorAction SilentlyContinue
    [PSCustomObject]@{Port=$_.LocalPort; Process=$proc.Name; PID=$_.OwningProcess}
  } | Sort-Object Port

# --- File hash verification (integrity check) ---
Get-FileHash C:\Windows\System32\lsass.exe -Algorithm SHA256
Get-FileHash C:\path\to\suspicious.exe -Algorithm MD5

# --- Check for auto-start entries ---
$runKeys = @(
  'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run',
  'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
)
$runKeys | ForEach-Object { Get-ItemProperty $_ }

# --- Decode base64 PowerShell commands (common attacker obfuscation) ---
$encoded = "cG93ZXJzaGVsbA=="   # attacker's encoded payload
[System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String($encoded))
```

### Remote Investigation

```powershell
# Test network connectivity
Test-NetConnection -ComputerName 192.168.1.10 -Port 445
Test-NetConnection -ComputerName fileserver.domain.com -Port 80

# Download a file (also used by attackers — watch in logs)
Invoke-WebRequest -Uri "https://example.com/file.txt" -OutFile "C:\temp\file.txt"

# Execute on remote machine (requires WinRM enabled)
Invoke-Command -ComputerName Server01 -ScriptBlock { Get-Process | Where-Object {$_.CPU -gt 50} }
```
