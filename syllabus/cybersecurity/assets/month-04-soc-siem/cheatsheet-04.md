# Month 4 — Cheatsheet: SOC Operations & SIEM

## Splunk SPL Quick Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `search` | Filter events | `index=windows EventCode=4625` |
| `stats` | Aggregate data | `\| stats count by src_ip` |
| `sort` | Order results | `\| sort -count` |
| `head` / `tail` | Limit results | `\| head 10` |
| `where` | Filter post-stats | `\| where count > 5` |
| `eval` | Compute new fields | `\| eval risk=if(count>10,"high","low")` |
| `rex` | Regex extraction | `\| rex "User=(?P<user>\w+)"` |
| `timechart` | Time-series chart | `\| timechart count by EventCode` |
| `lookup` | Enrich with table | `\| lookup geo_lookup ip OUTPUT country` |
| `dedup` | Remove duplicates | `\| dedup Account_Name` |
| `rename` | Rename fields | `\| rename Account_Name AS username` |
| `table` | Select output columns | `\| table _time, user, src_ip` |

## Splunk Time Modifiers

| Syntax | Meaning |
|--------|---------|
| `earliest=-24h` | Last 24 hours |
| `earliest=-7d latest=-1d` | 7 days ago to 1 day ago |
| `earliest=@d` | Start of today |
| `earliest=-1h@h` | Start of current hour minus 1 |

## KQL Quick Reference (Microsoft Sentinel)

| Operator | Purpose | Example |
|----------|---------|---------|
| `where` | Filter rows | `\| where EventID == 4625` |
| `summarize` | Aggregate | `\| summarize count() by Account` |
| `order by` | Sort | `\| order by TimeGenerated desc` |
| `project` | Select columns | `\| project Account, Computer` |
| `extend` | Add column | `\| extend risk = "high"` |
| `top N by` | Top N rows | `\| top 10 by count_` |
| `ago()` | Relative time | `TimeGenerated > ago(1h)` |
| `between` | Time range | `TimeGenerated between(start..end)` |
| `has` | String contains | `CommandLine has "mimikatz"` |
| `matches regex` | Regex filter | `Account matches regex @"^admin"` |
| `join` | Join tables | `\| join kind=inner OtherTable on $left.IP == $right.IP` |

## Critical Windows Event IDs Reference

| Event ID | Log | Description | ATT&CK Relevance |
|----------|-----|-------------|-----------------|
| 4624 | Security | Logon success | Baseline |
| 4625 | Security | Logon failure | Brute force (T1110) |
| 4648 | Security | Explicit credential logon | Pass-the-hash (T1550.002) |
| 4672 | Security | Special privileges assigned | Privilege escalation |
| 4688 | Security | Process creation | Execution (T1059) |
| 4698 | Security | Scheduled task created | Persistence (T1053.005) |
| 4720 | Security | User account created | Persistence (T1136) |
| 4732 | Security | Added to local group | Privilege escalation |
| 4768 | Security | Kerberos TGT request | Kerberoasting (T1558.003) |
| 4769 | Security | Kerberos service ticket | Kerberoasting |
| 7045 | System | Service installed | Persistence (T1543.003) |
| 1102 | Security | Audit log cleared | Defense evasion (T1070.001) |

## MITRE ATT&CK Tactics & Common Techniques

| Tactic | High-Value Technique | Technique ID |
|--------|---------------------|-------------|
| Initial Access | Phishing | T1566 |
| Execution | PowerShell | T1059.001 |
| Persistence | Scheduled Task | T1053.005 |
| Privilege Escalation | Token Impersonation | T1134 |
| Defense Evasion | Obfuscated Files | T1027 |
| Credential Access | OS Credential Dumping | T1003 |
| Discovery | System Network Scan | T1046 |
| Lateral Movement | Pass the Hash | T1550.002 |
| C2 | DNS Tunneling | T1071.004 |
| Exfiltration | Exfil Over C2 Channel | T1041 |

## ELK Stack Ports & Config

| Service | Default Port | Config File | Key Setting |
|---------|-------------|-------------|-------------|
| Elasticsearch | 9200 (HTTP), 9300 (transport) | elasticsearch.yml | `network.host` |
| Logstash | 5044 (Beats input) | logstash.conf | pipeline settings |
| Kibana | 5601 | kibana.yml | `elasticsearch.hosts` |
| Filebeat | — (agent) | filebeat.yml | `output.logstash` |

## Common Log Sources & What They Detect

| Log Source | Detects |
|------------|---------|
| Windows Security Event Log | Logons, account changes, privilege use |
| Sysmon | Process, network, file, registry at granular level |
| DNS logs | C2 beaconing, DGA domains, DNS tunneling |
| Firewall logs | Port scans, blocked outbound, unusual protocols |
| Proxy/web logs | Suspicious downloads, C2 over HTTP, data exfil |
| Active Directory logs | Password sprays, group membership changes |

## SOC Shift Handover Template

```
Shift: [Date] [Start]-[End] | Analyst: [Name]
Open Tickets: [IDs and status]
Escalated: [ID → L2/L3 reason]
False Positives Tuned: [Rule name, what was changed]
Ongoing Investigations: [Summary]
Watch Items: [IPs/accounts to monitor]
```
