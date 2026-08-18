# Month 5 — Practice Exercises: Incident Response & Digital Forensics

**25 exercises with worked answers.**

---

## Section A: IR Lifecycle (Questions 1-8)

**Q1.** A junior analyst says "We detected the incident, so the preparation phase is over — we're now in detection." Is this correct? Explain the actual relationship between the four NIST IR phases.

**Answer:** This is incorrect. The four NIST IR phases (Preparation, Detection & Analysis, Containment/Eradication/Recovery, Post-Incident Activity) are not strictly sequential — they can overlap, and Preparation is continuous, not a phase you complete once.

Preparation runs in parallel with all other phases: during an active incident, you may realise your preparation was insufficient (no forensic toolkit available, communication tree hasn't been updated) and need to improve it even while responding. After the Post-Incident Activity, improved preparation feeds back to prevent the next incident.

The correct model: Preparation is the foundation. Detection triggers the response cycle. Post-Incident activity feeds back into improved preparation, closing the loop. Many incidents also require cycling back — eradication is incomplete, new systems are discovered as compromised, and you return to containment.

---

**Q2.** You are the incident commander for a P1 incident: ransomware is actively spreading across the corporate network. List your first 10 actions in priority order and justify each.

**Answer:**
1. **Activate the IR team** (call all on-call responders, notify CISO) — you need all hands immediately
2. **Identify the scope** — query SIEM/EDR for how many hosts show ransomware indicators. Is this 1 host or 500? This determines the response scale.
3. **Contact Legal and Cyber Insurance** — cyber insurance needs early notification to preserve claim validity; legal needs to advise on regulatory notification requirements
4. **Identify the spread vector** — is ransomware spreading via network shares (block immediately) or lateral movement (isolate affected segment)?
5. **Segment the network** — disable network shares, isolate affected VLANs. This stops the spread without completely cutting off all systems.
6. **Identify and preserve patient zero** — the initial infection point is the most valuable forensic artefact. Take a memory dump before isolating.
7. **Assess backup status** — which backups exist and when were they last tested? Are the backups themselves encrypted?
8. **Do NOT reboot infected machines** — rebooting may destroy volatile evidence (memory, active network connections). Isolate but keep powered on for forensics.
9. **Check for decryptor** — consult nomoreransom.org with the ransomware note text. If there's a free decryptor, eradication is much simpler.
10. **Begin documented timeline** — every action taken must be timestamped. This is critical for insurance claims, legal proceedings, and PIR.

---

**Q3.** What is the "order of volatility" in digital forensics? Why must evidence be collected in this order, and what happens if you reboot a compromised system before collecting memory?

**Answer:** The order of volatility ranks evidence from most to least volatile (i.e., most likely to be lost first):
1. CPU registers, CPU cache (lost immediately on process change)
2. Routing tables, ARP cache, process table, kernel statistics (lost on reboot)
3. **Memory / RAM** (lost on reboot)
4. Temporary file systems, pagefile.sys, swap (modified frequently; some lost on reboot)
5. Disk (persistent, but can be modified)
6. Remote logging, network monitoring (may be overwritten over time)
7. Physical configuration (changes rarely)
8. Archival/backup media (most stable)

**If you reboot before collecting memory:** You permanently lose: all running processes (including the malware process and what it was doing), active network connections (C2 addresses, data being transferred), decryption keys held in memory (ransomware often holds its symmetric key in memory briefly), evidence of fileless malware (lives only in memory, nothing on disk), and potentially the malware itself (if it was injected into memory with no file on disk).

Memory evidence is the most valuable and the most fragile. A 16GB memory dump takes about 5-10 minutes to acquire. Always do this before isolation or reboot.

---

**Q4.** Explain chain of custody in digital forensics. Why does it matter even for corporate (non-law enforcement) incidents?

**Answer:** Chain of custody is the documented record of who collected evidence, what they did with it, where it was stored, and who had access to it at every point in time. Every step is logged with signatures.

**Why it matters for corporate incidents (not just criminal):**
1. **Legal action against the attacker:** If the organisation wants to pursue criminal charges or a civil lawsuit, any evidence must be admissible. Evidence without chain of custody can be challenged as potentially tampered with.
2. **HR/employment decisions:** If an insider threat is discovered, the investigation may lead to employee dismissal. Without chain of custody, the employee's legal team can challenge the evidence.
3. **Regulatory investigations:** DPDP Act, RBI audits, and other regulatory enquiries may require proving evidence wasn't modified.
4. **Insurance claims:** Cyber insurers may dispute claims if they believe the investigation methodology was flawed.

**Practical requirements:**
- Evidence must be collected using write blockers (to prevent modifying the disk)
- Hash the evidence immediately after collection (MD5/SHA-256) — proves integrity
- Store in secure location with access log
- Any examination must be on a copy, not the original

---

**Q5.** During a forensic investigation of a compromised Linux server, you run `ps aux` and notice a process named `kworker/u24:3` with a network connection to `5.5.5.5`. Is this suspicious? How do you investigate?

**Answer:** **Yes, this is suspicious.** `kworker` is a legitimate Linux kernel worker thread name, but legitimate kworker processes: run in kernel space (not user space), have very low PIDs (close to 1), don't make network connections (kernel threads don't use TCP sockets), and their `/proc/PID/exe` link points to something like `[kworker/u24:3]` (in brackets), not a real binary path.

**Investigation:**
```bash
# Get the PID (let's say it's 4521)
ps aux | grep kworker

# Check what binary is actually running
ls -la /proc/4521/exe       # Should be brackets [kworker] for real thread, or a suspicious path

# Check the actual binary path
cat /proc/4521/cmdline      # What command was it started with?

# Check open files
ls -la /proc/4521/fd/       # What files does it have open?

# Check network connections
cat /proc/4521/net/tcp      # Network connections for this PID's namespace

# Check parent process
cat /proc/4521/status | grep PPid  # Parent PID — what spawned this?

# Check when it was created (birth time from /proc/stat)
ls -la /proc/4521           # Directory creation time = process start time

# Check if it has environment variables that reveal its purpose
cat /proc/4521/environ | tr '\0' '\n'
```

A real `kworker` thread would show: parent PID 2 (kthreadd, the kernel thread spawner), no network connections, no real executable path. If it shows a user home directory as executable path and an external connection — it's malware masquerading as a kernel thread.

---

**Q6.** What is "timestomping" and why does it complicate forensic investigations? What techniques do forensic investigators use to detect it?

**Answer:** Timestomping is the deliberate modification of file timestamps (Created, Modified, Accessed, Changed — the MACE times) to disguise when a file was created or last accessed. Attackers use it to make malware files appear as if they were created years ago (blending in with old system files) or to confuse timeline analysis.

**How it complicates investigation:** If an attacker created a malicious tool on the system and timestomped it to show "Created: 2019-01-01", a forensic analyst building a timeline might not associate it with the compromise that happened yesterday. The attack chain becomes unclear.

**Detection techniques:**
1. **$MFT vs $STANDARD_INFORMATION mismatch:** The NTFS filesystem stores timestamps in two places — the $STANDARD_INFORMATION attribute (user-visible, modifiable) and the $FILE_NAME attribute (only modified by the OS when a file is created/renamed). Timestomping tools typically only modify $STANDARD_INFORMATION. If these don't match, timestomping occurred.
2. **Timestamp precision:** Windows NTFS timestamps are accurate to 100ns, but many timestomping tools write timestamps with 0 nanoseconds — a forensic artifact of the tool itself.
3. **Log correlation:** Correlate file timestamps with event logs. If a file was "created in 2019" but an Event 4688 shows the same filename being executed yesterday, the creation time is false.
4. **Prefetch correlation:** Windows Prefetch records the first execution time of executables. If prefetch shows first execution yesterday but the file "was created in 2019" — timestomping.

---

**Q7.** Explain the difference between "containment" and "eradication" in the NIST IR model. Give a specific example of when incomplete eradication causes re-infection.

**Answer:**
**Containment:** Stop the incident from spreading further. The threat is still present but isolated. Actions: network isolation of the compromised host, blocking C2 IP at firewall, disabling the compromised account.

**Eradication:** Remove the threat entirely — malware, persistence mechanisms, attacker access. Actions: delete malware files, remove scheduled tasks, reset passwords, close the initial access vector.

**Example of incomplete eradication causing re-infection:**
A company detects ransomware on FILE-SERVER-01. They:
1. Isolate FILE-SERVER-01 ✓
2. Reimaged the server from backup ✓
3. Restore files from last clean backup ✓
4. Return FILE-SERVER-01 to production ✓

What they forgot: The attacker also created a backdoor user account on the Active Directory domain controller BEFORE the ransomware was deployed. They left a Cobalt Strike beacon running on DC-01. 3 days after restoration, the attacker uses the backdoor to re-deploy ransomware — this time successfully targeting 200 servers.

**Lesson:** Eradication must be domain-wide, not just on the initially detected host. The forensic investigation must identify the FULL attack chain and scope before declaring eradication complete.

---

**Q8.** Write a bash script that collects live incident response data from a Linux system (triage script).

**Answer:**
```bash
#!/bin/bash
# Linux Live Triage Script — run as root
# Collects volatile and semi-volatile evidence for IR

OUTPUT_DIR="/tmp/ir_$(hostname)_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT_DIR"

echo "[+] Starting triage on $(hostname) at $(date)"
echo "[+] Output directory: $OUTPUT_DIR"

# System info
echo "[*] Collecting system information..."
uname -a > "$OUTPUT_DIR/uname.txt"
hostname >> "$OUTPUT_DIR/uname.txt"
uptime >> "$OUTPUT_DIR/uname.txt"
date >> "$OUTPUT_DIR/uname.txt"

# Currently logged in users
echo "[*] Collecting user sessions..."
w > "$OUTPUT_DIR/current_users.txt"
who >> "$OUTPUT_DIR/current_users.txt"
last -20 >> "$OUTPUT_DIR/recent_logins.txt"
lastb -20 >> "$OUTPUT_DIR/failed_logins.txt" 2>/dev/null

# Running processes
echo "[*] Collecting process list..."
ps auxf > "$OUTPUT_DIR/processes.txt"
ps auxf --sort=-%cpu > "$OUTPUT_DIR/processes_by_cpu.txt"

# Network connections
echo "[*] Collecting network state..."
ss -tlnp > "$OUTPUT_DIR/listening_ports.txt"
ss -tnp > "$OUTPUT_DIR/connections.txt"
ip route > "$OUTPUT_DIR/routes.txt"
arp -a > "$OUTPUT_DIR/arp_cache.txt"
cat /proc/net/tcp > "$OUTPUT_DIR/proc_tcp.txt"

# Open files by process
echo "[*] Collecting open files..."
lsof -nP > "$OUTPUT_DIR/open_files.txt" 2>/dev/null

# Scheduled tasks
echo "[*] Collecting scheduled tasks..."
crontab -l > "$OUTPUT_DIR/crontab_root.txt" 2>/dev/null
cat /etc/crontab >> "$OUTPUT_DIR/crontab_system.txt"
ls -la /etc/cron.d/ >> "$OUTPUT_DIR/crontab_system.txt"

# User accounts
echo "[*] Collecting user information..."
cat /etc/passwd > "$OUTPUT_DIR/passwd.txt"
cat /etc/group > "$OUTPUT_DIR/groups.txt"

# SUID/SGID files
echo "[*] Searching for SUID/SGID files..."
find / -perm -4000 -o -perm -2000 2>/dev/null > "$OUTPUT_DIR/suid_sgid.txt"

# Recently modified files
echo "[*] Finding recently modified files..."
find / -mtime -3 -type f -not -path "/proc/*" -not -path "/sys/*" 2>/dev/null \
    > "$OUTPUT_DIR/recent_files_3d.txt"

# Authentication logs
echo "[*] Collecting auth logs..."
cp /var/log/auth.log "$OUTPUT_DIR/auth.log" 2>/dev/null
cp /var/log/secure "$OUTPUT_DIR/secure.log" 2>/dev/null

# Package integrity (check if system binaries modified)
echo "[*] Checking package integrity..."
dpkg --verify 2>/dev/null > "$OUTPUT_DIR/pkg_verify.txt" \
    || rpm -Va 2>/dev/null > "$OUTPUT_DIR/pkg_verify.txt"

# Hash the triage output for integrity verification
echo "[*] Hashing output files..."
sha256sum "$OUTPUT_DIR"/* > "$OUTPUT_DIR/MANIFEST_SHA256.txt"

echo "[+] Triage complete. Files in: $OUTPUT_DIR"
echo "[+] Hash manifest: $OUTPUT_DIR/MANIFEST_SHA256.txt"
```

---

## Section B: Digital Forensics (Questions 9-15)

**Q9.** You have a memory image and need to investigate it with Volatility3. Write the sequence of commands you would run for a suspected malware infection investigation.

**Answer:**
```bash
# Step 1: Identify OS and build information
python3 vol.py -f memory.raw windows.info.Info

# Step 2: List all processes with parent relationships
python3 vol.py -f memory.raw windows.pstree.PsTree
# Look for: processes with unusual parents (cmd.exe spawned by Word.exe),
# processes with suspicious names (svchost without parent services.exe),
# multiple instances of normally-single processes (two lsass.exe)

# Step 3: Get command lines for all processes
python3 vol.py -f memory.raw windows.cmdline.CmdLine
# Look for: encoded PowerShell, wget/curl to external IPs, suspicious paths

# Step 4: Check network connections at time of capture
python3 vol.py -f memory.raw windows.netstat.NetStat
# Look for: connections to external IPs, unusual ports, ESTABLISHED connections
# by svchost, rundll32 (red flags)

# Step 5: Find injected code (malware often injects into legitimate processes)
python3 vol.py -f memory.raw windows.malfind.MalFind
# Shows memory regions that are: executable, not backed by a file, suspicious characteristics

# Step 6: List loaded DLLs (malware may load malicious DLLs)
python3 vol.py -f memory.raw windows.dlllist.DllList
# Look for DLLs in temp directories, AppData, unusual paths

# Step 7: Dump suspicious process for static analysis
python3 vol.py -f memory.raw windows.dumpfiles.DumpFiles --pid 4521 --dump-dir ./dumped/
# Then: strings dumped_file | grep -i "http\|cmd\|powershell"

# Step 8: Check registry run keys from memory
python3 vol.py -f memory.raw windows.registry.printkey.PrintKey \
    --key "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"

# Step 9: Scan for known malware patterns
python3 vol.py -f memory.raw windows.yarascan.YaraScan --yara-rules mimikatz.yar
```

---

**Q10.** What are Windows Prefetch files and what forensic value do they provide? Write a PowerShell script to parse and display prefetch data.

**Answer:** Windows Prefetch files (`C:\Windows\Prefetch\*.pf`) record executable usage to speed up loading. For forensics, they prove a program was executed — even if the program has since been deleted.

Each prefetch file records:
- The executable name and path
- The number of times it was run
- The last 8 run times (Windows 10/11)
- Files and directories the program accessed on startup

**Forensic value:** Attacker deletes `mimikatz.exe` from disk — but `MIMIKATZ.EXE-E64CFDC2.pf` remains in Prefetch, proving it ran. The embedded timestamps show exactly when it ran.

```powershell
# Parse Windows Prefetch files (requires admin rights)
# Note: A full parser needs binary parsing; this shows the basics using a helper tool

# Method 1: Use WinPrefetchView (free Nirsoft tool) or
# Method 2: Parse with PowerShell using a module

# Quick approach - list prefetch files with timestamps
Get-ChildItem "C:\Windows\Prefetch" -Filter "*.pf" |
    Sort-Object LastWriteTime -Descending |
    Select-Object @{N="ExeName";E={$_.Name -replace "-[A-F0-9]+\.pf$"}},
                  @{N="LastRun";E={$_.LastWriteTime}},
                  @{N="PfFile";E={$_.Name}} |
    Format-Table -AutoSize

# For full parsing including run count and all 8 timestamps:
# Use PECmd by Eric Zimmerman (free, from github.com/EricZimmerman)
# PECmd.exe -d "C:\Windows\Prefetch" --csv C:\Output
```

---

**Q11.** During a Windows forensic investigation, you discover the file `C:\Users\jsmith\AppData\Roaming\Microsoft\Windows\Recent\Q4_Financial_Report.lnk`. What is this file, what information can you extract from it, and what does its presence suggest?

**Answer:** This is a **Windows Shell Link file** (LNK file / shortcut). Windows automatically creates LNK files in the `\Recent\` folder every time a user opens a file. The LNK file points to the original file's location.

**Information extractable from LNK metadata:**
- Target file path (where the document lived)
- Target file size
- Target file creation, modification, and access timestamps AT THE TIME IT WAS OPENED
- Volume serial number of the drive where the file was stored
- NetBIOS name of the machine (if accessed from a network share)
- Drive type (local, removable, network)
- Whether it was accessed from a local drive, USB, or network share

**Forensic significance:**
- Proves jsmith accessed a file named `Q4_Financial_Report` regardless of whether the file or its parent folder still exists
- If the LNK shows the target was on a USB drive (drive type = removable), it suggests a USB was connected and data may have been copied to it
- The timestamp embedded in the LNK (target file times) may differ from current file timestamps on disk, revealing timestomping
- Even if the original file has been deleted, the LNK proves it existed and was opened

**Tools:** Eric Zimmerman's `LECmd.exe` (free) parses LNK files into CSV for easy analysis.

---

**Q12.** What is the Windows Registry's `ShimCache` (AppCompatCache) and `Amcache.hve`? What forensic value do each provide during malware investigations?

**Answer:**
**ShimCache (Application Compatibility Cache):**
- Stored in: `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\AppCompatCache`
- Records: every executable that runs on the system, with the executable path and last modification time
- Forensic value: Proves a program EXISTED on the system and the OS processed it. Important: ShimCache records executables that WERE SEEN by the Windows loader, not necessarily that they executed. But in practice, they were almost certainly executed.
- Survives deletion: If attacker deletes malware exe, ShimCache still records it ran.
- Tool: AppCompatCacheParser.exe (Eric Zimmerman)

**Amcache.hve:**
- Location: `C:\Windows\AppCompat\Programs\Amcache.hve` (Windows 8+)
- Records: executable files that were run, with SHA-1 hash, publisher, install date, last execution time
- Forensic value: Provides the SHA-1 HASH of executed files — even deleted ones! You can query VirusTotal with the hash to identify if the executed program was malware.
- Amcache is more reliable than ShimCache for proving execution.

Together, they provide a comprehensive execution history that persists even after file deletion — critical for proving "yes, this malware ran on this system" even if the attacker cleaned up.

---

**Q13.** A forensic examiner says "the file was deleted so we can't recover it." Is this always true on modern systems? Explain file system deletion and 3 methods for recovering deleted files.

**Answer:** Not necessarily true — deletion does NOT immediately erase file data in most cases.

**What actually happens when you delete a file (NTFS):**
1. The file's directory entry is marked as deleted
2. The $MFT (Master File Table) record is marked as available
3. The clusters holding the data are marked as free in the $Bitmap
4. The actual data remains on disk until those clusters are overwritten by new data

**3 recovery methods:**
1. **MFT carving:** Even if the MFT record is reused, tools like `TestDisk` or `Autopsy` can read the raw $MFT and find records marked as deleted but with intact metadata (filename, timestamps, size, cluster pointers). If the clusters haven't been overwritten — file is fully recoverable.

2. **File carving:** Search raw disk sectors for known file signatures (magic bytes). JPG starts with `FF D8 FF`, PDF with `%PDF`, ZIP with `PK`. Tools like `Photorec` or `Autopsy`'s carver find these patterns even without any filesystem metadata — works even if MFT is overwritten.

3. **Volume Shadow Copy / VSS:** Windows automatically creates snapshots at restore points and Windows Update. Previous versions of deleted files may exist in shadow copies. Mount them with: `mklink /d C:\shadow \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\`

**When files ARE unrecoverable:** SSD TRIM (controller zeroes blocks immediately after deletion), full-disk encryption with key destruction, secure erase tools (`shred`, `sdelete`), or prolonged use after deletion (sectors overwritten many times).

---

**Q14.** You are analysing network traffic captured during an incident and see this pattern:
```
09:23:01 Internal 10.0.1.50 → External 185.143.223.X  HTTP GET /check.php  
09:23:61 Internal 10.0.1.50 → External 185.143.223.X  HTTP GET /check.php  
09:24:01 Internal 10.0.1.50 → External 185.143.223.X  HTTP GET /check.php  
[repeats every 60 seconds for 4 hours]
09:25:01 Internal 10.0.1.50 ← External 185.143.223.X  HTTP 200 command=upload&file=/etc/passwd
09:25:02 Internal 10.0.1.50 → External 185.143.223.X  HTTP POST /upload.php [47KB]
```
What is happening? What malware behaviour does this represent?

**Answer:** This is a **C2 (Command-and-Control) beaconing** pattern followed by **data exfiltration**.

**Beaconing analysis:** The host 10.0.1.50 is checking in with the C2 server at exactly 60-second intervals — classic malware "heartbeat." The malware polls `/check.php` to receive new commands. The regularity (exactly 60 seconds) is itself an indicator — legitimate user traffic is not this regular.

**Command received:** The C2 server responds with `command=upload&file=/etc/passwd` — instructing the malware to exfiltrate the `/etc/passwd` file.

**Exfiltration:** The host immediately POSTs 47KB (the `/etc/passwd` contents encoded/compressed) to `/upload.php`.

**Indicators of Compromise:**
- IP: 185.143.223.X (external C2)
- URL patterns: `/check.php` (beacon), `/upload.php` (exfiltration endpoint)
- Beaconing period: 60 seconds
- Data sent: Contents of `/etc/passwd`

**Response:**
1. Block 185.143.223.X and the full /24 at firewall
2. Isolate 10.0.1.50
3. Determine what process is making these HTTP requests (check Sysmon Event 3 or `/proc/PID/net/tcp`)
4. Determine what other files were exfiltrated (examine all POST requests to this IP)
5. Check if other internal hosts are beaconing to the same IP

---

**Q15.** Write a Python script that parses Windows Security Event Log (EVTX format) to extract all failed logon attempts and produce a summary report.

**Answer:**
```python
import subprocess, json, re
from collections import Counter, defaultdict
from datetime import datetime

def parse_security_events_powershell() -> list:
    """Use PowerShell to extract Windows Security events (cross-platform via subprocess)"""
    ps_cmd = """
    Get-EventLog -LogName Security -InstanceId 4625 -Newest 1000 |
    Select-Object TimeGenerated, 
        @{N='Account';E={$_.ReplacementStrings[5]}},
        @{N='Domain';E={$_.ReplacementStrings[6]}},
        @{N='LogonType';E={$_.ReplacementStrings[10]}},
        @{N='SourceIP';E={$_.ReplacementStrings[19]}},
        @{N='FailureReason';E={$_.ReplacementStrings[8]}} |
    ConvertTo-Json
    """
    result = subprocess.run(['powershell', '-Command', ps_cmd], 
                            capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return []

def analyse_failed_logons(events: list) -> None:
    ip_counter = Counter()
    user_counter = Counter()
    hourly = defaultdict(int)
    logon_types = {
        '2': 'Interactive', '3': 'Network', '4': 'Batch',
        '5': 'Service', '7': 'Unlock', '8': 'NetworkCleartext',
        '10': 'RemoteInteractive', '11': 'CachedInteractive'
    }
    
    for event in events:
        ip = event.get('SourceIP', 'Unknown')
        user = event.get('Account', 'Unknown')
        ltype = event.get('LogonType', '?')
        
        if ip and ip not in ('', '-', '::1', '127.0.0.1'):
            ip_counter[ip] += 1
        if user and user not in ('', '-'):
            user_counter[user] += 1
        
        # Parse hour from timestamp
        ts = event.get('TimeGenerated', '')
        try:
            dt = datetime.strptime(ts[:19], '%Y-%m-%dT%H:%M:%S')
            hourly[dt.strftime('%Y-%m-%d %H:00')] += 1
        except (ValueError, TypeError):
            pass
    
    print("=" * 60)
    print("FAILED LOGON ANALYSIS REPORT")
    print("=" * 60)
    print(f"\nTotal failed logons analysed: {len(events)}")
    
    print("\n--- TOP 10 SOURCE IPs ---")
    for ip, count in ip_counter.most_common(10):
        flag = " ⚠ HIGH VOLUME" if count > 50 else ""
        print(f"  {ip:<20} {count:>5} attempts{flag}")
    
    print("\n--- TOP 10 TARGETED USERNAMES ---")
    for user, count in user_counter.most_common(10):
        print(f"  {user:<25} {count:>5} attempts")
    
    print("\n--- HOURLY ACTIVITY (last 24h) ---")
    for hour in sorted(hourly)[-24:]:
        bar = "█" * min(hourly[hour] // 5, 40)
        print(f"  {hour} | {bar} ({hourly[hour]})")
    
    print("\n--- RECOMMENDATIONS ---")
    if ip_counter.most_common(1):
        top_ip, top_count = ip_counter.most_common(1)[0]
        if top_count > 20:
            print(f"  • Block {top_ip} — {top_count} failures (suspected brute force)")
    
    if any(u.lower() in ('administrator', 'admin', 'root') for u in user_counter):
        print("  • Privileged account being targeted — consider renaming or disabling default admin")

events = parse_security_events_powershell()
analyse_failed_logons(events)
```

---

## Section C: Forensic Scenarios (Questions 16-20)

**Q16.** Create a complete incident timeline from these disjointed log entries. Identify the attack chain and map each step to a MITRE ATT&CK technique.

```
[13:42] Email gateway: "Invoice_Q4.docm" received by finance@company.com from invoice@supp1ier-uk.com
[13:45] Endpoint: Word.exe spawned PowerShell.exe with encoded command
[13:46] Network: DNS query for "update.malware-cdn.ru" from 10.0.2.50 (FINANCE-PC-03)
[13:46] Network: HTTPS connection established to 91.240.118.50:443 from 10.0.2.50
[13:47] Endpoint: Sysmon Event 11 - file created C:\Users\fjones\AppData\Roaming\update_svc.exe
[13:48] Registry: HKCU\Software\Microsoft\Windows\CurrentVersion\Run modified — value "MSUpdate" = "C:\Users\fjones\AppData\Roaming\update_svc.exe"
[13:52] Network: DNS queries to "91-240-118-50.in-addr.arpa" resolving to "c2.malware-cdn.ru"
[16:30] AD: New logon (Type 3) by fjones on FILESERVER-01 from 10.0.2.50
[16:32] Endpoint: FILESERVER-01 — xcopy C:\Finance\ \\10.0.2.50\C$\Users\fjones\Downloads\
[17:15] Network: 2.3GB outbound transfer to 91.240.118.50 via HTTPS
```

**Answer:**
**Reconstructed Timeline and ATT&CK Mapping:**

| Time | Event | ATT&CK Technique |
|------|-------|-----------------|
| 13:42 | Spear phishing email with malicious Word macro attachment arrives | T1566.001 — Phishing: Spearphishing Attachment |
| 13:45 | User opens document; macro runs; Word spawns PowerShell | T1204.002 — Malicious File + T1059.001 — PowerShell |
| 13:46 | PowerShell resolves C2 domain | T1071.004 — C2 over DNS |
| 13:46 | Malware establishes HTTPS connection to C2 (91.240.118.50) | T1071.001 — C2 over HTTP |
| 13:47 | Malware drops `update_svc.exe` to AppData | T1105 — Ingress Tool Transfer |
| 13:48 | Persistence via Registry Run key | T1547.001 — Registry Run Keys |
| 13:52 | Continued C2 beaconing | T1071.001 — Application Layer Protocol |
| 16:30 | Lateral movement: fjones authenticates to FILESERVER-01 | T1021.002 — SMB/Windows Admin Shares |
| 16:32 | Data collection: copies Finance folder to local machine | T1074.001 — Local Data Staging |
| 17:15 | Exfiltration: 2.3GB over HTTPS to C2 | T1048.002 — Exfiltration Over C2 Channel |

**Root cause:** Spear phishing email with `.docm` (macro-enabled Word document). Typosquatting sender domain `supp1ier-uk.com` (number 1 instead of letter l). Attack achieved initial access → persistence → lateral movement → data exfiltration within 4 hours.

---

**Q17.** A CISO asks you: "We found evidence that the attacker was in our network for 45 days before we detected them. What should our dwell time target be and how do we reduce it?"

**Answer:** **Target:** Dwell time under 24 hours for P1 incidents (active breach with exfiltration). Under 72 hours for lateral movement without confirmed exfiltration.

**Current context:** 45 days is above industry average but not unusual for organisations without mature security programs. The 2024 Mandiant M-Trends report shows median dwell time of 10 days globally — organisations with robust detection programmes can achieve this.

**How to reduce dwell time:**

1. **Expand detection coverage (biggest impact):**
   - Map current SIEM rules to ATT&CK — identify which techniques have zero detection coverage
   - 45-day dwell time suggests the initial access and early-stage techniques were undetected
   - Add detection for: LOLBin abuse, new scheduled tasks, DNS to newly-registered domains, LSASS access

2. **Deploy endpoint detection (EDR):** Agents that capture process genealogy, file writes, and registry changes provide the telemetry needed to detect lateral movement

3. **Threat hunting programme:** Proactively hunt for known attacker techniques weekly, don't wait for rules to fire

4. **Honeypots/deception technology:** Place fake credentials, fake file shares, and fake systems that trigger immediate alerts if touched — there's no legitimate reason to access them

5. **External attack surface monitoring:** Detect if your domains or IPs appear in threat intelligence feeds (early warning that attackers are interested in you)

---

**Q18.** Explain what "evidence preservation" means in a digital forensics context. Write a procedure for creating a forensically-sound copy of a hard drive.

**Answer:** Evidence preservation means capturing evidence in a way that: (1) doesn't modify the original, (2) creates a verifiable copy (hashed), and (3) documents the process for chain of custody.

**Forensically-sound disk imaging procedure:**
```bash
# Equipment needed:
# - Write blocker (hardware: Tableau, Wiebetech — prevents any write to original disk)
# - Forensic workstation with sufficient storage
# - Chain of custody form

# Step 1: Connect the suspect disk through a write blocker
# (hardware write blocker is mandatory for legal admissibility)

# Step 2: Document the disk before acquisition
lsblk -o NAME,SIZE,SERIAL,MODEL    # Note disk serial number, size, model
# Fill in chain of custody: disk serial, date, your name, case number

# Step 3: Create forensic image with dcfldd (better than dd — hashes in real time)
# Or use FTK Imager (Windows, free GUI)
dcfldd if=/dev/sdb \
       of=/evidence/case001/disk.E01 \
       hash=sha256 \
       hashlog=/evidence/case001/hash.log \
       hashwindow=1G \
       bs=512 \
       conv=noerror,sync     # Continue past read errors

# Step 4: Verify the image hash matches
sha256sum /dev/sdb > /evidence/case001/source_hash.txt
sha256sum /evidence/case001/disk.E01 > /evidence/case001/image_hash.txt
# Compare: hashes must be identical

# Step 5: Document in chain of custody:
# - Time acquisition started
# - Time acquisition completed  
# - Hash value of original
# - Hash value of image
# - Your name and signature

# Step 6: NEVER work on the original — mount the IMAGE read-only for analysis
mount -o ro,loop /evidence/case001/disk.E01 /mnt/analysis
```

---

**Q19.** What is DFIR (Digital Forensics and Incident Response)? How does the forensics mindset differ from the incident response mindset, and how do the two disciplines complement each other?

**Answer:**
**DFIR** combines both disciplines in the same team or individual. Most major incidents require both simultaneously.

**IR mindset:** "Stop the bleeding. Protect the business. Return to normal operations as fast as possible." Focus: speed, containment, business continuity. Sometimes trades forensic thoroughness for speed (e.g., reimaging a system quickly rather than taking a full forensic image first).

**Forensics mindset:** "Preserve evidence exactly as it is. Document everything. Don't contaminate the scene. Attribution matters." Focus: evidence integrity, completeness, admissibility. May slow response (proper acquisition takes time) but is essential for legal action and comprehensive understanding.

**The tension:** IR wants to reimage the compromised server immediately to restore service. Forensics needs to image it first. The IR team may want to reset passwords and kick the attacker out; the forensics team wants to observe attacker behaviour a bit longer to understand the full scope.

**How they complement each other:**
- Forensic evidence gathered during IR reveals the full attack chain, helping IR teams find ALL compromised systems (not just the first one found)
- IR's containment stops the attacker from destroying more evidence
- Post-incident forensic analysis improves future IR procedures
- Both feed into the PIR (Post-Incident Review) that improves overall security posture

**Best practice:** DFIR teams have pre-defined "forensic first" procedures for high-value systems (DCs, database servers) where even a few minutes of forensic acquisition before containment is worth the risk, and "respond first" for wide-spreading incidents (ransomware) where every second of spread means more damage.

---

**Q20.** You are building an IR playbook for Business Email Compromise (BEC). Write the complete playbook covering detection through post-incident activity.

**Answer:**

---
**BEC Incident Response Playbook v1.0**

**Trigger:** Finance reports suspicious wire transfer request; email security flags impersonation; user reports unusual executive request

**Phase 1 — Detection and Initial Assessment (0-30 minutes)**
1. Determine: is the executive's mailbox COMPROMISED or was the email SPOOFED?
   - Compromised: email came from the real executive account
   - Spoofed: email came from look-alike domain (`ceo@acme-c0rp.com`)
   - Check: email headers → `Received-From` chain → does the sending server match the legitimate domain?
2. Escalate to CISO and Legal immediately — financial crime involved

**Phase 2 — Containment (30-60 minutes)**
- If mailbox compromised:
  - Reset executive's password + revoke all active sessions (Azure AD → Revoke token)
  - Enable MFA on the account immediately
  - Preserve the mailbox before any changes (Legal hold in O365)
  - Check: did attacker set up inbox rules (forward all to attacker)?
    - O365: `Get-InboxRule -Mailbox ceo@company.com | Where-Object {$_.ForwardTo}`
- Block spoofed domain at email gateway
- Alert all users: "Do not process wire transfer requests via email without phone verification"

**Phase 3 — Financial Recovery (immediate, parallel to above)**
- Contact Finance — was the transfer completed? How recently?
- If transfer < 24 hours: call the sending bank immediately — request wire recall
- If transfer > 24 hours: call receiving bank — may be able to freeze account
- File report with RBI Cyber Crime Portal (www.cybercrime.gov.in)
- Contact cyber insurance carrier

**Phase 4 — Investigation (1-72 hours)**
- Timeline of mailbox access: when did the attacker log in? From where?
- What other emails did the attacker read/send?
- Were other employees targeted with similar requests?
- How did the attacker gain access? (Phishing? Password spray? Credential from breach?)

**Phase 5 — Post-Incident**
- Update email security: DMARC policy to `p=reject`, add DKIM and SPF
- Train Finance: all wire requests over ₹1 lakh require voice verification with a known number
- Implement approval workflow: no single person can authorise large transfers via email alone

---

## Section D: Advanced Forensics (Questions 21-25)

**Q21.** What is the difference between a forensic image (E01) and a logical copy? When would you use each?

**Answer:**
**Forensic Image (E01/dd/AFF4):** A bit-for-bit copy of the ENTIRE storage device — every sector, including deleted files, unallocated space, slack space, and filesystem metadata. Verifiable with cryptographic hash. Captures evidence that's "invisible" to the operating system: deleted files, fragments of old files in slack space, hidden partitions.
**Use when:** Criminal investigations, regulatory matters, when deleted file recovery is needed, any situation requiring legal admissibility.

**Logical Copy:** A file-system-level copy of selected files/folders (`xcopy`, `rsync`, cloud backup sync). Copies only files the OS can "see" — no deleted files, no slack space, no unallocated data. Cannot be verified with a sector hash.
**Use when:** Quick collection for business continuity (get the documents back), when the disk is unavailable for imaging (cloud storage), low-severity matters where deleted content isn't relevant, and when speed is critical and legal admissibility isn't required.

**Rule of thumb:** For criminal/HR matters, always image. For operational recovery where speed matters, logical copy may suffice — but document why imaging wasn't done.

---

**Q22.** Explain what the Windows NTFS Master File Table ($MFT) is and why it's so valuable for forensic investigations.

**Answer:** The $MFT (Master File Table) is the NTFS filesystem's database of every file and directory. Each record (1KB or 4KB) contains: file name, size, timestamps (Created, Modified, Accessed, Changed — the MACE times), attributes, and cluster locations.

**Forensic value:**
1. **Evidence of deleted files:** When a file is deleted, its $MFT record is marked as available but often not immediately overwritten. Forensic tools can parse the raw $MFT binary and find these "deleted" records with intact metadata.

2. **Two sets of timestamps:** The $STANDARD_INFORMATION attribute contains the user-visible MACE timestamps (modifiable by timestomping tools). The $FILE_NAME attribute contains timestamps set by the kernel that are MUCH harder to modify. If they differ, timestomping occurred.

3. **Directory hierarchy reconstruction:** Even if a folder was deleted, the $MFT records can reveal what was in it.

4. **Sequence number:** Each $MFT record has a sequence number incremented on reuse. If an attacker deletes a file and creates a new one that reuses the MFT record slot, forensic tools can detect this by comparing the MFT entry's sequence number with expected values.

**Tools:** MFTECmd by Eric Zimmerman (free) — parses raw $MFT into CSV timeline format.

---

**Q23.** What is Volatility's `malfind` plugin and what does it detect? Write an analysis workflow for a suspicious process found by malfind.

**Answer:** `malfind` hunts for injected code in process memory. It finds memory regions that are:
- Marked executable (the `PAGE_EXECUTE_*` protection flag)
- Not backed by a file on disk (a legitimate DLL would have a file backing)
- Beginning with `MZ` or shellcode signatures

This pattern indicates code injection: attackers inject shellcode or DLLs into legitimate processes (`explorer.exe`, `svchost.exe`) to hide malicious activity.

**Analysis workflow for a malfind hit:**
```bash
# Step 1: Find injected regions
python3 vol.py -f memory.raw windows.malfind.MalFind
# Output shows: PID, Process name, Virtual Address, Size, Protection, hexdump

# Step 2: Examine the suspicious process
python3 vol.py -f memory.raw windows.pstree.PsTree | grep -A5 "SUSPICIOUS_PID"
# Is the parent process legitimate? (svchost.exe should be children of services.exe)

# Step 3: Dump the injected region for static analysis
python3 vol.py -f memory.raw windows.dumpfiles.DumpFiles --pid SUSPICIOUS_PID --dump-dir ./dump/

# Step 4: Analyse the dumped region
strings ./dump/file.*.dmp | grep -iE "http|cmd|powershell|CreateThread|VirtualAlloc"
file ./dump/file.*.dmp  # Is it a PE? Shellcode?

# Step 5: Hash and check threat intel
sha256sum ./dump/file.*.dmp
# Submit hash to VirusTotal

# Step 6: Check network connections from this PID
python3 vol.py -f memory.raw windows.netstat.NetStat | grep "SUSPICIOUS_PID"

# Step 7: Write indicators
# - PID of compromised host process
# - VA range of injection
# - SHA256 of injected code
# - Any network indicators from the dump
```

---

**Q24.** What are PCAP (packet capture) files and what can a forensic analyst extract from them during an incident investigation?

**Answer:** A PCAP (Packet CAPture) file contains raw network traffic captured at the packet level — the complete content of all network packets (headers and payload) during a capture window.

**What forensic analysts can extract:**
1. **HTTP traffic:** If unencrypted (HTTP not HTTPS), see exact URLs visited, form data submitted (credentials), file downloads, cookies
2. **DNS queries:** Every domain a host looked up, even for domains that were blocked. Reveals C2 domain names, exfiltration channels, reconnaissance.
3. **Email traffic (SMTP/IMAP):** If unencrypted, read the actual email content and attachments
4. **File transfers:** Extract transferred files (HTTP objects, FTP files, SMB transfers) using Wireshark: `File → Export Objects → HTTP`
5. **TLS metadata:** Even for encrypted HTTPS — you can see: which domains (from SNI field in TLS ClientHello), certificate details, size and timing of transfers
6. **Attack patterns:** Scan signatures, exploit attempts, lateral movement (SMB to multiple hosts), C2 beaconing regularity
7. **Credentials:** In cleartext protocols (Telnet, FTP, HTTP basic auth) — directly readable passwords
8. **Adversary TTPs:** Timing between requests, User-Agent strings, packet sizes — can sometimes fingerprint specific malware families

**Key tools:** Wireshark (GUI), `tshark` (CLI), `zeek` (protocol analysis), `suricata` (IDS on PCAP)

---

**Q25.** Write a forensic investigation report template that meets professional standards for a corporate security incident. Include all required sections.

**Answer:**

---
**CONFIDENTIAL — INCIDENT INVESTIGATION REPORT**

**Case Reference:** [Case Number]  
**Classification:** [Restricted / Confidential]  
**Report Author:** [Name, Title, Certifications]  
**Report Date:** [Date]  
**Incident Date:** [Date(s) of incident]  
**Status:** [Draft / Final]

---
**EXECUTIVE SUMMARY**  
[1-2 paragraphs, non-technical. What happened, when, what was impacted, what was done, current status. Written for CISO / Board. No technical jargon.]

---
**INCIDENT OVERVIEW**

| Field | Detail |
|-------|--------|
| Incident ID | |
| Severity | P1 / P2 / P3 |
| Classification | Malware / BEC / Data Breach / Insider |
| Date Detected | |
| Date Contained | |
| Dwell Time | |
| Systems Affected | |
| Data Potentially Impacted | |

---
**TIMELINE OF EVENTS**

| UTC Timestamp | Event | Evidence Source |
|--------------|-------|----------------|
| | Initial compromise | |
| | Lateral movement | |
| | Detection | |
| | Containment | |

---
**TECHNICAL FINDINGS**

**Initial Access:** [How attacker entered]  
**Persistence:** [How attacker maintained access]  
**Lateral Movement:** [How attacker spread]  
**Objective Achieved:** [What the attacker did]

**MITRE ATT&CK Mapping:**

| Tactic | Technique ID | Technique Name |
|--------|-------------|---------------|
| | | |

---
**INDICATORS OF COMPROMISE (IoCs)**

**File Hashes:** [SHA256 of malware]  
**IP Addresses:** [C2 servers, attacker IPs]  
**Domains:** [C2 domains]  
**Registry Keys:** [Persistence keys]  
**File Paths:** [Malware locations]

---
**ROOT CAUSE ANALYSIS**  
[What allowed this to happen — technical and process gaps]

**RECOMMENDATIONS**  

| Priority | Recommendation | Owner | Due Date |
|----------|---------------|-------|---------|
| P0 | | | |
| P1 | | | |

---
**EVIDENCE LOG**

| Evidence ID | Description | Hash (SHA256) | Collected By | Date |
|------------|-------------|--------------|-------------|------|
| | | | | |

---
**APPENDICES**  
A: Raw log extracts  
B: Malware analysis results  
C: Network traffic analysis  
D: Forensic tool outputs
