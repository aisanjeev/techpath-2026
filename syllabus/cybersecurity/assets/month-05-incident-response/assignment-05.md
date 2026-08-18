# Month 5 — Assignment: Incident Response & Digital Forensics
**Total Marks: 100 | Submission: ZIP folder + PDF incident report**

---

## Task 1 — NIST IR Phase Analysis (20 marks)

You are an IR analyst at a financial services company. You receive the following alert at 09:00:

> *"Security alert: User `j.singh` logged on to fileserver-02 from IP 185.220.101.47 (Tor exit node) at 08:47. This account was also used for 47 failed RDP login attempts against 12 servers in the previous hour."*

For each of the 6 NIST IR phases, describe the **specific actions you would take** in this scenario. Use bullet points and be concrete — avoid generic textbook definitions.

**Marking Breakdown:**

| Criterion | Marks |
|-----------|-------|
| Prepare phase response is relevant and pre-incident-focused | 3 |
| Identify actions correctly confirm incident scope | 3 |
| Contain actions are specific and do not destroy evidence | 4 |
| Eradicate actions address root cause (not just symptoms) | 4 |
| Recover actions include monitoring uplift and user communication | 3 |
| Learn section includes at least one playbook or detection improvement | 3 |

---

## Task 2 — Memory Forensics with Volatility 3 (30 marks)

Download the provided memory dump sample: `task2-memory.raw` (link in resources portal).

Using Volatility 3, analyse the dump and answer the following:

**2a)** List all running processes. Identify any process that appears suspicious (unexpected name, unusual parent, runs from a temp path). Justify your reasoning. *(8 marks)*

**2b)** Run the network connections plugin. List all established or listening connections. Identify any connection to an external IP on a suspicious port (e.g. 4444, 1337, 443 to an unknown host). *(7 marks)*

**2c)** Run the malfind plugin. For any flagged region, note the PID, process name, and the first few bytes of the injected region. Does this look like a PE file? (Hint: look for `MZ` header = 4D 5A). *(8 marks)*

**2d)** Dump the suspicious process identified in 2a using `windows.dumpfiles`. Submit the dumped file path and a VirusTotal screenshot showing its detection result. *(7 marks)*

**Commands to use:**
```bash
python vol.py -f task2-memory.raw windows.pstree.PsTree
python vol.py -f task2-memory.raw windows.netstat.NetStat
python vol.py -f task2-memory.raw windows.malfind.Malfind
python vol.py -f task2-memory.raw windows.dumpfiles.DumpFiles --pid <SUSPICIOUS_PID>
```

---

## Task 3 — Professional Incident Report (35 marks)

Based on the simulated intrusion in Task 2 (and the alert from Task 1 if using those details), write a professional incident report as if you were a senior IR analyst delivering findings to the CISO.

**Required sections:**

1. **Executive Summary** (max 150 words — written for a non-technical audience)
2. **Incident Timeline** (table: UTC timestamp, event, source of evidence)
3. **Technical Analysis** (what the attacker did, which tools were used, how they got in)
4. **IOCs** (all discovered IP addresses, file hashes, domains, usernames, process names)
5. **MITRE ATT&CK Mapping** (min 3 techniques with IDs and evidence justifying each)
6. **Immediate Recommendations** (3-5 specific containment or hardening actions)

**Marking Breakdown:**

| Section | Marks |
|---------|-------|
| Executive summary is clear, non-technical, and accurate | 6 |
| Timeline is detailed, chronological, and evidence-attributed | 7 |
| Technical analysis explains the kill chain coherently | 8 |
| IOCs are complete and correctly formatted | 5 |
| ATT&CK mapping is accurate with evidence citations | 5 |
| Recommendations are actionable and specific | 4 |

---

## Task 4 — Threat Intelligence Enrichment (15 marks)

Using the IOCs from Task 2 (or the scenario IP `185.220.101.47`), perform threat intelligence enrichment using **at least 3 different platforms**.

For each IOC:
- Record the platform used (VirusTotal, AbuseIPDB, OTX, Shodan, etc.)
- Screenshot the results
- Write 2 sentences interpreting what the result tells you about the attacker

| Platform Used | IOC Checked | Key Finding |
|--------------|-------------|-------------|
| _(fill in)_ | _(fill in)_ | _(fill in)_ |

**Bonus (+5):** Import your IOCs into a local MISP instance and create an event. Screenshot the event view.

**Marking Breakdown:**

| Criterion | Marks |
|-----------|-------|
| At least 3 platforms used | 6 |
| Screenshots provided for each lookup | 5 |
| Interpretations are accurate and contextual | 4 |
| Bonus: MISP event created | 5 |

---

## Submission Checklist

- [ ] PDF report: Tasks 1, 3, and 4 written responses
- [ ] Volatility command outputs (copy-paste to PDF or include as .txt files)
- [ ] Screenshots: Volatility pstree, netstat, malfind output; VirusTotal results
- [ ] IOC list as a separate plain-text file (for import to SIEM)
- [ ] Naming convention: `assignment-05-[your-name].zip`

## Rubric Summary

| Task | Marks |
|------|-------|
| Task 1 — NIST Phase Analysis | 20 |
| Task 2 — Memory Forensics | 30 |
| Task 3 — Incident Report | 35 |
| Task 4 — Threat Intel | 15 |
| **Total** | **100** |
