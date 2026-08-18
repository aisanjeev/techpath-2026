# Month 5 — Cheatsheet: Incident Response & Digital Forensics

## NIST IR Phase Quick Reference

| Phase | Trigger | Primary Actions | Output |
|-------|---------|-----------------|--------|
| Prepare | N/A (ongoing) | IR plan, playbooks, tools, training | Runbooks, contact lists |
| Identify | Alert / user report | Triage, enrich, declare incident | Incident ticket, severity |
| Contain | Confirmed incident | Isolate host, block C2, disable accounts | Isolation confirmation |
| Eradicate | Scope understood | Remove malware, patch vuln, close access | Clean bill of health |
| Recover | Eradication complete | Rebuild systems, restore data, monitor | Return to service |
| Learn | Incident closed | PIR meeting, update playbooks, fix gaps | Lessons-learned doc |

## Volatility 3 Command Reference

| Command | Plugin | Purpose |
|---------|--------|---------|
| `vol.py -f dump.raw windows.pslist` | PsList | All running processes (linear scan) |
| `vol.py -f dump.raw windows.pstree` | PsTree | Process tree with parent-child |
| `vol.py -f dump.raw windows.psscan` | PsScan | Pool-based scan (finds hidden procs) |
| `vol.py -f dump.raw windows.cmdline` | CmdLine | Command line for each process |
| `vol.py -f dump.raw windows.netstat` | NetStat | Network connections (active + recent) |
| `vol.py -f dump.raw windows.malfind` | Malfind | Injected code / suspicious memory |
| `vol.py -f dump.raw windows.dlllist` | DllList | Loaded DLLs per process |
| `vol.py -f dump.raw windows.handles` | Handles | Open handles per process |
| `vol.py -f dump.raw windows.dumpfiles --pid N` | DumpFiles | Dump process to disk |
| `vol.py -f dump.raw windows.svcscan` | SvcScan | Installed and running services |
| `vol.py -f dump.raw windows.registry.hivelist` | HiveList | List loaded registry hives |

## Sysmon Event ID Quick Reference

| Event ID | Name | Detection Use |
|----------|------|--------------|
| 1 | Process Create | Malicious launches, LOLBins, encoded PowerShell |
| 2 | File Create Time Changed | Timestomping (T1070.006) |
| 3 | Network Connection | Outbound C2, unexpected connections per process |
| 5 | Process Terminated | Short-lived malicious processes |
| 7 | Image Loaded | Unsigned DLLs, DLL hijacking |
| 8 | CreateRemoteThread | Process injection (T1055) |
| 10 | ProcessAccess | LSASS access → credential dumping (T1003.001) |
| 11 | File Create | Malware drops, new executables in temp paths |
| 12 | Registry Key Created | Persistence via run keys |
| 13 | Registry Value Set | Run key values being written |
| 15 | File Create Stream Hash | Alternate Data Streams (ADS) |
| 17/18 | Pipe Events | Named pipe C2 (PsExec, Cobalt Strike) |
| 22 | DNS Query | Resolves domain per process — C2 DNS detection |
| 25 | Process Tampering | Process hollowing, doppelgänging |

## Pyramid of Pain — IOC Value Table

| IOC Type | Ease of Change for Attacker | Detection Value |
|----------|---------------------------|-----------------|
| File hashes (MD5/SHA256) | Trivial (recompile) | Very low |
| IP addresses | Easy (rotate VPS/VPN) | Low |
| Domain names | Moderate (register new) | Medium |
| Network artefacts (JA3, URIs) | Hard | Medium-high |
| Host artefacts (paths, mutexes) | Hard | High |
| Tools (Mimikatz, Cobalt Strike) | Hard | High |
| TTPs (behaviours, ATT&CK techniques) | Very hard | Very high |

## Evidence Acquisition Checklist

```
[ ] RAM capture FIRST (volatile data — ephemeral)
[ ] Record SHA-256 hash of all collected items
[ ] Use write-blocker for disk acquisition
[ ] Document exact timestamps (acquisition, chain of custody)
[ ] Create forensic image (dd, FTK Imager, DC3DD)
[ ] Verify image integrity: hash original == hash copy
[ ] Label and seal physical evidence
[ ] Log analyst name, date, tools used
```

## Memory Acquisition Tools

| Tool | Platform | Command |
|------|----------|---------|
| WinPMem | Windows | `winpmem.exe memory.raw` |
| DumpIt | Windows | `DumpIt.exe /O memory.dmp` |
| LiME | Linux (kernel module) | `insmod lime.ko "path=/output/mem.lime format=lime"` |
| Avml | Linux | `avml output.lime` |

## Disk Imaging Commands

```bash
# Linux dd image
dd if=/dev/sda of=/mnt/evidence/sda.img bs=4M status=progress conv=noerror,sync

# Verify hash
sha256sum /dev/sda > sda.sha256
sha256sum sda.img >> sda.sha256
diff <(head -1 sda.sha256 | cut -d' ' -f1) <(tail -1 sda.sha256 | cut -d' ' -f1)

# Faster imaging with dc3dd
dc3dd if=/dev/sda of=evidence.img hash=sha256 log=acquisition.log

# Remote imaging (Velociraptor)
velociraptor artifacts collect Windows.Disk.Raw --args device="\\\\.\\PhysicalDrive0"
```

## IOC Quick Lookup Commands

```bash
# Check hash on VirusTotal (CLI)
curl -s -X POST "https://www.virustotal.com/vtapi/v2/file/report" \
  -d "apikey=YOUR_KEY&resource=SHA256_HASH"

# Enrich IP with AbuseIPDB
curl -G https://api.abuseipdb.com/api/v2/check \
  --data-urlencode "ipAddress=1.2.3.4" \
  -H "Key: YOUR_KEY" -H "Accept: application/json"

# Check domain in OTX
curl https://otx.alienvault.com/api/v1/indicators/domain/evil.com/general \
  -H "X-OTX-API-KEY: YOUR_KEY"
```
