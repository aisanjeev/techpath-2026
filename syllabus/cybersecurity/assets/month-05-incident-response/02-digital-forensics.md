# Digital Forensics: Memory, Disk, and Endpoint Artefacts

## What Is Digital Forensics?

Digital forensics is the scientific process of collecting, preserving, analysing, and presenting digital evidence in a way that maintains its integrity and is legally defensible. In an IR context, it answers the question: **"What exactly happened, and how do we prove it?"**

Key principles:
- **Preserve first, analyse second** — never work on original evidence
- **Verify integrity** — every action must be documented and hash-verified
- **Minimise footprint** — analysis should not alter the artefacts being examined
- **Document everything** — the evidence trail is only as good as your notes

---

## Evidence Hierarchy: Volatility vs Persistence

| Data Type | Persistence | Priority |
|-----------|-------------|---------|
| CPU registers / cache | Gone on shutdown | Capture first |
| RAM / running processes | Lost on reboot | Capture within minutes |
| Network connections | Closed when isolated | Second priority |
| Temp files / open handles | May be lost on reboot | Third |
| Disk data (NTFS, registry) | Survives reboot | Can wait |
| Backups / logs | Very stable | Can wait |

---

## Memory Forensics with Volatility 3

Memory forensics analyses a snapshot of RAM to find what was running — including malware that never touched disk (fileless attacks).

### Why Memory Forensics?

Many modern attacks are:
- **Fileless** — live entirely in PowerShell or process memory, no executable on disk
- **Injected** — malicious code hidden inside legitimate processes like `svchost.exe`
- **Anti-forensic** — designed to delete artefacts from disk after execution

Memory is the only place these attacks leave traces.

### Memory Acquisition

Always capture RAM before isolating or rebooting:

```bash
# Windows (run as admin)
winpmem.exe output.raw

# Hyper-V / VMware — take a snapshot and use .vmem file
# Or use Sysinternals ProcDump for individual process:
procdump.exe -ma -accepteula svchost.exe svchost.dmp
```

### Critical Volatility 3 Analysis Workflow

```
1. windows.info.Info          → Confirm OS version, architecture
2. windows.pstree.PsTree      → Process parent-child map
3. windows.cmdline.CmdLine    → Full command lines (spot encoded PowerShell)
4. windows.netstat.NetStat    → Network connections per process
5. windows.malfind.Malfind    → Injected code detection
6. windows.dlllist.DllList    → DLLs loaded per process (spot unsigned)
7. windows.svcscan.SvcScan    → Services (including hidden)
8. windows.psscan.PsScan      → Pool tag scan (finds DKOM-hidden processes)
9. windows.handles.Handles    → Open file/registry handles (reveals access patterns)
```

### Spotting Malicious Processes

| Red Flag | Example | What It Suggests |
|----------|---------|-----------------|
| Unusual parent process | `cmd.exe` spawned by `outlook.exe` | Phishing macro execution |
| Runs from temp path | `C:\Users\bob\AppData\Local\Temp\svchost.exe` | Malware posing as system process |
| No version info | `lsass.exe` with no Microsoft version info | Process masquerading |
| Two copies | Two `lsass.exe` running simultaneously | Process hollowing |
| Unexpected network | `notepad.exe` with external TCP connection | Injected C2 code |
| Missing from pslist but in psscan | Process name + PID found by pool scan only | DKOM rootkit hiding the process |

---

## Disk Forensics with Autopsy

### Evidence Acquisition

```bash
# Create forensic image with dc3dd (Linux)
dc3dd if=/dev/sdb of=/mnt/external/evidence.img hash=sha256 log=acq.log

# Verify: SHA256 of original == SHA256 of image
sha256sum /dev/sdb > original.sha256
sha256sum /mnt/external/evidence.img > image.sha256

# Windows: Use FTK Imager (GUI) or:
# dd if=\\.\PhysicalDrive1 of=C:\evidence\disk.img bs=512
```

### Windows Forensic Artefacts Cheatsheet

| Artefact | Location | What It Reveals |
|----------|----------|-----------------|
| MFT (Master File Table) | `$MFT` (NTFS root) | All files ever created, MAC timestamps |
| LNK files (shortcuts) | `%APPDATA%\Roaming\Microsoft\Windows\Recent\` | Recently accessed files |
| Prefetch | `C:\Windows\Prefetch\*.pf` | Which executables ran and when (last 8 runs) |
| Amcache | `C:\Windows\AppCompat\Programs\Amcache.hve` | Hash and path of recently executed files |
| Shimcache (AppCompatCache) | SYSTEM registry hive | Executables that touched the filesystem |
| UserAssist | `NTUSER.DAT\...\Explorer\UserAssist` | GUI applications run by user |
| Jump Lists | `%APPDATA%\Roaming\Microsoft\Windows\Recent\AutomaticDestinations\` | Recent files per application |
| Browser History | Chrome: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\History` | URLs visited, downloads |
| Registry Run Keys | `HKLM\SOFTWARE\...\CurrentVersion\Run` | Persistence mechanism |
| SAM / SECURITY | `C:\Windows\System32\config\SAM` | Local user accounts and password hashes |
| Event Logs | `C:\Windows\System32\winevt\Logs\` | Security events, application events |
| Shadow Copies (VSS) | `\\?\GLOBALROOT\Device\HarddiskVolumeShadowCopyN` | Previous versions of files |

### Timeline Analysis Methodology

```
Step 1: Set the time zone (UTC always for forensics)
Step 2: Run Timeline in Autopsy or plaso (log2timeline)
Step 3: Identify T0 (first indicator of compromise)
Step 4: Work backwards from T0 to find delivery event
Step 5: Work forwards from T0 to trace lateral movement
Step 6: Build table: [UTC timestamp] | [Artifact] | [Path] | [Significance]
```

### Recovering Deleted Files

Deleted files in NTFS are not immediately overwritten — only their MFT record is flagged as unallocated. Tools can carve the file from unallocated space:

```bash
# Autopsy: Right-click deleted file → Extract File(s)

# Command-line with TSK (The Sleuth Kit):
fls -r -d disk.img              # list deleted files
icat disk.img <inode_number> > recovered_file.exe  # extract by inode

# Carve by file signature (finds files even without MFT entry):
foremost -i disk.img -o recovered/ -t exe,pdf,doc,zip
```

---

## Sysmon: Advanced Windows Logging

Sysmon fills the gaps in Windows native logging by capturing:
- Full process command lines with hashes (Event ID 1)
- Network connections per process (Event ID 3)
- DNS lookups per process (Event ID 22)
- File and registry changes (Event IDs 11, 12, 13)
- Process injection indicators (Event IDs 8, 10, 25)

### Detecting Common ATT&CK Techniques with Sysmon

| ATT&CK Technique | Sysmon Detection |
|-----------------|-----------------|
| T1059.001 PowerShell | Event 1: `powershell.exe` with `-enc` or `-NoP -NonI` |
| T1003.001 LSASS Dump | Event 10: `lsass.exe` accessed by non-Microsoft process |
| T1055 Process Injection | Event 8: CreateRemoteThread from unexpected source |
| T1071.004 DNS C2 | Event 22: Unusual domain queried by `svchost` or common app |
| T1547.001 Run Keys | Event 13: Value set in `HKLM\...\CurrentVersion\Run` |
| T1070 Clear Logs | Event 1: `wevtutil.exe cl Security` |

---

## Velociraptor: Enterprise-Scale Hunting

When you need to hunt across 1,000+ endpoints simultaneously, Velociraptor is the tool:

```bash
# Start local Velociraptor server (for lab use)
velociraptor gui

# Collect process list from all connected endpoints:
# In the Hunt Manager UI → New Hunt → Windows.System.Pslist

# VQL query to find suspicious network connections:
SELECT Pid, Name, LocalAddr, LocalPort, RemoteAddr, RemotePort, Status
FROM netstat()
WHERE RemoteAddr != "0.0.0.0" 
  AND RemoteAddr != "::"
  AND NOT RemoteAddr =~ "^192\\.168\\."
  AND NOT RemoteAddr =~ "^10\\."
```
