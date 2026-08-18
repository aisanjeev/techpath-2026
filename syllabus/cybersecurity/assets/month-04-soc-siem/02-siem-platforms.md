# SIEM Platforms: Splunk, Microsoft Sentinel & ELK Stack

## Why SIEM?

A SIEM (Security Information and Event Management) is the central nervous system of a SOC. It ingests logs from hundreds of sources, correlates events across time and systems, and surfaces the patterns that matter. Without a SIEM, analysts are manually reviewing individual log files — an impossible task at scale.

Modern SIEMs do three things:
1. **Collect** — Ingest, normalise, and store logs from every source
2. **Detect** — Apply correlation rules, ML models, and threat intel to find threats
3. **Respond** — Trigger alerts, ticket creation, and automated playbook execution

---

## Platform Comparison

| Feature | Splunk Enterprise | Microsoft Sentinel | Elastic Security (ELK) |
|---------|------------------|--------------------|------------------------|
| **Cost** | High (GB/day pricing) | Medium (pay-per-GB) | Free (open source) |
| **Query Language** | SPL | KQL | Lucene / KQL |
| **Deployment** | On-prem or cloud | Azure cloud only | Self-hosted or Elastic Cloud |
| **Integration** | Extensive app marketplace | Deep Azure/M365 native | Good with Beats ecosystem |
| **Learning Curve** | Medium | Medium | Higher (more config) |
| **Market Share** | ~30% enterprise SOCs | Growing (Azure shops) | Common in startups/labs |
| **Best For** | Large enterprises, MSSPs | Microsoft-heavy environments | Budget-conscious / open source |

---

## Splunk Deep Dive

### Architecture

```
Data Sources → Forwarder → Indexer → Search Head
(servers,          (ships       (indexes &    (UI, dashboards,
 endpoints,         raw logs)    stores data)   SPL queries)
 cloud, apps)
```

### SPL Query Anatomy

Every SPL search follows a pipe-based pipeline:

```spl
<search terms> | <command 1> | <command 2> | ...
```

Example — full pipeline for brute force detection:
```spl
index=windows                    ← specify the index
EventCode=4625                   ← filter by field
earliest=-1h                     ← time modifier
| stats count AS fails            ← aggregate
    by Account_Name, src_ip       ← group by fields
| where fails > 10               ← threshold filter
| sort -fails                    ← order by fail count
| table Account_Name, src_ip, fails  ← select columns
```

### Key SPL Concepts

| Concept | Example |
|---------|---------|
| Boolean logic | `(EventCode=4625 OR EventCode=4648) NOT Account_Name="*$"` |
| Wildcard | `process_name="*powershell*"` |
| Field extraction | `\| rex field=_raw "cmd=(?P<command>.+?)\s"` |
| Subsearch | `[search index=blacklist \| return 100 ip]` |
| Lookup | `\| lookup ip_geo_lookup ip OUTPUT country` |
| Calculated field | `\| eval risk=if(count>20, "critical", "medium")` |

### Splunk Alert Rule Types

- **Real-time** — fires immediately when condition is met
- **Scheduled** — runs a saved search on a cron schedule and alerts if result count meets threshold
- **Rolling window** — looks at a sliding time window for pattern detection

---

## Microsoft Sentinel Deep Dive

### Architecture

```
Log Sources → Log Analytics Workspace → Sentinel (analytics rules)
(Azure, M365,     (storage, KQL         (alerts, incidents,
 on-prem via        query engine)         playbooks, workbooks)
 AMA/MMA)
```

Sentinel runs entirely in Azure — no servers to manage. Pricing is per GB ingested.

### KQL Query Anatomy

```kql
SecurityEvent                           // table name
| where EventID == 4625                 // filter
| where TimeGenerated > ago(1h)         // time range
| summarize count() by Account, Computer  // aggregate
| where count_ > 5                      // threshold
| order by count_ desc                  // sort
| project Account, Computer, count_     // select columns
```

### Sentinel Analytics Rule Types

| Rule Type | Use Case |
|-----------|----------|
| Scheduled | Run KQL query on a schedule, alert on results |
| Microsoft Security | Auto-create incidents from M365 Defender alerts |
| Fusion | ML-based correlation of anomalies → incidents |
| Anomaly | Behavioural baselines using ML |
| Near Real-Time (NRT) | Trigger within minutes of event |

### KQL Key Functions

```kql
ago(1h)                     // relative time: 1 hour ago
now()                       // current timestamp
bin(TimeGenerated, 5m)      // time bucket for time charts
tostring(column)            // type conversion
extract("regex", 0, field)  // regex extraction
parse_json(column)          // parse embedded JSON
mv-expand baggage           // expand array/multi-value fields
```

---

## ELK Stack Deep Dive

### Architecture

```
Winlogbeat / Filebeat → Logstash (optional) → Elasticsearch → Kibana
(ships raw logs)        (parse, enrich)       (index & store)  (search & visualize)
```

Logstash is optional — for simple use cases, Beats can ship directly to Elasticsearch. Logstash is valuable when you need complex parsing, enrichment, or multi-destination routing.

### Logstash Pipeline

```ruby
input {
  beats { port => 5044 }
}

filter {
  if [winlog][event_id] == 4625 {
    mutate { add_tag => ["failed-logon"] }
    geoip { source => "[winlog][event_data][IpAddress]" }
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "security-events-%{+YYYY.MM.dd}"
  }
}
```

### Kibana KQL (not identical to Sentinel KQL)

Kibana uses a simpler query syntax in Discover and dashboards:

```
winlog.event_id: 4625 and user.name: "administrator"
winlog.event_id: (4625 or 4648) and not user.name: "SYSTEM"
process.name: "powershell.exe" and winlog.event_id: 4688
```

---

## Log Normalisation

Different systems use different field names for the same concept. Normalisation maps them to a common schema:

| Raw Field | Splunk | Elastic Common Schema (ECS) |
|-----------|--------|-----------------------------|
| Username | Account_Name | user.name |
| Source IP | src_ip | source.ip |
| Process | New_Process_Name | process.name |
| Hostname | ComputerName | host.name |
| Timestamp | _time | @timestamp |

Using normalised field names means detection rules can be written once and applied across sources — key for multi-SIEM environments.

---

## Choosing a SIEM for Your Homelab

For learning and portfolio building, the recommendation is:

1. **Start with Security Onion** — all-in-one, free, realistic enterprise feel
2. **Splunk (dev licence)** — best for job market, most employer-facing certifications
3. **ELK Stack** — best if you want to understand the underlying technology
4. **Microsoft Sentinel (free trial)** — essential if targeting Azure/M365 environments
